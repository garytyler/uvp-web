from django_redis import get_redis_connection


class GuestQueue:
    def __init__(self, queue_id: str):
        self.redis = get_redis_connection("default")
        self.id = queue_id

    def __repr__(self):
        return str(sorted(self.get(0, -1), key=lambda i: i[0]))

    def set_timeout(self, secs: int):
        self.timeout = secs

    def add(self, guest_id: str):
        self.redis.zadd(self.id, {self.redis.zcard(self.id): guest_id}, nx=True)

    def pop(self):
        self.redis.bzpopmin(self.timeout)

    def rem(self, guest_id):
        self.redis.zrem(self.id, guest_id)

    def get(self, start=0, stop=0):
        return self.redis.zrange(self.id, start, stop, withscores=True)
