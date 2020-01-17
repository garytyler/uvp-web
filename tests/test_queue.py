import time

import pytest
from channels.db import database_sync_to_async as db_sync_to_async
from django.conf import settings


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("num_guests", ([2, 5]))
async def test_add_guests_to_queue_on_connect(
    fake_presenter_factory, fake_guest_factory, num_guests, feature_factory
):
    # Create Objects
    feature = await db_sync_to_async(feature_factory)()
    assert 0 == len(list(feature.guest_queue))
    presenter = await fake_presenter_factory(feature_slug=feature.slug)
    guests = [
        await fake_guest_factory(feature_slug=feature.slug) for n in range(num_guests)
    ]
    guest_sessions = [guest["client"].session.session_key for guest in guests]

    # Connect presenter
    connected, subprotocol = await presenter["communicator"].connect()
    assert connected is True

    # Connect guests
    for guest in guests:
        connected, subprotocol = await guest["communicator"].connect()
        assert connected is True

    # Test state
    guest_queue_session_keys = list(feature.guest_queue)
    assert num_guests == len(guest_sessions) == len(guest_queue_session_keys)
    assert tuple(guest_sessions) == tuple(guest_queue_session_keys)


@pytest.mark.skip  # Queue member timeout is not used with current queue management
@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("num_guests", ([2, 5]))
async def test_queued_guests_expire(
    fake_presenter_factory, fake_guest_factory, num_guests, feature_factory, mocker
):
    # Create Objects
    feature = await db_sync_to_async(feature_factory)()
    assert 0 == len(list(feature.guest_queue))
    presenter = await fake_presenter_factory(feature_slug=feature.slug)
    guests = [
        await fake_guest_factory(feature_slug=feature.slug) for n in range(num_guests)
    ]
    guest_sessions = [guest["client"].session.session_key for guest in guests]

    # Connect presenter
    connected, subprotocol = await presenter["communicator"].connect()
    assert connected is True

    # Connect guests
    for guest in guests:
        connected, subprotocol = await guest["communicator"].connect()
        assert connected is True

    # Check that guests are queued
    assert num_guests == len(guest_sessions) == len(list(feature.guest_queue))

    # Wait for expiry
    time.sleep(getattr(settings, "GUEST_QUEUE_MEMBER_TIMEOUT") + 0.5)

    # Test that queue is empty
    assert 0 == len(list(feature.guest_queue))


@pytest.mark.skip  # Removal is currently only handled by the observer
@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("num_guests", ([2, 5]))
async def test_remove_guests_from_queue_on_disconnect(
    fake_presenter_factory, fake_guest_factory, num_guests, feature_factory
):
    # Create objects
    feature = await db_sync_to_async(feature_factory)()
    presenter = await fake_presenter_factory(feature_slug=feature.slug)
    guests = [
        await fake_guest_factory(feature_slug=feature.slug) for n in range(num_guests)
    ]
    guest_sessions = [guest["client"].session.session_key for guest in guests]

    # Connect presenter
    connected, subprotocol = await presenter["communicator"].connect()
    assert connected is True

    # Connect guests
    for guest in guests:
        connected, subprotocol = await guest["communicator"].connect()
        assert connected is True

    # Test state
    assert num_guests == len(guest_sessions) == len(feature.guest_queue)
    for guest in guests:
        await guest["communicator"].disconnect()
    assert 0 == len(feature.guest_queue)
