import os
import sys
from pathlib import Path

import dotenv

dotenv.load_dotenv()
current_directory = Path(__file__).parent.parent

sys.path.append(str(current_directory))

import asyncio
import multiprocessing
import traceback
from copy import deepcopy
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass
import uvicorn
from uvicorn.config import LOGGING_CONFIG

from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, JSONResponse
from google.auth import default
from google.cloud import bigquery
from google.oauth2 import service_account
from trilogy.constants import DEFAULT_NAMESPACE
from trilogy.core.enums import Purpose
from trilogy.core.models import (
    ProcessedQuery,
    ProcessedQueryPersist,
    ProcessedShowStatement,
    ShowStatement,
    MultiSelectStatement,
    SelectStatement,
    PersistStatement,
    DataType,
)
from trilogy import Environment, Executor, Dialects
from trilogy.parser import parse_text
from starlette.background import BackgroundTask
from trilogy_public_models import models as public_models
from trilogy.parsing.render import render_query, Renderer
from sqlalchemy import create_engine
from backend.io_models import (
    ListModelResponse,
    Model,
    GenAIConnectionInSchema,
    QueryInSchema,
    GenAIQueryInSchema,
    GenAIQueryOutSchema,
    FormatQueryOutSchema,
    ModelInSchema,
    QueryOut,
    QueryOutColumn,
    ConnectionInSchema,
    ConnectionListItem,
    ConnectionListOutput,
)
from backend.models.helpers import model_to_response
from sqlalchemy_bigquery import *  # this is for pyinstaller

from sqlalchemy_bigquery.base import BigQueryDialect
from duckdb_engine import Dialect as DuckDBDialect
from trilogy.executor import generate_result_set
from trilogy_nlp.core import NLPEngine
from trilogy.core.models import LazyEnvironment
from logging import getLogger
import click
from click_default_group import DefaultGroup
from sqlalchemy.dialects import registry

# force registry here
# to avoid issues with dynamic imports in pyinstaller
registry.impls["bigquery"] = BigQueryDialect
registry.impls["duckdb"] = DuckDBDialect

logger = getLogger(__name__)

PORT = 5678

STATEMENT_LIMIT = 100

PARSE_DEPENDENCY_RESOLUTION_ATTEMPTS = 10

app = FastAPI()


def load_pyinstaller_trilogy_files() -> None:
    # dynamic imports used by trilogy_public_models
    # won't function properly in a pyinstaller bundle
    # so we manually load the modules here
    if not getattr(sys, "frozen", False):
        return
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    application_path = Path(sys._MEIPASS)  # type: ignore
    search_path = application_path / "trilogy_public_models"

    test = Path(search_path)

    for item in test.glob("**/*trilogy"):
        if item.name == "entrypoint.trilogy":
            relative = item.parent.relative_to(test)
            label = str(relative).replace("/", ".")
            if label in public_models:
                continue
            public_models[label] = LazyEnvironment(
                    load_path=Path(item), working_path=Path(test.parent)
                )


load_pyinstaller_trilogy_files()


@dataclass
class InstanceSettings:
    connections: Dict[str, Executor]
    models: Dict[str, Environment]


allowed_origins = [
    "app://.",
]

# if not IN_APP_CONFIG.validate:
allowed_origins += [
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:8090",
]
allow_origin_regex = "(app://.)|(http://localhost:[0-9]+)"


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization"],
    allow_origin_regex=allow_origin_regex,
)


CONNECTIONS: Dict[str, Executor] = {}

GENAI_CONNECTIONS: Dict[str, NLPEngine] = {}

router = APIRouter()


def safe_format_query(input: str) -> str:
    input = input.strip()
    if input[-1] != ";":
        return input + ";"
    return input


