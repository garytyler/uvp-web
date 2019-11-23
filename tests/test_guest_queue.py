import asyncio

import pytest
from django.test import Client

from live.consumers import get_feature


@pytest.mark.asyncio
async def test_guests_added_on_connect_and_removed_on_disconnect(
    caplog, transactional_db, communicator_factory
):
    # Make sure current guests is empty
    assert 0 == len((await get_feature()).current_guests)

    # Connect communicators
    clients = [Client() for n in range(3)]
    communicators = []
    for client in clients:
        communicator = communicator_factory(client=client, path="/ws/guest/")
        await communicator.connect()
        communicators.append(communicator)
    await asyncio.sleep(0.5)  # Wait a bit so ORM connect calls can complete

    # Test that current_guests matches session keys
    assert [i.session.session_key for i in clients] == (
        await get_feature()
    ).current_guests

    # Disconnect communicators
    for communicator in communicators:
        await communicator.disconnect()
    await asyncio.sleep(0.5)  # Wait a bit so ORM disconnect calls can complete

    # Test that current guests is empty
    assert [] == (await get_feature()).current_guests
