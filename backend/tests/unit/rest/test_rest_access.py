import pytest
from httpx import AsyncClient

from app.core.security import (
    generate_password_reset_token,
    get_password_hash,
    verify_password,
)
from app.models.users import User


@pytest.mark.asyncio
async def test_hash_password(create_random_password):
    password = create_random_password()
    password_hash = get_password_hash(password=password)
    assert verify_password(password, password_hash)


@pytest.mark.asyncio
async def test_rest_read_access_token_succeeds(
    app, create_random_user_obj, create_random_password
) -> None:
    user_password = create_random_password()
    user_obj = await create_random_user_obj(password=user_password)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"username": user_obj.email, "password": user_password}
        r = await ac.post("/api/access/token", data=payload)
        assert r.status_code == 200
        assert "access_token" in r.json()
        assert r.json()["access_token"]


@pytest.mark.asyncio
async def test_rest_create_user_and_login(app, faker, create_random_password) -> None:
    user_password = create_random_password()

    # create user
    payload = dict(name=faker.name(), password=user_password, email=faker.safe_email())
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/api/users", json=payload)  # type: ignore
    assert r.status_code == 200
    assert r.json()["email"] == payload["email"]

    # access user
    payload = dict(username=r.json()["email"], password=user_password)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/api/access/token", data=payload)
    assert r.status_code == 200
    assert "access_token" in r.json()
    assert r.json()["access_token"]


@pytest.mark.asyncio
async def test_rest_access_reset_password_with_reset_endpoint(
    app,
    faker,
    create_random_user_obj,
    create_random_password,
) -> None:
    # create user
    old_password = create_random_password()
    old_user_obj = await create_random_user_obj(password=old_password)
    assert verify_password(old_password, old_user_obj.hashed_password)

    # reset password with endpoint
    reset_token = generate_password_reset_token(old_user_obj.email)
    new_password = create_random_password()
    payload = {"token": reset_token, "new_password": new_password}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/api/access/reset-password", json=payload)
    assert r.status_code == 200

    # get updated user
    new_user_obj = await User.get(id=old_user_obj.id)

    # old password does not verify
    assert not verify_password(old_password, new_user_obj.hashed_password)

    # new password verifies
    assert verify_password(new_password, new_user_obj.hashed_password)