def parse_env_from_full_model(input: ModelInSchema) -> Environment:
    env = Environment()

    parsed: dict[str, Environment] = dict()
    successful = set()
    attempts = 0
    exception = None
    # attempt to determine the dependency order of inputs
    # TODO: do some smarter first path dependency resolution based on imports
    while (
        len(parsed) < len(input.sources)
        and attempts < PARSE_DEPENDENCY_RESOLUTION_ATTEMPTS
    ):
        attempts += 1
        for source in input.sources:
            if source.alias in successful:
                continue
            try:
                if source.alias:
                    new = Environment()
                    for k, v in parsed.items():
                        new.add_import(k, v)
                    new.parse(source.contents)
                    env.add_import(source.alias, new)
                    parsed[source.alias] = new
                else:
                    env.parse(source.contents)
                successful.add(source.alias)
            except Exception as e:
                exception = e
                pass
    success = len(successful) == len(input.sources)
    if not success:
        raise ValueError(
            f"unable to parse input models after {attempts} attempts; "
            f"successfully parsed {parsed.keys()}; error was {str(exception)},"
            f"have {[c.address for c in env.concepts.values()]}"
        )

    return env


## Begin Endpoints
@router.get("/models", response_model=ListModelResponse)
async def get_models() -> ListModelResponse:
    models = []
    for key, value in public_models.items():
        models.append(model_to_response(name=key, env=value))
    return ListModelResponse(models=models)


@router.get("/model/{model}", response_model=Model)
async def get_model(model: str) -> Model:
    if model in CONNECTIONS:
        connection = CONNECTIONS[model]
        return model_to_response(model, connection.environment, True)
    if model not in public_models:
        raise HTTPException(404, f"model {model} not found")
    return model_to_response(model, public_models[model], True)


@router.get("/connections")
async def list_connections():
    output = []
    for key, value in CONNECTIONS.items():
        output.append(
            ConnectionListItem(name=key, dialect=value.dialect, model=value.environment)
        )
    return ConnectionListOutput(connections=output)


@router.put("/connection")
def update_connection(connection: ConnectionInSchema):
    # if connection.name not in CONNECTIONS:
    #     raise HTTPException(status_code=404, detail=f"Connection {connection.name} not found.")
    return create_connection(connection)


@router.post("/connection")
def create_connection(connection: ConnectionInSchema):
    if connection.full_model is not None:
        try:
            environment = parse_env_from_full_model(connection.full_model)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    elif connection.model:
        try:
            environment = deepcopy(public_models[connection.model])
        except KeyError:
            environment = Environment()
    else:
        environment = Environment()
    if connection.dialect == Dialects.BIGQUERY:
        if connection.extra and connection.extra.get("user_or_service_auth_json"):
            import json
            from google.auth._default import load_credentials_from_dict

            credentials, project = load_credentials_from_dict(
                json.loads(connection.extra["user_or_service_auth_json"])
            )
        elif os.path.isfile("/run/secrets/bigquery_auth"):
            credentials = service_account.Credentials.from_service_account_file(
                "/run/secrets/bigquery_auth",
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )
            project = credentials.project_id
        elif "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
            credentials = service_account.Credentials.from_service_account_file(
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )
            project = credentials.project_id
        else:
            credentials, project = default()
        if connection.extra:
            project = connection.extra.get("project", project)
        if not project:
            raise HTTPException(
                status_code=400,
                detail="BigQuery dialect requires a project to be specified in the extra field",
            )
        client = bigquery.Client(credentials=credentials, project=project)
        engine = create_engine(
            f"bigquery://{project}/test_tables?user_supplied_client=True",
            connect_args={"client": client},
        )
        executor = Executor(
            dialect=connection.dialect, engine=engine, environment=environment
        )
    elif connection.dialect == Dialects.SNOWFLAKE:
        if not connection.extra or not all(
            [x in connection.extra for x in ["username", "password", "account"]]
        ):
            raise HTTPException(
                status_code=400,
                detail="Snowflake requires a username, password, and account to be set",
            )
        assert connection.extra
        username = connection.extra["username"]
        password = connection.extra["password"]
        account = connection.extra["account"]
        engine = create_engine(
            f"snowflake://{username}:{password}@{account}",
        )
        executor = Executor(
            dialect=connection.dialect, engine=engine, environment=environment
        )
    elif connection.dialect == Dialects.DUCK_DB:
        executor = Executor(
            dialect=connection.dialect,
            engine=create_engine("duckdb:///:memory:"),
            environment=environment,
        )
    else:
        raise HTTPException(400, "this dialect type is not supported currently")
    CONNECTIONS[connection.name] = executor


