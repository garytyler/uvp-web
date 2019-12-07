import pytest
from channels.db import database_sync_to_async as db_sync_to_async

# @pytest.mark.asyncio
# @pytest.mark.django_db(transaction=True)
# @pytest.mark.parametrize("num_guests", ([2, 5]))
# async def test_add_guests_to_queue_on_connect_database(guest_factory, num_guests):
#     assert 0 == len(feature.current_guests)  # queue is empty
#     guests = [await guest_factory() for n in range(num_guests)]
#     guest_sessions = [guest["client"].session.session_key for guest in guests]
#     for guest in guests:
#         connected, subprotocol = await guest["communicator"].connect()
#         await asyncio.sleep(0.05)
#         assert connected is True
#     queued_sessions = feature.current_guests
#     assert num_guests == len(guest_sessions) == len(queued_sessions)
#     assert isinstance(guest_sessions, list)
#     assert isinstance(queued_sessions, list)
#     assert guest_sessions == queued_sessions


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("num_guests", ([2, 5]))
async def test_add_guests_to_queue_on_connect(
    guest_factory, presenter_factory, num_guests, feature_factory
):
    feature = await db_sync_to_async(feature_factory)()
    assert 0 == len(feature.guest_queue)
    guests = [await guest_factory(feature_slug=feature.slug) for n in range(num_guests)]
    guest_sessions = tuple(guest["client"].session.session_key for guest in guests)
    for guest in guests:
        connected, subprotocol = await guest["communicator"].connect()
        assert connected is True
    queued_sessions = feature.guest_queue
    assert num_guests == len(guest_sessions) == len(queued_sessions)
    assert tuple(guest_sessions) == tuple(queued_sessions)


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("num_guests", ([2, 5]))
async def test_remove_guests_from_queue_on_disconnect(
    guest_factory, num_guests, feature_factory
):
    feature = await db_sync_to_async(feature_factory)()
    guests = [await guest_factory(feature_slug=feature.slug) for n in range(num_guests)]
    guest_sessions = tuple(guest["client"].session.session_key for guest in guests)
    for guest in guests:
        connected, subprotocol = await guest["communicator"].connect()
        assert connected is True
    queued_sessions = feature.guest_queue
    assert num_guests == len(guest_sessions) == len(queued_sessions)
    for guest in guests:
        await guest["communicator"].disconnect()
    assert 0 == len(feature.guest_queue)
