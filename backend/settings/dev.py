""" Development Settings """
import os
from distutils.util import strtobool

from ._base import *  # noqa: F403,F401

# Domain name
ALLOWED_HOSTS = ["*"]


# Security
SECRET_KEY = os.environ.get("DJANGO_DEV_SECRET_KEY")
DEBUG = True


# Template debugging (Requires current host in INTERNAL_IPS)
INTERNAL_IPS = os.getenv("INTERNAL_IPS", globals()["ALLOWED_HOSTS"])
TEMPLATE_DEBUG = True if INTERNAL_IPS else False


# Channels
CHANNEL_LAYERS = globals()["CHANNEL_LAYERS"]
if os.getenv("IN_MEMORY_CHANNEL_LAYER"):
    CHANNEL_LAYERS["default"] = {"BACKEND": "channels.layers.InMemoryChannelLayer"}


# Expire sessions at browser close
SESSION_EXPIRE_AT_BROWSER_CLOSE = strtobool(
    os.getenv("SESSION_EXPIRE_AT_BROWSER_CLOSE", "False")
)