@router.post("/gen_ai_connection")
def create_gen_ai_connection(connection: GenAIConnectionInSchema):
    engine = NLPEngine(
        # name=connection.name,
        provider=connection.provider,
        model=connection.extra.get("model", None) if connection.extra else None,
        api_key=connection.api_key,
    )
    try:
        engine.test_connection()
    except Exception as e:
        raise HTTPException(
            status_code=403,
            detail=f"Error validating connection: {str(e)}",
        )
    GENAI_CONNECTIONS[connection.name] = engine


@router.post("/raw_query")
def run_raw_query(query: QueryInSchema):
    start = datetime.now()
    # we need to use a deepcopy here to avoid mutation the model default
    executor = CONNECTIONS.get(query.connection)
    if not executor:
        raise HTTPException(401, "Not a valid connection")
    try:
        rs = executor.engine.execute(query.query)
        outputs = [
            (
                col,
                QueryOutColumn(
                    name=col,
                    purpose=Purpose.KEY,
                    datatype=DataType.STRING,
                ),
            )
            for col in rs.keys()
        ]
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
        connection=query.connection,
        query=query.query,
        generated_sql=query.query,
        headers=headers,
        results=query_output,
        duration=int(delta.total_seconds() * 1000),
        columns=outputs,
    )
    return output


@router.post("/gen_ai_query")
def run_genai_query(query: GenAIQueryInSchema):
    from trilogy_nlp.main import parse_query

    datetime.now()
    executor = CONNECTIONS.get(query.connection)
    if not executor:
        raise HTTPException(
            403, "Not a valid live connection. Refresh connection, then retry."
        )

    gen_ai = GENAI_CONNECTIONS.get(query.genai_connection)
    if not gen_ai:
        raise HTTPException(
            403, "Not a valid genai connection. Refresh connection, then retry."
        )
    assert executor
    assert gen_ai
    try:
        processed_query = parse_query(
            input_text=query.text,
            input_environment=executor.environment,
            debug=True,
            llm=gen_ai.llm,
        )

        generated = render_query(processed_query)
        return GenAIQueryOutSchema(text=generated)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query")
def run_query(query: QueryInSchema):
    start = datetime.now()
    executor = CONNECTIONS.get(query.connection)
    if not executor:
        raise HTTPException(
            403, "Not a valid live connection. Refresh connection, then retry."
        )

    outputs = []
    # parsing errors or generation
    # should be 422
    try:
        _, pre_parsed = parse_text(safe_format_query(query.query), executor.environment)
        parsed: List[
            SelectStatement | PersistStatement | MultiSelectStatement | ShowStatement
        ] = [
            x
            for x in pre_parsed
            if isinstance(
                x,
                (
                    SelectStatement,
                    PersistStatement,
                    MultiSelectStatement,
                    ShowStatement,
                ),
            )
        ]
        sql = executor.generator.generate_queries(executor.environment, parsed)
    except Exception as e:
        raise HTTPException(status_code=422, detail="Parsing error: " + str(e))
    # execution errors should be 500
    try:
        rs = None
        compiled_sql = ""
        for statement in sql:
            # for UI execution, cap the limit
            if isinstance(statement, ProcessedQuery):
                statement.limit = (
                    min(int(statement.limit), STATEMENT_LIMIT)
                    if statement.limit
                    else STATEMENT_LIMIT
                )

            if isinstance(statement, (ProcessedQuery, ProcessedQueryPersist)):
                compiled_sql = executor.generator.compile_statement(statement)
                rs = executor.engine.execute(compiled_sql)
                outputs = [
                    (
                        col.name,
                        QueryOutColumn(
                            name=(
                                col.name.replace(".", "_")
                                if col.namespace == DEFAULT_NAMESPACE
                                else col.address.replace(".", "_")
                            ),
                            purpose=col.purpose,
                            datatype=col.datatype.data_type,
                        ),
                    )
                    for col in statement.output_columns
                    if col not in statement.hidden_columns
                ]
            elif isinstance(statement, (ProcessedShowStatement)):
                select: ProcessedQuery | ProcessedQueryPersist = statement.output_values[0]  # type: ignore # noqa: E501
                compiled_sql = executor.generator.compile_statement(select)
                outputs = [
                    (
                        col.name,
                        QueryOutColumn(
                            name=(
                                col.name.replace(".", "_")
                                if col.namespace == DEFAULT_NAMESPACE
                                else col.address.replace(".", "_")
                            ),
                            purpose=col.purpose,
                            datatype=col.datatype.data_type,
                        ),
                    )
                    for col in statement.output_columns
                ]
                rs = generate_result_set(
                    statement.output_columns,
                    [
                        executor.generator.compile_statement(x)
                        for x in statement.output_values
                        if isinstance(x, ProcessedQuery)
                    ],
                )

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
        connection=query.connection,
        query=query.query,
        generated_sql=compiled_sql,
        headers=headers,
        results=query_output,
        duration=int(delta.total_seconds() * 1000),
        columns=outputs,
    )
    return output


