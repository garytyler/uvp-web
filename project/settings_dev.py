import os

if os.getenv("DJANGO_SETTINGS_MODULE").endswith("dev"):
    from project.settings import *


# DEBUG
DEBUG = True


# ALLOWED_HOSTS
allowed_hosts = os.getenv("ALLOWED_HOSTS")
if allowed_hosts:
    ALLOWED_HOSTS += allowed_hosts.split(",")


# INSTALLED_APPS
INSTALLED_APPS += ["django_extensions"]


# Template debugging
TEMPLATE_DEBUG = True  # Requires current host in INTERNAL_IPS
INTERNAL_IPS = os.getenv("INTERNAL_IPS")


# Channels
if os.getenv("IN_MEMORY_CHANNEL_LAYER"):
    CHANNEL_LAYERS["default"] = {"BACKEND": "channels.layers.InMemoryChannelLayer"}


# Sessions
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Default is false
