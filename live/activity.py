from django_redis import get_redis_connection


class SessionQueueInterface:
    redis = get_redis_connection("default")

    def __init__(self, queue_key):
        self.key = str(queue_key)

    def __repr__(self):
        return str(self.ordered_pairs())

    def set_timeout(self, secs: int):
        self.timeout = secs

    def append(self, session_key: str):
        return self.redis.zadd(self.key, {session_key: self.max_score() + 1})

    def max_score(self) -> int:
        try:
            return self.redis.zrange(
                self.key, -1, -1, withscores=True, score_cast_func=int
            )[0][1]
        except IndexError:
            return 0

    def pop(self):
        return self.redis.bzpopmin(self.key, self.timeout)

    def remove(self, session_key):
        return self.redis.zrem(self.key, session_key)

    def values(self):
        members = self.redis.zrange(self.key, 0, -1, desc=True, score_cast_func=int)
        return tuple(map(lambda i: i.decode(), members[::-1]))
