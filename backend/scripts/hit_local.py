import sys
from pathlib import Path

import dotenv

dotenv.load_dotenv()
current_directory = Path(__file__).parent.parent.parent

sys.path.append(str(current_directory))

import requests
from backend.io_models import ConnectionInSchema, QueryInSchema
from trilogy import Dialects

if __name__ == "__main__":
    response = requests.post(
        "http://0.0.0.0:5678/connection",
        data=ConnectionInSchema(
            name="test", dialect=Dialects.BIGQUERY, extra={"project": "preqldata"}
        ).model_dump_json(),
    )

    print(response.status_code)
    print(response.text)

    response = requests.post(
        "http://0.0.0.0:5678/query",
        data=QueryInSchema(
            connection="test", query="select 1 -> test;"
        ).model_dump_json(),
    )

    print(response.status_code)
    print(response.text)
