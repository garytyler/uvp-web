from distutils.util import strtobool
from importlib import import_module
from os import getenv

if getenv("DJANGO_SETTINGS_MODULE", default="").endswith("test"):
    from seevr.settings import *


GUEST_QUEUE_MEMBER_PING_INTERVAL = 0.5
GUEST_QUEUE_MEMBER_TIMEOUT = 1