@router.post("/format_query")
def format_query(query: QueryInSchema):
    executor = CONNECTIONS.get(query.connection)
    if not executor:
        raise HTTPException(
            403, "Not a valid live connection. Refresh connection, then retry."
        )
    try:
        _, parsed = parse_text(safe_format_query(query.query), executor.environment)
    except Exception as e:
        raise HTTPException(status_code=422, detail="Parsing error: " + str(e))
    renderer = Renderer()
    output = FormatQueryOutSchema(
        text="\n\n".join([renderer.to_string(x) for x in parsed])
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
    for task in asyncio.all_tasks():
        print(f"cancelling task: {task}")
        try:
            task.cancel()
        except Exception:
            print(f"Task kill failed: {_get_last_exc()}")
            pass
    asyncio.gather(*asyncio.all_tasks())
    loop = asyncio.get_running_loop()
    loop.stop()


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Overdrive the default exception handler to allow for graceful shutdowns"""
    if exc.status_code == 503:
        # here is where we terminate all running processes
        task = BackgroundTask(exit_app)
        return PlainTextResponse(
            "Server is shutting down", status_code=exc.status_code, background=task
        )
    # this is a local application, so we don't sanitize 500 responses to
    # support debugging
    # TODO: reevaluate as needed
    elif exc.status_code == 500:
        return JSONResponse(
            status_code=412,
            content=jsonable_encoder({"detail": exc.detail}),
        )
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"detail": exc.detail}),
    )


app.include_router(router)


@click.group(cls=DefaultGroup, default="run", default_if_no_args=True)
def cli():
    pass


@cli.command()
def run():
    LOGGING_CONFIG["disable_existing_loggers"] = True
    import sys

    if os.environ.get("in-ci"):
        print("Running in a unit test, exiting")
        exit(0)
    elif getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        print("running in a PyInstaller bundle")

        f = open(os.devnull, "w")
        sys.stdout = f
        def run():
            uvicorn.run(
            app,
            host="0.0.0.0",
            port=PORT,
            log_level="info",
            log_config=LOGGING_CONFIG,
        )
    else:
        print("Running in a normal Python process, assuming dev")

        def run():
            return uvicorn.run(
                "main:app",
                host="0.0.0.0",
                port=PORT,
                log_level="info",
                log_config=LOGGING_CONFIG,
                reload=True,
            )

    try:
        run()
    except Exception as e:
        print(f"Server is shutting down due to {e}")
        exit(1)


@cli.command()
def test():
    # assert that we have multiple values
    assert len(public_models.values()) > 2


if __name__ == "__main__":
    multiprocessing.freeze_support()
    try:
        cli()
        sys.exit(0)
    except:  # noqa: E722
        sys.exit(0)
