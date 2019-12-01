import pytest
from channels.db import database_sync_to_async as db_sync_to_async

from live.consumers import get_feature
from live.models import Feature

# @pytest.mark.asyncio
# @pytest.mark.django_db(transaction=True)
# @pytest.mark.parametrize("num_guests", ([2, 5]))
# async def test_add_guests_to_queue_on_connect_database(guest_factory, num_guests):
#     assert 0 == len((await get_feature()).current_guests)  # queue is empty
#     guests = [await guest_factory() for n in range(num_guests)]
#     guest_sessions = [guest["client"].session.session_key for guest in guests]
#     for guest in guests:
#         connected, subprotocol = await guest["communicator"].connect()
#         await asyncio.sleep(0.05)
#         assert connected is True
#     queued_sessions = (await get_feature()).current_guests
#     assert num_guests == len(guest_sessions) == len(queued_sessions)
#     assert isinstance(guest_sessions, list)
#     assert isinstance(queued_sessions, list)
#     assert guest_sessions == queued_sessions


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("num_guests", ([2, 5]))
async def test_add_guests_to_queue_on_connect(guest_factory, num_guests):
    assert 0 == len((await get_feature()).guest_queue.ordered_members())
    guests = [await guest_factory() for n in range(num_guests)]
    guest_sessions = tuple(guest["client"].session.session_key for guest in guests)
    for guest in guests:
        connected, subprotocol = await guest["communicator"].connect()
        assert connected is True
    queued_sessions = (await get_feature()).guest_queue.ordered_members()
    assert num_guests == len(guest_sessions) == len(queued_sessions)
    assert isinstance(guest_sessions, tuple)
    assert isinstance(queued_sessions, tuple)
    assert guest_sessions == queued_sessions


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("num_guests", ([2, 5]))
async def test_remove_guests_from_queue_on_disconnect(guest_factory, num_guests):
    guests = [await guest_factory() for n in range(num_guests)]
    guest_sessions = tuple(guest["client"].session.session_key for guest in guests)
    for guest in guests:
        connected, subprotocol = await guest["communicator"].connect()
        assert connected is True
    queued_sessions = (await get_feature()).guest_queue.ordered_members()
    assert num_guests == len(guest_sessions) == len(queued_sessions)
    for guest in guests:
        await guest["communicator"].disconnect()
    assert 0 == len((await get_feature()).guest_queue.ordered_members())


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("title", ([("Big One")]))
async def test_add_feature_on_presenter(presenter_factory, guest_factory, title):
    feature = await db_sync_to_async(lambda: Feature.objects.create(title=title))()
    presenter = await presenter_factory(feature.slug)
    connected, subprotocol = await presenter["communicator"].connect()
    assert connected is True
    assert await db_sync_to_async(
        lambda: Feature.objects.get(title=title).channel_name
    )()
    guest = await guest_factory(feature_slug=feature.slug)
    connected, subprotocol = await guest["communicator"].connect()
    assert connected is True

    # assert feature.channel_name
    # assert 0 == len(feature.guest_queue.ordered_members())

    # guest = await guest_factory()
    # assert guest


# @pytest.mark.asyncio
# @pytest.mark.django_db(transaction=True)
# async def test_guests_added_on_connect_and_removed_on_disconnect(
#     caplog, communicator_factory
# ):
#     # Connect communicators
#     guest_clients = [Client() for n in range(3)]
#     communicators = []
#     for guest_clients in guest_clients:
#         communicator = communicator_factory(path="/ws/guest/", client=guest_clients)
#         connected, subprotocol = await communicator.connect()
#         assert connected is True
#         communicators.append(communicator)
#     await asyncio.sleep(0.5)  # Wait a bit so ORM connect calls can complete

#     # Test that current_guests matches session keys
#     assert [i.session.session_key for i in guest_clients] == (
#         await get_feature()
#     ).current_guests

#     # Disconnect communicators
#     for communicator in communicators:
#         await communicator.disconnect()
#     await asyncio.sleep(0.5)  # Wait a bit so ORM disconnect calls can complete

#     # Test that current guests is empty
#     assert [] == (await get_feature()).guest_queue.current_guests
