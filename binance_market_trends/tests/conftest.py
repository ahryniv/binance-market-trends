import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from binance_market_trends.app import create_app
from binance_market_trends.conf.settings import Settings


@pytest.fixture(scope='session')
def app() -> 'FastAPI':
    test_settings = Settings()
    app = create_app(test_settings)
    return app


@pytest.fixture(scope='session')
def client(app: FastAPI) -> TestClient:
    client_ = TestClient(app, raise_server_exceptions=False)
    return client_
