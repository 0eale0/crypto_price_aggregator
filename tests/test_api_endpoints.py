import pytest
from fastapi.testclient import TestClient
from app.main import app
from httpx import AsyncClient


client = TestClient(app)


def test_json_content_type():
    response = client.get("/main_crypto")
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]


def test_get_crypto_info():
    response = client.post("/get_crypto_info", json={"name_crypto": "bitcoin"})
    assert response.status_code == 200, response.json() is not None

    wrong_response = client.post("/get_crypto_info")
    assert wrong_response.status_code == 422


def test_top_10_most_expensive():
    response = client.get("/top_most_expensive_assets")
    assert response.status_code == 200
    assert len(response.json()) == 10


def test_top_10_cheapest():
    response = client.get("/top_cheapest_assets")
    assert response.status_code == 200
    assert len(response.json()) == 10


def test_recommendations_not_authenticated():
    response = client.post("/recommendations")
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]


def test_get_favourite_crypto_user_not_authenticated():
    response = client.get("/get_favourite_crypto")
    data = response.json()
    assert response.status_code == 401
    assert "Not authenticated" in data["detail"]


@pytest.mark.anyio
async def test_get_favourite_crypto_user_authenticated():
    user_credentials = {"username": "Danis111", "password": "1234"}
    async with AsyncClient(app=app, base_url="http://127.0.0.1/") as ac:
        response = await ac.post(url="auth/token", data=user_credentials)
        assert response.status_code == 200
        data = response.json()

        token = data["access_token"]
        async with AsyncClient(app=app, base_url="http://127.0.0.1/") as ac2:
            sec_response = await ac2.get(
                url="/get_favourite_crypto",
                headers={
                    "Authorization": f"Bearer {token}",
                    "accept": "application/json",
                },
            )
            assert sec_response.status_code == 200
