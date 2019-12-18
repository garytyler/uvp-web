import json

import pytest
from channels.db import database_sync_to_async as db_sync_to_async

from live.models import Feature


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_connected_guest_session_has_guest_name_item(
    fake_guest_factory, feature_factory, SessionStore
):
    # Create objects
    feature = await db_sync_to_async(feature_factory)()
    guest = await fake_guest_factory(feature_slug=feature.slug)
    assert 0 == len(feature.guest_queue)

    # Connect guest
    connected, subprotocol = await guest["communicator"].connect()
    assert connected is True

    # Test state
    assert 1 == len(feature.guest_queue)
    assert SessionStore(feature.guest_queue[0])["guest_name"]


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_feature_connection_sets_feature_channel_name(
    fake_guest_factory, feature_factory, fake_presenter_factory
):
    # Create objects
    feature = await db_sync_to_async(feature_factory)()
    assert not feature.presenter_channel

    # Connect guests
    presenter = await fake_presenter_factory(feature_slug=feature.slug)
    connected, subprotocol = await presenter["communicator"].connect()
    assert connected

    # Get latest feature after connecting
    feature = await db_sync_to_async(lambda: Feature.objects.get(slug=feature.slug))()

    # Test state
    assert feature.presenter_channel


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_init_message(single_connected_guest_presenter_feature):
    # Create objects
    guest, presenter, feature = single_connected_guest_presenter_feature

    # Get latest feature state after connecting
    feature = await db_sync_to_async(lambda: Feature.objects.get(slug=feature.slug))()

    # Receive init message
    message_json = await guest["communicator"].receive_from()
    message_data = json.loads(message_json)

    # Test state
    assert message_data["feature"]["channel_name"] == feature.presenter_channel
    assert message_data["feature"]["title"] == feature.title
    assert len(message_data["guest_queue"]) == 1
