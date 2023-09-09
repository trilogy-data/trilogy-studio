from fastapi.testclient import TestClient
from main import ConnectionInSchema
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
