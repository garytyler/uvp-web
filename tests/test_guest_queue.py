import asyncio

import pytest
from django.test import Client

from live.consumers import get_feature


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("num_guests", (range(3)))
async def test_add_guests_to_queue_on_connect(
    feature_factory, guest_factory, num_guests
):
    guests = [await guest_factory(connect=True) for n in range(num_guests)]
    guest_session_keys = [guest["client"].session.session_key for guest in guests]
    current_feature_guests = (await get_feature()).current_guests
    assert guest_session_keys == current_feature_guests
    assert len(guest_session_keys) == len(current_feature_guests) == num_guests

    # @pytest.mark.asyncio
    # @pytest.mark.django_db(transaction=True)
    # async def test_guests_are_removed(
    #     self, feature_factory, guest_factory, client_communicator_factory
    # ):
    #     guests = [await guest_factory(connect=True) for n in range(3)]
    #     guest_clients, guest_communicators = zip(*[i.values() for i in guests])
    #     guest_session_keys = [guest["client"].session.session_key for guest in guests]

    #     await get_feature()

    #     current_feature_guests = (await get_feature()).current_guests
    #     # assert guest_session_keys == current_feature_guests

    #     # Disconnect communicators
    #     for communicator in guest_communicators:
    #         await communicator.disconnect()
    #     await asyncio.sleep(0.5)  # Wait a bit so ORM disconnect calls can complete

    #     # Test that current guests is empty
    #     assert [] == (await get_feature()).current_guests


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_guests_added_on_connect_and_removed_on_disconnect(
    caplog, communicator_factory
):
    # Connect communicators
    guest_clients = [Client() for n in range(3)]
    communicators = []
    for guest_clients in guest_clients:
        communicator = communicator_factory(path="/ws/guest/", client=guest_clients)
        connected, subprotocol = await communicator.connect()
        assert connected is True
        communicators.append(communicator)
    await asyncio.sleep(0.5)  # Wait a bit so ORM connect calls can complete

    # Test that current_guests matches session keys
    assert [i.session.session_key for i in guest_clients] == (
        await get_feature()
    ).current_guests

    # Disconnect communicators
    for communicator in communicators:
        await communicator.disconnect()
    await asyncio.sleep(0.5)  # Wait a bit so ORM disconnect calls can complete

    # Test that current guests is empty
    assert [] == (await get_feature()).current_guests
