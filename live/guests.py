from django_redis import get_redis_connection


class SessionQueueInterface:
    redis = get_redis_connection("default")

    def __init__(self, queue_key):
        self.queue_key = str(queue_key)

    def __repr__(self):
        return str(self.ordered_pairs())

    def set_timeout(self, secs: int):
        self.timeout = secs

    def add(self, session_key: str):
        return self.redis.zadd(self.queue_key, {session_key: self.length() + 1})

    def pop(self):
        return self.redis.bzpopmin(self.timeout)

    def remove(self, session_key):
        return self.redis.zrem(self.queue_key, session_key)

    def length(self):
        return self.redis.zcard(self.queue_key)

    def ordered_members(self, start=0, stop=-1, reverse=False):
        unordered = self._unordered_pairs(start, stop)
        ordered = sorted(unordered, key=lambda i: i[1], reverse=reverse)
        return tuple(map(lambda i: i[0].decode(), ordered))

    def ordered_pairs(self, start=0, stop=-1, reverse=False):
        unordered = self._unordered_pairs(start, stop)
        ordered = sorted(unordered, key=lambda i: i[1], reverse=reverse)
        return tuple(map(lambda i: (i[0].decode(), i[1]), ordered))

    def _unordered_pairs(self, start=0, stop=-1):
        return self.redis.zrange(self.queue_key, start, stop, withscores=True)
