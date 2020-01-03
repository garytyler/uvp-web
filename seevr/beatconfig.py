from datetime import timedelta

from django.conf import settings

BEAT_SCHEDULE: dict = {
    "observer": [
        {
            "type": "run",
            "message": {},
            "schedule": timedelta(seconds=settings.GUEST_STATUS_CHECK_INTERVAL),
        }
    ],
}
