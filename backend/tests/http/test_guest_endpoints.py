import pytest
from async_asgi_testclient import TestClient


@pytest.mark.asyncio
async def test_http_endpoint_create_current_guest(
    app, create_random_feature_obj, faker
):
    url_path = "/api/guests/current"
    async with TestClient(app, use_cookies=True) as client:
        assert not bool(client.cookie_jar.get("session"))
        feature = await create_random_feature_obj()
        guest_data = {"name": faker.name(), "feature_id": str(feature.id)}
        r = await client.post(url_path, json=guest_data)
        assert r.ok
        assert r.json()["id"]
        assert r.json()["name"] == guest_data["name"]
        assert r.json()["feature_id"] == guest_data["feature_id"]
        assert bool(client.cookie_jar.get("session"))
        # Confirm guest_id is saved in session by attempting to create again
        r = await client.post(url_path, json=guest_data)
        assert r.status_code == 400


@pytest.mark.asyncio
async def test_http_endpoint_get_current_guest(app, create_random_feature_obj, faker):
    path = "/api/guests/current"
    async with TestClient(app) as client:
        feature_id = (await create_random_feature_obj()).id
        r = await client.post(
            path,
            # path.format(feature_id=feature_id),
            json={"name": faker.name(), "feature_id": str(feature_id)},
        )
        assert r.ok
        created_guest = r.json()
        r = await client.get(path)
        print(created_guest)
        assert r.ok
        retrieved_guest = r.json()
        print(retrieved_guest)
        assert retrieved_guest["id"]
        assert retrieved_guest["name"]
        assert retrieved_guest["feature_id"]
        assert retrieved_guest == created_guest
        # assert retrieved_guest["id"] == created_guest["id"]
        assert retrieved_guest["name"] == created_guest["name"]
        assert retrieved_guest["feature_id"] == created_guest["feature_id"]
        assert retrieved_guest["feature_id"] == str(feature_id)


@pytest.mark.asyncio
async def test_http_endpoint_get_guest_by_id(
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
