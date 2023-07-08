import os
import sys
from pathlib import Path

import dotenv

dotenv.load_dotenv()
current_directory = Path(__file__).parent.parent

sys.path.append(str(current_directory))

import asyncio
import multiprocessing
import os
import sys
import traceback
from copy import deepcopy
from datetime import datetime
from typing import Mapping, Optional

import uvicorn
from fastapi import APIRouter, FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from google.auth import default
from google.cloud import bigquery
from google.oauth2 import service_account
from preql.constants import DEFAULT_NAMESPACE
from preql.core.enums import DataType, Purpose
from preql.executor import Dialects, Executor
from preql.parser import parse_text
from pydantic import BaseModel, Field
from sqlalchemy.engine import create_engine
from starlette.background import BackgroundTask
from starlette.exceptions import HTTPException as StarletteHTTPException
from trilogy_public_models import models
from trilogy_public_models import models as public_models
from uvicorn.config import LOGGING_CONFIG

from backend.io_models import ListModelResponse, Model, UIConcept
from backend.models.helpers import flatten_lineage

PORT = 5678

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    # allow_origins=[
    #     "http://localhost:8080",
    #     "http://localhost:8081",
    #     "http://localhost:8090",
    #     "app://.",
    # ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


## BEGIN REQUESTS


class InputRequest(BaseModel):
    text: str
    # conversation:str


## Begin Endpoints
router = APIRouter()


class QueryInSchema(BaseModel):
    model: str
    query: str
    # chart_type: ChartType | None = None


class QueryOutColumn(BaseModel):
    name: str
    datatype: DataType
    purpose: Purpose


class QueryOut(BaseModel):
    model: str
    query: str
    generated_sql: str
    headers: list[str]
    results: list[dict]
    created_at: datetime = Field(default_factory=datetime.now)
    refreshed_at: datetime = Field(default_factory=datetime.now)
    duration: Optional[int]
    columns: Mapping[str, QueryOutColumn] | None


STATEMENT_LIMIT = 100
GCP_PROJECT = "ttl-test-355422"


def safe_format_query(input: str) -> str:
    input = input.strip()
    if input[-1] != ";":
        return input + ";"
    return input


@router.get("/models", response_model=ListModelResponse)
async def get_models() -> ListModelResponse:
    models = []
    for key, value in public_models.items():
        final_concepts = []
        for skey, sconcept in value.concepts.items():
            # don't show private concepts
            if sconcept.name.startswith("_"):
                continue
            final_concepts.append(
                UIConcept(
                    name=sconcept.name,
                    datatype=sconcept.datatype,
                    purpose=sconcept.purpose,
                    description=sconcept.metadata.description
                    if sconcept.metadata
                    else None,
                    namespace=sconcept.namespace,
                    key=skey,
                    lineage=flatten_lineage(sconcept, depth=0),
                )
            )
        final_concepts.sort(key=lambda x: x.namespace + x.key)
        models.append(Model(name=key, concepts=final_concepts))
    return ListModelResponse(models=models)


@router.post("/query")
async def run_query(query: QueryInSchema):
    start = datetime.now()
    if os.path.isfile("/run/secrets/bigquery_auth"):
        credentials = service_account.Credentials.from_service_account_file(
            "/run/secrets/bigquery_auth",
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        project = credentials.project_id
    else:
        credentials, project = default()
    client = bigquery.Client(credentials=credentials, project=GCP_PROJECT)
    engine = create_engine(
        f"bigquery://{GCP_PROJECT}/test_tables?user_supplied_client=True",
        connect_args={"client": client},
    )

    # we need to use a deepcopy here to avoid mutation the model default
    try:
        environment = deepcopy(models[query.model])
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Model {query.model} not found.")
    executor = Executor(
        dialect=Dialects.BIGQUERY, engine=engine, environment=environment
    )
    outputs = {}
    # parsing errors or generation
    # should be 422
    try:
        _, parsed = parse_text(safe_format_query(query.query), executor.environment)
        sql = executor.generator.generate_queries(executor.environment, parsed)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=422, detail="Parsing error: " + str(e))
    # execution errors should be 500
    try:
        rs = None
        compiled_sql = ""
        for statement in sql:
            # for UI execution, cap the limit
            statement.limit = (
                min(int(statement.limit), STATEMENT_LIMIT)
                if statement.limit
                else STATEMENT_LIMIT
            )
            compiled_sql = executor.generator.compile_statement(statement)
            rs = executor.engine.execute(compiled_sql)
            outputs = {
                col.name: QueryOutColumn(
                    name=col.name
                    if col.namespace == DEFAULT_NAMESPACE
                    else col.address.replace(".", "_"),
                    purpose=col.purpose,
                    datatype=col.datatype,
                )
                for col in statement.output_columns
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if not rs:
        headers = []
        query_output = []
    else:
        headers = list(rs.keys())
        query_output = [
            {"_index": idx, **dict(row.items())}
            for idx, row in enumerate(rs.fetchall())
        ]
    # return execution time to frontend
    delta = datetime.now() - start
    output = QueryOut(
        model=query.model,
        query=query.query,
        generated_sql=compiled_sql,
        headers=headers,
        results=query_output,
        duration=int(delta.total_seconds() * 1000),
        columns=outputs,
    )
    return output


## Core
@router.get("/")
async def healthcheck():
    return "healthy"


@router.get("/terminate")
async def terminate():
    raise HTTPException(503, "Terminating server")


@app.on_event("shutdown")
def shutdown_event():
    print("Shutting down...!")


def _get_last_exc():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    sTB = "\n".join(traceback.format_tb(exc_traceback))
    return f"{exc_type}\n - msg: {exc_value}\n stack: {sTB}"


async def exit_app():
    if asyncio.Task:
        for task in asyncio.all_tasks():
            print(f"cancelling task: {task}")
            try:
                task.cancel()
            except Exception:
                print(f"Task kill failed: {_get_last_exc()}")
                pass
    asyncio.gather(asyncio.all_tasks())
    loop = asyncio.get_running_loop()
    loop.stop()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    if exc.status_code == 503:
        task = BackgroundTask(exit_app)
        return PlainTextResponse(
            "Server is shutting down", status_code=exc.status_code, background=task
        )
    return Response(status_code=exc.status_code, headers=exc.headers, content=exc.detail)


app.include_router(router)


def run():
    LOGGING_CONFIG["disable_existing_loggers"] = True
    import sys

    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        print("running in a PyInstaller bundle, setting sys.stdout to devnull")

        f = open(os.devnull, "w")
        sys.stdout = f
    else:
        print("running in a normal Python process")
    try:
        uvicorn.run(
            app, host="localhost", port=PORT, log_level="info", log_config=LOGGING_CONFIG
        )
    except Exception:
        print("GOT AN ERROR RUNNING")
        print("Server is shutting down")
        exit(0)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    try:
        run()
        sys.exit(0)
    except:  # noqa: E722
        sys.exit(0)
