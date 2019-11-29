from django_redis import get_redis_connection


class SessionQueueInterface:
    redis = get_redis_connection("default")

    def __init__(self, queue_key):
        self.queue_key = str(queue_key)

    def __repr__(self):
        return str(sorted(self.get(), key=lambda i: i[0]))

    def set_timeout(self, secs: int):
        self.timeout = secs

    def add(self, session_key: str):
        member_score_mapping = {session_key: self.length()}
        return self.redis.zadd(self.queue_key, member_score_mapping, nx=True)

    def pop(self):
        return self.redis.bzpopmin(self.timeout)

    def remove(self, session_key):
        return self.redis.zrem(self.queue_key, session_key)

    def length(self):
        return self.redis.zcard(self.queue_key)

    def ordered_members(self, start=0, stop=-1, reverse=False):
        unordered = self._unordered_pairs(start, stop)
        decoded = map(lambda i: i[0].decode(), unordered)
        ordered = sorted(decoded, key=lambda i: i[0], reverse=reverse)
        return tuple(ordered)

    def ordered_pairs(self, start=0, stop=-1, reverse=False):
        unordered = self._unordered_pairs(start, stop)
        decoded = map(lambda i: (i[0].decode(), i[1]), unordered)
        ordered = sorted(decoded, key=lambda i: i[0], reverse=reverse)
        return tuple(ordered)

    def _unordered_pairs(self, start=0, stop=-1):
        return self.redis.zrange(self.queue_key, start, stop, withscores=True)
