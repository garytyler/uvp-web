from django.conf import settings
from django.core.cache import caches
from django_redis import get_redis_connection


class CachedList:
    cache = caches[settings.SESSION_CACHE_ALIAS]

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


class CachedListSet:
    """Facade for a redis ordered set that emulates a mutable ordered set"""

    redis = get_redis_connection(settings.SESSION_CACHE_ALIAS)

    def __init__(self, key):
        self._key = str(key)

    def __repr__(self):
        return str(self._get_values())

    def __str__(self):
        return str(self._get_values())

    def _get_values(self, start=0, stop=-1):
        members = self.redis.zrange(
            self._key, start, stop, desc=True, score_cast_func=int
        )
        return tuple(map(lambda i: i.decode(), members[::-1]))

    def _max_score(self) -> int:
        try:
            return self.redis.zrange(
                self._key, -1, -1, withscores=True, score_cast_func=int
            )[0][1]
        except IndexError:
            return 0

    def __len__(self):
        return self.redis.zcard(self._key)

    def __iter__(self):
        return (i for i in self._get_values())

    def __reversed__(self):
        return (i for i in reversed(self._get_values()))

    def __index__(self, value: str):
        return self.redis.zrank.get(self._key, value)

    def __getitem__(self, index):
        values = self._get_values(start=index, stop=index)
        if values:
            return values[0]

    def __contains__(self, value):
        return value in self._get_values()

    def set_timeout(self, secs: int):
        self.timeout = secs

    def append(self, value):
        return self.redis.zadd(self._key, {value: self._max_score() + 1})

    def remove(self, value):
        return self.redis.zrem(self._key, value)

    def pop(self):
        return self.redis.zpopmax(self._key, count=1).decode()

    def popleft(self):
        return self.redis.zpopmin(self._key, count=1).decode()


class Presentation:
    @property
    def guest_queue(self):
        return CachedListSet(self.cache_key_prefix + "guest_queue")


class PresentationManager:
    @property
    def guest_queue(self):
        return CachedListSet(self.cache_key_prefix + "guest_queue")
