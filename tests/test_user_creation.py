import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_try_create_user():
    response = client.post(
        "auth/register",
        json={
            "username": "ivan",
            "email": "ivan@example.com",
            "password": "1234",
            "repeat_password": "1234",
        },
    )
    assert response.status_code == 200
    assert b"exists" in response.content


@pytest.mark.xfail
def test_create_user():
    response = client.post(
        "auth/register",
        json={
            "username": "elon",
            "email": "mask@example.com",
            "password": "fsjklfjlkdbnvd",
            "repeat_password": "fsjklfjlkdbnvd",
        },
    )
    assert response.status_code == 200
    assert b"created" in response.content


def test_register_existing_user():
    response = client.post(
        url="auth/register",
        json={
            "username": "ivan",
            "email": "ivan@example.com",
            "password": "1234",
            "repeat_password": "1234",
        },
    )
    assert response.status_code == 200, (
        b"This email or username already exists" in response.content
    )


def test_create_user_wrong_passwords():
    response = client.post(
        "auth/register",
        json={
            "username": "moydodir",
            "email": "mddr@example.com",
            "password": "1234",
            "repeat_password": "12345",
        },
    )
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["msg"] == "passwords do not match"


def test_receive_token():
    login_response = client.post(
        "auth/token", {"username": "Danis111", "password": "1234"}
    )
    assert login_response.status_code == 200
    assert len(login_response.json()) == 2
    assert login_response.json()["access_token"] is not None
    assert login_response.json()["token_type"] is not None
