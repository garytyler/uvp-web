import logging
import os

from django.apps import AppConfig


class LiveConfig(AppConfig):
    name = "live"

    def ready(self):
        pass
        logging.getLogger(self.name).setLevel(
            os.getenv(f"LOG_LEVEL_{self.name.upper()}", "INFO")
        )
