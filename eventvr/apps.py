from django.apps import AppConfig


class EventVRConfig(AppConfig):
    name = "eventvr"

    def ready(self):
        import eventvr.signals
