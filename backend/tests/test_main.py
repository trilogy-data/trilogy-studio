from fastapi.testclient import TestClient


def test_read_main(test_client: TestClient):
    response = test_client.get("/")
    assert response.status_code == 200


def test_read_models(test_client: TestClient):
    response = test_client.get("/models")
    assert response.status_code == 200
