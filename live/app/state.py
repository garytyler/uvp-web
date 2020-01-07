import asyncio
import json
import logging
import threading
import time
import uuid
from importlib import import_module

from channels.db import database_sync_to_async as db_sync_to_async
from channels.layers import get_channel_layer
from django.conf import settings

from live.app import caching
from live.models import Feature

log = logging.getLogger(__name__)


async def watch_feature_state_in_thread(feature_slug):
    thread_name = f"status-watcher:{feature_slug}"

    if not settings.USE_THREAD_BASED_FEATURE_OBSERVERS:
        return log.warning(
            f"Use worker or 'USE_THREAD_BASED_FEATURE_OBSERVERS' {thread_name=}"
        )
    elif any([t.name == thread_name for t in threading.enumerate()]):
        return log.warning(f"Feature thread is already running. {thread_name=}")

    def init_worker(loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    loop = asyncio.new_event_loop()
    worker = threading.Thread(
        target=init_worker, args=(loop,), name=thread_name, daemon=True,
    )
    worker.start()

    async def coro(feature_slug):
        while True:
            await refresh_feature_states(feature_slugs=[feature_slug])
            await asyncio.sleep(settings.GUEST_STATUS_CHECK_INTERVAL)

    loop.call_soon_threadsafe(lambda: asyncio.create_task(coro(feature_slug)))


async def refresh_feature_states(feature_slugs=None):
    if feature_slugs:
        features = []
        for feature_slug in feature_slugs:
            features.append(
                await db_sync_to_async(lambda: Feature.objects.get(slug=feature_slug))()
            )
    else:
        features = await db_sync_to_async(lambda: Feature.objects.all())()

    presenting_features = [f for f in features if f.presenter_channel]
    for feature in presenting_features:
        begin = time.time()

        # Get
        status = await get_guest_queue_member_status(feature=feature)

        # Update
        feature.guest_queue.clear()
        feature.guest_queue.extend(status["sessions"])
        feature.member_channels.clear()
        feature.member_channels.extend(status["channels"])

        # Broadcast
        await broadcast_feature_state(feature=feature)

        # Finish
        time_spent = time.time() - begin
        log_values = f"{feature.slug=}, {time_spent=}, {feature.guest_queue=}"
        log.info("REFRESHED GUEST QUEUE - " + log_values)


async def get_guest_queue_member_status(feature) -> dict:
    """
    - We use group_send instead of individual channel sends because:
        - Decoupling the observer pattern.
        - We can let timeouts handle stuck clients w/ minimal performance loss.
        - Letting timeouts handle stuck clients will help prevent race conditions
        that result in missing channels.
    - We will store channel names only to determiine when to exit listening
        during state updates.
    """
    # Initialize collection store
    collection_key = f"status-store:{feature.slug}:{uuid.uuid1()}"
    collection_store = caching.CachedListSet(collection_key)

    for session_key in feature.guest_queue:
        await get_channel_layer().group_send(
            session_key,
            {
                "type": "update_channel_status",
                "message": {"collection_key": collection_key},
            },
        )

    # Wait for status responses
    num_channels = len(feature.member_channels)
    timeout = time.time() + settings.GUEST_STATUS_PING_TIMEOUT
    while time.time() < timeout:
        await asyncio.sleep(0)
        if num_channels <= len(collection_store):
            break
    await asyncio.sleep(0.1)

    # Parse collected status data
    alive_sessions = []
    alive_channels = []
    for sk, cn in [i.split(":") for i in collection_store]:
        alive_sessions.append(sk)
        alive_channels.append(cn)

    # Create status dict with correct session order
    queued = []
    for sk in feature.guest_queue:
        if sk in alive_sessions:
            queued.append(sk)
            alive_sessions.remove(sk)
    added = alive_sessions

    status = {"sessions": queued + added, "channels": set(alive_channels)}

    return status


async def get_session_stores(session_keys):
    if isinstance(session_keys, str):
        session_keys = [session_keys]
    SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
    return [SessionStore(sk).load() for sk in session_keys]


async def broadcast_feature_state(feature):
    guest_datas = []
    for ss in await get_session_stores(feature.guest_queue):
        guest_datas.append(
            {"guest_name": ss["guest_name"], "session_key": ss["session_key"]}
        )
    for guest_data in guest_datas:
        await get_channel_layer().group_send(
            guest_data["session_key"],
            {
                "type": "send_to_client",
                "message": {
                    "text_data": json.dumps(
                        {
                            "feature": {
                                "presenter_channel": feature.presenter_channel,
                                "title": feature.title,
                            },
                            "guest_queue": guest_datas,
                        }
                    )
                },
            },
        )
    # await get_channel_layer().group_send(
    #     feature.slug,
    #     {
    #         "type": "send_to_client",
    #         "message": {
    #             "text_data": json.dumps(
    #                 {
    #                     "feature": {
    #                         "presenter_channel": feature.presenter_channel,
    #                         "title": feature.title,
    #                     },
    #                     "guest_queue": queue_data,
    #                 }
    #             )
    #         },
    #     },
    # )
