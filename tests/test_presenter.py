import pytest
from channels.db import database_sync_to_async as db_sync_to_async

from live.models import Feature


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_feature_connection_sets_feature_channel_name(
    fake_guest_factory, feature_factory, fake_presenter_factory
):
    # Create objects
    feature = await db_sync_to_async(feature_factory)()
    assert not feature.channel_name

    # Connect guests
    presenter = await fake_presenter_factory(feature_slug=feature.slug)
    connected, subprotocol = await presenter["communicator"].connect()
    assert connected

    # Test state
    feature = await db_sync_to_async(lambda: Feature.objects.get(slug=feature.slug))()
    assert feature.channel_name
