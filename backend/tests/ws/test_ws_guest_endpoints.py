import json

import pytest
from tests._utils.features import create_random_feature
from tests._utils.guests import create_random_guest


@pytest.mark.asyncio
async def test_guest_ws_broadcasts_feature_to_guests_on_connect(xclient):
    async with xclient() as client:
        random_feature = await create_random_feature()
        await create_random_guest(feature=random_feature)
        async with client.websocket_connect(f"/ws/guest/{random_feature.slug}") as ws1:
            async with client.websocket_connect(f"/ws/guest/{random_feature.slug}"):
                received_text = await ws1.recv()
                received_json = json.loads(received_text)
                assert received_json["feature"]["id"] == str(random_feature.id)
                assert received_json["feature"]["title"] == random_feature.title
                assert received_json["feature"]["slug"] == random_feature.slug
