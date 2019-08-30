import os

import django
from django.conf import settings


def pytest_configure():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings_dev")
    settings.DEBUG = False
    django.setup()
