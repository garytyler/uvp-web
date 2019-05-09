from django.apps import AppConfig


class eventvrConfig(AppConfig):
    name = "eventvr"

    def ready(self):
        import eventvr.signals
