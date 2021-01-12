import pytest
from httpx import AsyncClient

from app.core.security import verify_password
from app.models.users import User


@pytest.mark.asyncio
async def test_create_user(app, faker, create_random_password) -> None:
    user_password = create_random_password()
    payload = dict(password=user_password, email=faker.safe_email(), name=faker.name())
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/api/users", json=payload)  # type: ignore
    assert r.status_code == 200
    assert r.json()["email"] == payload["email"]
    user_obj = await User.get(email=payload["email"])
    assert user_obj
    assert verify_password(user_password, user_obj.hashed_password)


@pytest.mark.asyncio
async def test_get_own_user(
    app, create_random_password, create_random_user_obj
) -> None:
    user_password = create_random_password()
    user_obj = await create_random_user_obj(password=user_password)

    # get access token
    payload = dict(username=user_obj.email, password=user_password)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/api/access/token", data=payload)
    assert r.status_code == 200
    access_token = r.json()["access_token"]

    # get own user
    async with AsyncClient(
        app=app,
        base_url="http://test",
        headers={"Authorization": f"Bearer {access_token}"},
    ) as ac:
        r = await ac.get("/api/users/current")
    assert r.status_code == 200
    assert r.json()["id"] == str(user_obj.id)
    assert r.json()["email"] == user_obj.email


@pytest.mark.asyncio
async def test_update_own_user_email(
    app, create_random_password, create_random_user_obj, faker
) -> None:
    user_password = create_random_password()
    old_user_obj = await create_random_user_obj(password=user_password)

    # get access token
    payload = dict(username=old_user_obj.email, password=user_password)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/api/access/token", data=payload)
    assert r.status_code == 200
    access_token = r.json()["access_token"]

    # update email
    new_email = faker.safe_email()
    async with AsyncClient(
        app=app,
        base_url="http://test",
        headers={"Authorization": f"Bearer {access_token}"},
    ) as ac:
        r = await ac.patch(
            "/api/users/current",
            json={"email": new_email},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert r.status_code == 200
        new_user_obj = await User.get(id=old_user_obj.id)
        assert new_email == new_user_obj.email


@pytest.mark.asyncio
async def test_update_own_user_password(
    app, create_random_password, create_random_user_obj, faker
) -> None:
    old_password = create_random_password()
    old_user_obj = await create_random_user_obj(password=old_password)

    # get access token
    payload = dict(
        username=old_user_obj.email, password=old_password, name=old_user_obj.name
    )
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/api/access/token", data=payload)
    assert r.status_code == 200
    access_token = r.json()["access_token"]

    # update own user password
    new_password = create_random_password()
    async with AsyncClient(
        app=app,
        base_url="http://test",
        headers={"Authorization": f"Bearer {access_token}"},
    ) as ac:
        r = await ac.patch(
            "/api/users/current",
            json={"password": new_password},
            headers={"Authorization": f"Bearer {access_token}"},
        )
    assert r.status_code == 200

    new_user_obj = await User.get(id=old_user_obj.id)
    assert new_user_obj
    assert verify_password(new_password, new_user_obj.hashed_password)
