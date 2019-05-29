import logging
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


# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "[{asctime}] {levelname} {message}", "style": "{"},
        "verbose": {
            "format": "[{asctime}] {process:d} {thread:d} {levelname} [{module}:{lineno}] {message}",
            "style": "{",
        },
        "dev": {
            "format": "[{relativeCreated:.3f}] {levelname} {message} [{module}:{lineno}]",
            "style": "{",
        },
        "dev": {
            "format": "[{relativeCreated:.3f}] {levelname} {message} [{module}:{lineno}]",
            "style": "{",
        },
    },
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "dev"}},
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("LOG_LEVEL_DJANGO", "INFO"),
            "propagate": True,
        },
        "eventvr": {
            "handlers": ["console"],
            "level": os.getenv("LOG_LEVEL_EVENTVR", "INFO"),
            "propagate": False,
        },
    },
}


# Colored logging
try:
    import colorlog, copy
except ImportError:
    pass
else:
    LOGGING["loggers"]["eventvr"]["handlers"].remove("console")
    LOGGING["loggers"]["eventvr"]["handlers"].append("colored_console")
    LOGGING["handlers"]["colored_console"] = copy.copy(LOGGING["handlers"]["console"])
    LOGGING["handlers"]["colored_console"]["formatter"] = "colored_dev"
    LOGGING["formatters"]["colored_dev"] = copy.copy(LOGGING["formatters"]["dev"])
    LOGGING["formatters"]["colored_dev"]["()"] = "colorlog.ColoredFormatter"
    LOGGING["formatters"]["colored_dev"]["format"] = (
        "{log_color}" + LOGGING["formatters"]["dev"]["format"]
    )
