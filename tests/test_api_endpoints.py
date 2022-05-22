import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_json_content_type():
    response = client.get("/main_crypto")
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]


def test_top_10_most_expensive():
    response = client.get("/top_most_expensive_assets")
    assert response.status_code == 200
