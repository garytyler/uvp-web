from distutils.util import strtobool
from importlib import import_module
from os import getenv

if getenv("DJANGO_SETTINGS_MODULE", default="").endswith("dev"):
    from seevr.settings import *


# Debug
DEBUG = True

# Allowed hosts
ALLOWED_HOSTS = globals()["ALLOWED_HOSTS"] + ["127.0.0.1", "localhost", "0.0.0.0"]

# Template debugging
# Requires current host in INTERNAL_IPS
INTERNAL_IPS = getenv("INTERNAL_IPS", ALLOWED_HOSTS)
TEMPLATE_DEBUG = True if INTERNAL_IPS else False


# Channels
CHANNEL_LAYERS = globals()["CHANNEL_LAYERS"]
if getenv("IN_MEMORY_CHANNEL_LAYER"):
    CHANNEL_LAYERS["default"] = {"BACKEND": "channels.layers.InMemoryChannelLayer"}


# Expire sessions at browser close
SESSION_EXPIRE_AT_BROWSER_CLOSE = strtobool(
    getenv("SESSION_EXPIRE_AT_BROWSER_CLOSE", "False")
)
