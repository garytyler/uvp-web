import asyncio

import pytest
from channels.testing import WebsocketCommunicator
from django.test import Client

from live.consumers import get_feature
from project.routing import application


@pytest.fixture
def communicator_factory():
    def _create_communicator(client, path):
        communicator = WebsocketCommunicator(
            application=application,
            path=path,
            headers=[
                (b"cookie", f"sessionid={client.session.session_key}".encode("ascii"))
            ],
        )
        return communicator

    return _create_communicator


@pytest.mark.asyncio
async def test_guests_added_on_connect_and_removed_on_disconnect(
    caplog, transactional_db, communicator_factory
):
    # Make sure guest queue is empty
    assert 0 == len((await get_feature()).guest_queue)

    # Connect communicators
    clients = [Client() for n in range(3)]
    communicators = []
    for client in clients:
        communicator = communicator_factory(client=client, path="/ws/guest/")
        await communicator.connect()
        communicators.append(communicator)
    await asyncio.sleep(0.5)  # Wait a bit so ORM connect calls can complete

    # Test that guest_queue matches session keys
    assert [i.session.session_key for i in clients] == (await get_feature()).guest_queue

    # Disconnect communicators
    for communicator in communicators:
        await communicator.disconnect()
    await asyncio.sleep(0.5)  # Wait a bit so ORM disconnect calls can complete

    # Test that guest_queue is empty
    assert [] == (await get_feature()).guest_queue
