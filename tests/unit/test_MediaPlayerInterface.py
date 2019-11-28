import pytest
from django.test import Client

from live.consumers import get_feature


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_media_player_connect(communicator_factory, transactional_db):
    client = Client()
    media_communicator = communicator_factory(client=client, path="/ws/mediaplayer/")
    connected, subprotocol = await media_communicator.connect()
    assert connected is True
    feature = await get_feature()
    assert feature
