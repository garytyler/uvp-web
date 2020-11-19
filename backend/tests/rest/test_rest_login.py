import pytest
from httpx import AsyncClient

from app.core.security import get_password_hash, verify_password


@pytest.mark.asyncio
async def test_hash_password(create_random_password):
    password = create_random_password()
    password_hash = get_password_hash(password=password)
    assert verify_password(password, password_hash)


@pytest.mark.asyncio
async def test_rest_login_get_access_token_succeeds(
    app, create_random_user, create_random_password
) -> None:
    user_password = create_random_password()
    user_obj = await create_random_user(password=user_password)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"username": user_obj.email, "password": user_password}
        r = await ac.post("/api/token", data=payload)
        assert r.status_code == 200
        assert "access_token" in r.json()
        assert r.json()["access_token"]


@pytest.mark.asyncio
async def test_rest_login_create_user_and_login(
    app, faker, create_random_password
) -> None:
    user_password = create_random_password()

    # create user
    payload = dict(password=user_password, email=faker.safe_email())
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/api/users", json=payload)  # type: ignore
    assert r.status_code == 200
    assert r.json()["email"] == payload["email"]

    # login user
    payload = dict(username=r.json()["email"], password=user_password)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/api/token", data=payload)
    assert r.status_code == 200
    assert "access_token" in r.json()
    assert r.json()["access_token"]
