from fastapi.testclient import TestClient
from ..main import ConnectionInSchema
from typing import List, Mapping
from trilogy_public_models import models as public_models
from datetime import datetime

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
#         if attempts > max_attempts:
#             raise ValueError(f"Too many attempts, last response {response}")
#     # basic check that they ran async and not 5+5 seconds
#     assert (datetime.now() - datetime1).seconds < 7