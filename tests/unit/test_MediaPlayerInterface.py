import pytest
from django.test import Client


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_feature_connect(communicator_factory):
    communicator = communicator_factory(client=Client(), path="/ws/mediaplayer/")
    connected = await communicator.connect()
    assert connected
