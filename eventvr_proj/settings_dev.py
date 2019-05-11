import os

if os.getenv("DJANGO_SETTINGS_MODULE").endswith("dev"):
    from eventvr_proj.settings import *

print("* DJANGO DEVELOPMENT ENVIRONMENT *")

# DEBUG
DEBUG = True

# ALLOWED_HOSTS
allowed_hosts = os.getenv("ALLOWED_HOSTS")
if allowed_hosts:
    ALLOWED_HOSTS += allowed_hosts.split(",")

# INSTALLED_APPS
INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

# Channels
if os.getenv("IN_MEMORY_CHANNEL_LAYER"):
    CHANNEL_LAYERS["default"] = {"BACKEND": "channels.layers.InMemoryChannelLayer"}

# Django debug toolbar
DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG}
