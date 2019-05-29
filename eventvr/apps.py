from django.apps import AppConfig
from django.db.utils import DatabaseError


class EventVRConfig(AppConfig):
    name = "eventvr"

    def ready(self):
        pass
