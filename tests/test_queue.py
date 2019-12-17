import pytest
from channels.db import database_sync_to_async as db_sync_to_async


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("num_guests", ([2, 5]))
async def test_add_guests_to_queue_on_connect(
    fake_guest_factory, num_guests, feature_factory
):
    # Create Objects
    feature = await db_sync_to_async(feature_factory)()
    assert 0 == len(feature.guest_queue)
    guests = [
        await fake_guest_factory(feature_slug=feature.slug) for n in range(num_guests)
    ]
    guest_sessions = [guest["client"].session.session_key for guest in guests]

    # Connect guests
    for guest in guests:
        connected, subprotocol = await guest["communicator"].connect()
        assert connected is True

    # Test state
    assert num_guests == len(guest_sessions) == len(feature.guest_queue)
    assert tuple(guest_sessions) == tuple(feature.guest_queue)


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("num_guests", ([2, 5]))
async def test_remove_guests_from_queue_on_disconnect(
    fake_guest_factory, num_guests, feature_factory
):
    # Create objects
    feature = await db_sync_to_async(feature_factory)()
    guests = [
        await fake_guest_factory(feature_slug=feature.slug) for n in range(num_guests)
    ]
    guest_sessions = [guest["client"].session.session_key for guest in guests]

    # Connect guests
    for guest in guests:
        connected, subprotocol = await guest["communicator"].connect()
        assert connected is True

    # Test state
    assert num_guests == len(guest_sessions) == len(feature.guest_queue)
    for guest in guests:
        await guest["communicator"].disconnect()
    assert 0 == len(feature.guest_queue)
