import logging
import os

from django.apps import AppConfig
from django.db.utils import DatabaseError


class EventVRConfig(AppConfig):
    name = "eventvr"

    django_logger = logging.getLogger("django")
    django_logger.setLevel(os.getenv("LOG_LEVEL_DJANGO", "INFO"))
    eventvr_logger = logging.getLogger("eventvr")
    eventvr_logger.setLevel(os.getenv("LOG_LEVEL_EVENTVR", "INFO"))

    def ready(self):
        pass
