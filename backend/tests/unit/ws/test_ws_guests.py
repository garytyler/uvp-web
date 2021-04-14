import pytest
from async_asgi_testclient import TestClient


@pytest.mark.asyncio
async def test_guest_ws_broadcasts_feature_to_guests_on_connect(
    pg_container, app, create_random_feature_obj, create_random_guest_obj
):
    async with TestClient(app, timeout=20) as client:
        random_feature = await create_random_feature_obj()
        await create_random_guest_obj(feature=random_feature)
        async with client.websocket_connect(f"/ws/guest/{random_feature.slug}") as ws:
            received_json = await ws.receive_json()
            assert received_json["feature"]["id"] == str(random_feature.id)
            assert received_json["feature"]["title"] == random_feature.title
            assert received_json["feature"]["slug"] == random_feature.slug
            async with client.websocket_connect(
                f"/ws/guest/{random_feature.slug}"
            ) as ws2:
                received_json2 = await ws2.receive_json()
                assert received_json2["feature"]["id"] == str(random_feature.id)
                assert received_json2["feature"]["title"] == random_feature.title
                assert received_json2["feature"]["slug"] == random_feature.slug
