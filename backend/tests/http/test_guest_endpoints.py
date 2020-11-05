import pytest
from async_asgi_testclient import TestClient

from app.models.guests import Guest


@pytest.mark.asyncio
async def test_http_endpoint_create_current_guest(
    app, create_random_feature_obj, faker
):
    url_path = "/api/guests/current"
    async with TestClient(app, use_cookies=True) as client:
        assert not bool(client.cookie_jar.get("session"))
        feature = await create_random_feature_obj()
        payload = {"name": faker.name(), "feature_id": str(feature.id)}
        r = await client.post(url_path, json=payload)
        assert r.ok
        guest_obj = await Guest.get_or_none(**payload)
        assert r.json()["name"] == payload["name"] == guest_obj.name
        assert r.json()["feature_id"] == payload["feature_id"]
        assert bool(client.cookie_jar.get("session"))

        # Check trying to create again with same payload returns error
        r = await client.post(url_path, json=payload)
        assert r.status_code == 400


@pytest.mark.asyncio
async def test_http_endpoint_update_guest(
    app, create_random_feature_obj, create_random_guest_obj, faker
):
    url_path = "/api/guests/{guest_id}"
    async with TestClient(app, use_cookies=True) as client:
        assert not bool(client.cookie_jar.get("session"))
        feature_obj = await create_random_feature_obj()
        guest_obj_start = await create_random_guest_obj(feature=feature_obj)
        payload = {"name": faker.name()}
        r = await client.patch(
            url_path.format(guest_id=str(guest_obj_start.id)), json=payload
        )
        assert r.ok
        guest_obj_updated = await Guest.get_or_none(id=guest_obj_start.id)
        assert r.json()["id"] == str(guest_obj_start.id) == str(guest_obj_updated.id)
        assert r.json()["name"] == payload["name"] == guest_obj_updated.name
        # check did not update fields not defined in payload
        assert guest_obj_start.feature_id == guest_obj_updated.feature_id


@pytest.mark.asyncio
async def test_http_endpoint_get_current_guest(app, create_random_feature_obj, faker):
    path = "/api/guests/current"
    async with TestClient(app) as client:
        feature_id = (await create_random_feature_obj()).id
        payload = {"name": faker.name(), "feature_id": str(feature_id)}
        r = await client.post(path, json=payload)
        assert r.ok
        created_guest = r.json()
        r = await client.get(path)
        assert r.ok
        # assert r.json()["id"] == created_guest["id"]
        assert r.json()["name"] == created_guest["name"]
        assert r.json()["feature_id"] == created_guest["feature_id"]
        assert r.json()["feature_id"] == str(feature_id)


@pytest.mark.asyncio
async def test_http_endpoint_get_guest(
    app, create_random_feature_obj, create_random_guest_obj
):
    path = "/api/guests/{guest_id}"
    async with TestClient(app) as client:
        created_feature = await create_random_feature_obj()
        created_guests = [
            await create_random_guest_obj(created_feature) for _ in range(3)
        ]
        response = await client.get(path.format(guest_id=created_guests[1].id))
        assert response.status_code == 200
        assert response.json()["id"] == str(created_guests[1].id)
        assert response.json()["name"] == str(created_guests[1].name)
        assert response.json()["feature_id"] == str(created_guests[1].feature_id)
