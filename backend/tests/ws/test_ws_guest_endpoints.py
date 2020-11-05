import json

import pytest
from asgi_lifespan import LifespanManager


@pytest.mark.asyncio
async def test_guest_ws_broadcasts_feature_to_guests_on_connect(
    procclient, app, create_random_feature_obj, create_random_guest_obj
):
    async with LifespanManager(app):
        random_feature = await create_random_feature_obj()
        await create_random_guest_obj(feature=random_feature)
    async with procclient as client:
        ws = await client.websocket_connect(f"/ws/guest/{random_feature.slug}")
        received_text = await ws.recv()
        received_json = json.loads(received_text)
        assert received_json["feature"]["id"] == str(random_feature.id)
        assert received_json["feature"]["title"] == random_feature.title
        assert received_json["feature"]["slug"] == random_feature.slug
