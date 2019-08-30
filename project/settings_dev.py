from os import getenv

if getenv("DJANGO_SETTINGS_MODULE", default="").endswith("dev"):
    from project.settings import *


# Debug
DEBUG = True


# Allowed hosts
ALLOWED_HOSTS = getenv("ALLOWED_HOSTS", default="").split(",")


# Template debugging
# Requires current host in INTERNAL_IPS
INTERNAL_IPS = getenv("INTERNAL_IPS")
TEMPLATE_DEBUG = True if INTERNAL_IPS else False


# Channels
CHANNEL_LAYERS = globals()["CHANNEL_LAYERS"]
if getenv("IN_MEMORY_CHANNEL_LAYER"):
    CHANNEL_LAYERS["default"] = {"BACKEND": "channels.layers.InMemoryChannelLayer"}


# Sessions
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Default is false


# Logging
log_color_styles = {
    "default": {
        "DEBUG": "reset,fg_cyan",
        "INFO": "reset,fg_green",
        "WARNING": "reset,fg_yellow",
        "ERROR": "reset,fg_red",
        "CRITICAL": "reset,fg_white,bg_red",
    },
    "strong": {
        "DEBUG": "reset,fg_bold_cyan",
        "INFO": "reset,fg_bold_green",
        "WARNING": "reset,fg_bold_yellow",
        "ERROR": "reset,fg_red",
        "CRITICAL": "reset,fg_bold_white,bg_red",
    },
    "dull": {
        "DEBUG": "reset,thin_cyan",
        "INFO": "reset,thin_green",
        "WARNING": "reset,thin_yellow",
        "ERROR": "reset,thin_red",
        "CRITICAL": "reset,fg_bold_white,bg_bold_red",
    },
    "dim": {
        "DEBUG": "reset,fg_bold_black",
        "INFO": "reset,fg_bold_black",
        "WARNING": "reset,fg_bold_black",
        "ERROR": "reset,fg_bold_black",
        "CRITICAL": "reset,fg_bold_black",
    },
    "uncolored": {
        "DEBUG": "reset",
        "INFO": "reset",
        "WARNING": "reset",
        "ERROR": "reset",
        "CRITICAL": "reset",
    },
}


log_format_string = "{log_color}{reset_log_color}[{dim_log_color}{asctime:}{reset_log_color}][{emphasis_log_color}{levelname}{reset_log_color}] {primary_log_color}{message}{dim_log_color} [{filename}:{lineno}({funcName})]{reset_log_color}"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored_applogs_formatter": {
            "()": "colorlog.ColoredFormatter",
            "style": "{",
            "format": log_format_string,
            "log_colors": log_color_styles["default"],
            "secondary_log_colors": {
                "primary": log_color_styles["default"],
                "emphasis": log_color_styles["strong"],
                "dim": log_color_styles["dim"],
                "reset": log_color_styles["uncolored"],
            },
        },
        "colored_liblogs_formatter": {
            "()": "colorlog.ColoredFormatter",
            "style": "{",
            "format": log_format_string,
            "log_colors": log_color_styles["dull"],
            "secondary_log_colors": {
                "primary": log_color_styles["dull"],
                "emphasis": log_color_styles["dull"],
                "dim": log_color_styles["dim"],
                "reset": log_color_styles["uncolored"],
            },
        },
    },
    "handlers": {
        "colored_console": {
            "formatter": "colored_applogs_formatter",
            "class": "logging.StreamHandler",
        }
    },
    "loggers": {
        "django": {
            "handlers": ["colored_console"],
            "level": getenv("LOG_LEVEL_DJANGO", "INFO"),
        },
        "eventvr": {
            "handlers": ["colored_console"],
            "level": getenv("LOG_LEVEL_EVENTVR", "INFO"),
        },
    },
}
