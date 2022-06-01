import pytest
from fastapi.testclient import TestClient
from app.main import app
from httpx import AsyncClient
from app.api.services.statistics_services import get_standard_deviations


client = TestClient(app)


@pytest.mark.anyio
async def test_welcome():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Welcome"}


def test_average_min_max_price_by_exchange():
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


@pytest.mark.parametrize(
    "input_data",
    ["NEAR", "DOGE", "ATOM", "BAT"],
)
def test_show_charts(input_data):
    response = client.get(f"/charts/{input_data}")
    assert response.status_code == 200
    assert type(response.content) is not None


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
@pytest.mark.parametrize(
    "input_data",
    ["BTC", "SOL", "ATOM", "LUNA"],
)
async def test_add_favourite_crypto_user_authenticated(input_data):
    user_credentials = {"username": "Danis111", "password": "1234"}
    async with AsyncClient(app=app, base_url="http://127.0.0.1/") as ac:
        response = await ac.post(url="auth/token", data=user_credentials)
        assert response.status_code == 200
        data = response.json()

        token = data["access_token"]
        async with AsyncClient(app=app, base_url="http://127.0.0.1/") as ac2:
            sec_response = await ac2.post(
                url="/add_favourite_crypto",
                json={"name_crypto": input_data},
                headers={
                    "Authorization": f"Bearer {token}",
                    "accept": "application/json",
                },
            )
            assert sec_response.status_code == 200
            assert sec_response.content is not None


@pytest.mark.anyio
@pytest.mark.parametrize(
    "input_data",
    ["BTC", "SOL", "ATOM", "LUNA"],
)
async def test_delete_favourite_crypto_user_authenticated(input_data):
    user_credentials = {"username": "Danis111", "password": "1234"}
    async with AsyncClient(app=app, base_url="http://127.0.0.1/") as ac:
        response = await ac.post(url="auth/token", data=user_credentials)
        assert response.status_code == 200
        data = response.json()

        token = data["access_token"]
        async with AsyncClient(app=app, base_url="http://127.0.0.1/") as ac2:
            sec_response = await ac2.post(
                url="/delete_favourite_crypto",
                json={"name_crypto": input_data},
                headers={
                    "Authorization": f"Bearer {token}",
                    "accept": "application/json",
                },
            )
            assert sec_response.status_code == 200


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


@pytest.mark.anyio
@pytest.mark.parametrize(
    "input_data",
    [9000, 88888, 5000, 800],
)
async def test_get_recommendations(input_data):
    user_credentials = {"username": "Danis111", "password": "1234"}
    async with AsyncClient(app=app, base_url="http://127.0.0.1/") as ac:
        response = await ac.post(url="auth/token", data=user_credentials)
        assert response.status_code == 200
        data = response.json()

        token = data["access_token"]
        async with AsyncClient(app=app, base_url="http://127.0.0.1/") as ac2:
            sec_response = await ac2.post(
                url="/recommendations",
                json={"amount_of_money": input_data},
                headers={
                    "Authorization": f"Bearer {token}",
                    "accept": "application/json",
                },
            )
            assert sec_response.status_code == 200


@pytest.mark.parametrize(
    "input_data",
    ["BTC", "SOL", "ATOM", "LUNA"],
)
def test_get_std_devs(input_data):
    x = get_standard_deviations(input_data)
    assert isinstance(x, list) is True


@pytest.mark.parametrize("symbol", ["BTC", "SOL", "ATOM", "LUNA", "ETH", "BNB"])
def test_std_dev(symbol):
    response = client.get("/standard_deviation/{symbol}")
    assert response.status_code == 200


def test_auth_google():
    response = client.get("/auth/google")
    assert response.status_code == 200
