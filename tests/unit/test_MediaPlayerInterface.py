import pytest


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_media_player_connect(presenter_factory, feature_factory):
    feature = feature_factory(title="DO one")
    presenter = await presenter_factory(feature_slug=feature.slug)
    presenter_communicator = presenter["communicator"]
    connected, subprotocol = await presenter_communicator.connect()
    assert connected is True
