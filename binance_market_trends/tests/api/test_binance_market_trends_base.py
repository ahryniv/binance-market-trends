from http import HTTPStatus

from fastapi.testclient import TestClient


def test_health(client: TestClient):
    response = client.get('version')
    assert response.status_code == HTTPStatus.OK


def test_version(client: TestClient):
    response = client.get('health')
    assert response.status_code == HTTPStatus.OK
