from channels.db import database_sync_to_async as db_sync_to_async
from django.contrib.sessions.models import Session
from django.core.cache import caches
from django_redis import get_redis_connection


class CachedList:
    cache = caches["default"]

    def __init__(self, key):
        self.key = key
        if not self.cache.get(self.key):
            self.cache.set(self.key, [])

    def __str__(self) -> str:
        class_name = self.__class__.__name__
        _list = self.cache.get(self.key)
        return str(f"<{class_name} at '{self.key}': {_list}")

    def __repr__(self) -> str:
        return str(self.cache.get(self.key))

    def __len__(self):
        return len(self.cache.get(self.key))

    def __getitem__(self, n: int):
        return self.cache.get(self.key)[n]

    def __iter__(self):
        return iter(self.cache.get(self.key))

    def append(self, x):
        _list = self.cache.get(self.key)
        _list.append(x)
        self.cache.set(self.key, _list)

    def remove(self, x):
        _list = self.cache.get(self.key)
        _list.remove(x)
        self.cache.set(self.key, _list)


class GuestSessionQueue(CachedList):
    def __init__(self, key: str):
        super().__init__(key)

    @db_sync_to_async
    def append(self, session: Session):
        super().append(session.session_key)

    @db_sync_to_async
    def remove(self, session):
        super().remove(session.session_key)

    # @db_sync_to_async
    # def pop(self, n: int) -> Session:
    #     session_key = self.state[n]
    #     self.state.remove(session_key)
    #     return

    # @db_sync_to_async
    # def __getitem__(self, key) -> Session:
    #     if isinstance(key, str):
    #         for session_key, index in enumerate(super()):
    #             if session_key == key:
    #                 return Session.objects.get(pk=session_key)
    #         raise KeyError(key)
    #     elif isinstance(key, int):
    #         return Session.objects.get(pk=super().__getitem__(key))


class RedisListSet:
    """Facade for a redis ordered set to emulate typical list functionality"""

    redis = get_redis_connection("default")

    def __init__(self, key):
        self._key = str(key)

    def __repr__(self):
        return str(self.values())

    def set_timeout(self, secs: int):
        self.timeout = secs

    def append(self, value: str):
        return self.redis.zadd(self._key, {value: self.max_score() + 1})

    def max_score(self) -> int:
        try:
            return self.redis.zrange(
                self._key, -1, -1, withscores=True, score_cast_func=int
            )[0][1]
        except IndexError:
            return 0

    def pop(self):
        return self.redis.bzpopmin(self._key, self.timeout)

    def remove(self, value):
        return self.redis.zrem(self._key, value)

    def values(self):
        members = self.redis.zrange(self._key, 0, -1, desc=True, score_cast_func=int)
        return tuple(map(lambda i: i.decode(), members[::-1]))
