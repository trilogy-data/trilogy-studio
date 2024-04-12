from fastapi.testclient import TestClient
from ..main import (
    ConnectionInSchema,
    parse_env_from_full_model,
    ModelInSchema,

)
from ..io_models import ModelSourceInSchema
from typing import List, Mapping
from trilogy_public_models import models as public_models


def test_read_main(test_client: TestClient):
    response = test_client.get("/")
    assert response.status_code == 200


def test_read_models(test_client: TestClient):
    response = test_client.get("/models")
    assert response.status_code == 200

    arguments: List[Mapping[str, str | None | dict[str, str | None | list]]] = [
        {
            "name": "test-duck",
            "dialect": "duck_db",
            "model": list(public_models.keys())[0],
            "extra": None,
        },
        {
            "name": "test-duck",
            "dialect": "duck_db",
            "model": None,
            "extra": None,
            "full_model": {"name": "fix-names-2", "sources": []},
        },
    ]

    for arg in arguments:
        parsed = ConnectionInSchema.parse_obj(arg)

        response = test_client.post("/connection", data=parsed.json())  # type: ignore
        assert response.status_code == 200


# def test_async_functions(test_client: TestClient):
#     response = test_client.post("/long_sleep", json={"sleep": 1})
#     assert response.status_code == 200
#     assert response.json().get("slept") == 1

#     ## start async test
#     response = test_client.post("/async_long_sleep", json={"sleep": 5})
#     assert response.status_code == 200

#     guid1 = response.json().get("guid")
#     assert guid1 is not None

#     response = test_client.post("/async_long_sleep", json={"sleep": 5})
#     assert response.status_code == 200
#     guid2 = response.json().get("guid")
#     assert guid2 is not None

#     datetime1 = datetime.now()

#     found:set[str] = set()
#     attempts = 0
#     max_attempts = 5
#     from time import sleep

#     while len(found) < 2:
#         attempts += 1
#         for guid in (guid1, guid2):
#             if guid in found:
#                 continue
#             response = test_client.get(f"/background_tasks/{guid}")
#             print(response)
#             if response.status_code == 200:
#                 found.add(guid)
#                 assert response.json().get("slept") == 5
#                 break
#             elif response.status_code == 102:
#                 pass
#             else:
#                 raise ValueError(response)
#         sleep(1)
#         if attempts > max_at,tempts:
#             raise ValueError(f"Too many attempts, last response {response}")
#     # basic check that they ran async and not 5+5 seconds
#     assert (datetime.now() - datetime1).seconds < 7


def test_parse_full():
    input = ModelInSchema(
        name="test",
        sources=[
            ModelSourceInSchema(alias="", contents="select test.constant;"),
            ModelSourceInSchema(alias="test", contents="const constant <-1;"),
        ],
    )
    parse_env_from_full_model(input)

    test = {
        "name": "bigquery.google_analytics",
        "sources": [
            {
                "alias": "fundiverse",
                "contents": "\nkey user_pseudo_id int;\n\ndatasource fundiverse(\n    event_date: generic.event_date,\n    user_pseudo_id: user_pseudo_id,\n    event_time: generic.event_time,\n)\ngrain (generic.event_time)\naddress `preqldata.analytics_411641820.events_*`\n;",
            },
            {
                "alias": "pypreql",
                "contents": "\nkey user_pseudo_id int;\n\ndatasource pypreql(\n    event_date: generic.event_date,\n    user_pseudo_id: user_pseudo_id,\n    event_time: generic.event_time,\n)\ngrain (generic.event_time)\naddress `preqldata.analytics_417320071.events_*`\n;",
            },
            {
                "alias": "generic",
                "contents": "\n\nkey event_time int;\nkey event_date string;\n\n",
            },
        ],
    }
    input = ModelInSchema.model_validate(test)

    parse_env_from_full_model(input)
