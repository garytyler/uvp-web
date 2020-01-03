from datetime import timedelta

BEAT_SCHEDULE = {
    "status-manager": [
        {
            "type": "refresh.guest.queue.state",
            "message": {"feature_slug": "big-one"},
            "schedule": timedelta(seconds=2),  # Every 5 seconds
        }
    ],
    "status-receiver": [],
}
