import logging
import os

from django.apps import AppConfig


class LiveConfig(AppConfig):
    name = "live"

    django_logger = logging.getLogger("django")
    django_logger.setLevel(os.getenv("LOG_LEVEL_DJANGO", "INFO"))
    live_logger = logging.getLogger("live")
    live_logger.setLevel(os.getenv("LOG_LEVEL_PROJECT", "INFO"))

    def ready(self):
        pass
