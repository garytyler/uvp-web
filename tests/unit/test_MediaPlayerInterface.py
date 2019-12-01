import pytest

from live.consumers import get_feature


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_media_player_connect(presenter_factory, transactional_db):
    presenter = await presenter_factory()
    presenter_communicator = presenter["communicator"]
    connected, subprotocol = await presenter_communicator.connect()
    assert connected is True
    feature = await get_feature()
    assert feature
