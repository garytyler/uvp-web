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
in_memory = {"BACKEND": "channels.layers.InMemoryChannelLayer"}
local_redis = {
    "BACKEND": "channels_redis.core.RedisChannelLayer",
    # "CONFIG": {"hosts": [("localhost", 6379)]},
    "CONFIG": {"hosts": [os.environ.get("REDIS_URL", "redis://localhost:6379")]},
}
CHANNEL_LAYERS["default"] = local_redis if os.getenv("USE_REDIS") else in_memory

# Django debug toolbar
DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG}
