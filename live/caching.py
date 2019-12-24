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

    def __getitem__(self, index):
        values = self._get_values(start=index, stop=index)
        if values:
            return values[0]

    def __contains__(self, value):
        return value in self._get_values()

    def append(self, value):
        return self.redis.zadd(self._key, {value: self._max_score() + 1})

    def remove(self, value):
        return self.redis.zrem(self._key, value)

    def pop(self):
        return self.redis.zpopmax(self._key, count=1).decode()

    def popleft(self):
        return self.redis.zpopmin(self._key, count=1).decode()


class CachedExpiringMemberListSet(CachedListSet):
    """Same functionality as CachedListSet, but also handles queued guest timeouts
    """

    cache = caches[settings.SESSION_CACHE_ALIAS]

    def __init__(self, key_prefix, member_timeout):
        super().__init__(key=key_prefix)
        self.cache_key_prefix = key_prefix + "cache:"
        self.member_timeout = member_timeout

    def _is_active(self, session_key):
        if self.cache.get(self.cache_key_prefix + session_key):
            return True
        else:
            self.remove(session_key)
            return False

    def _get_values(self):
        return filter(self._is_active, super()._get_values())

    def __len__(self):
        return len([i for i in self._get_values()])

    def reset_member_expiry(self, session_key):
        """Returns True if the key was successfully touched, False otherwise
        See: https://docs.djangoproject.com/en/2.2/topics/cache/
        """
        return self.cache.touch(
            self.cache_key_prefix + session_key, self.member_timeout
        )

    def append(self, session_key):
        "Append session to queue if not already in it, and update the status expiration"
        result = super().append(value=session_key)
        self.cache.add(self.cache_key_prefix + session_key, session_key)
        self.reset_member_expiry(session_key)
        return result

    def remove(self, session_key):
        result = super().remove(value=session_key)
        self.cache.delete(self.cache_key_prefix + session_key)
        return result

    def pop(self):
        result = self._get_values()[-1]
        self._session_keys.remove(value=result)
        self.cache.delete(self.cache_key_prefix + result)
        return result

    def popleft(self):
        result = self._get_values()[0]
        self._session_keys.remove(value=result)
        self.cache.delete(self.cache_key_prefix + result)
        return result
