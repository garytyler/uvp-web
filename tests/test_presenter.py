import pytest
from channels.db import database_sync_to_async as db_sync_to_async

from seevr.live.models import Feature


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_presenter_connect_sets_feature_presenter_channel(
    fake_guest_factory, feature_factory, fake_presenter_factory
):
    # Create objects
    feature = await db_sync_to_async(feature_factory)()
    assert not feature.presenter_channel

    # Connect presenter
    presenter = await fake_presenter_factory(feature_slug=feature.slug)
    connected, subprotocol = await presenter["communicator"].connect()
    assert connected

    # Test state
    feature = await db_sync_to_async(lambda: Feature.objects.get(slug=feature.slug))()
    assert feature.presenter_channel


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_presenter_disconnect_unsets_feature_presenter_channel(
    connected_guest_presenter_feature_factory,
):
    # Create objects
    guest, presenter, feature = await connected_guest_presenter_feature_factory()

    # Test feature has presenter_channel set
    feature = await db_sync_to_async(lambda: Feature.objects.get(slug=feature.slug))()
    assert feature.presenter_channel

    # Disconnect
    await presenter["communicator"].disconnect()

    # Test feature has no presenter_channel
    assert not feature.presenter_channel
