from importlib import import_module

from channels.db import database_sync_to_async as db_sync_to_async
from django.conf import settings

SessionStore = getattr(import_module(settings.SESSION_ENGINE), "SessionStore")


def get_session(session_key: str):
    return SessionStore(session_key).load()


async def async_get_session(session_key: str):
    return await db_sync_to_async(get_session)(session_key=session_key)


def get_sessions(session_keys: list):
    return [get_session(session_key=sk) for sk in session_keys]


async def async_get_sessions(session_keys: list):
    return await db_sync_to_async(get_sessions)(session_keys=session_keys)


def get_session_store(session_key: str):
    return SessionStore(session_key)
