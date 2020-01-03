from django.apps import AppConfig


class LiveConfig(AppConfig):
    name = "live"

    def ready(self):
        pass
