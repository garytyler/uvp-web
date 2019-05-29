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


class LoggingFormatStringBuilder:
    def __init__(self, unicode, colored):

        self.unicode = unicode
        self.colored = colored
        self.string = ""

        if self.colored:
            self.string += "{log_color}"

    def __str__(self):
        return self

    def add_space(self):
        self.string += " "

    def add_time(self):
        if self.colored:
            self.string += "{reset_log_color}"

        self.string += "["

        if self.colored:
            self.string += "{dim_log_color}"

        self.string += "{asctime:}"

        if self.colored:
            self.string += "{reset_log_color}"

        self.string += "]"

    def add_level_name(self):
        if self.colored:
            self.string += "{emphasis_log_color}"

        if self.unicode:
            self.string += "{levelname:\u00B7<8}"
        else:
            self.string += "{levelname:.<8}"

    def add_prompt_symbol(self):
        if self.unicode:
            self.string += "{reset_log_color}\u276F"
        else:
            self.string += "{reset_log_color}>"

    def add_message(self):
        if self.colored:
            self.string += "{primary_log_color}{message}"
        else:
            self.string += "{message}"

    def add_line_number(self):
        if self.colored:
            self.string += "{dim_log_color}[{filename}:{lineno}]"
        else:
            self.string += "[{filename}:{lineno}]"


class LoggingColorProfiles:
    nocolor = {
        "DEBUG": "reset",
        "INFO": "reset",
        "WARNING": "reset",
        "ERROR": "reset",
        "CRITICAL": "reset",
    }
    applogger_primary = {
        "DEBUG": "reset,fg_cyan",
        "INFO": "reset,fg_green",
        "WARNING": "reset,fg_yellow",
        "ERROR": "reset,fg_red",
        "CRITICAL": "reset,fg_white,bg_red",
    }
    apploger_emphasis = {
        "DEBUG": "reset,fg_bold_cyan",
        "INFO": "reset,fg_bold_green",
        "WARNING": "reset,fg_bold_yellow",
        "ERROR": "reset,fg_red",
        "CRITICAL": "reset,fg_bold_white,bg_red",
    }
    dim_text = {
        "DEBUG": "reset,fg_bold_black",
        "INFO": "reset,fg_bold_black",
        "WARNING": "reset,fg_bold_black",
        "ERROR": "reset,fg_bold_black",
        "CRITICAL": "reset,fg_bold_black",
    }
    liblogger_primary = {
        "DEBUG": "reset,thin_cyan",
        "INFO": "reset,thin_green",
        "WARNING": "reset,thin_yellow",
        "ERROR": "reset,thin_red",
        "CRITICAL": "reset,fg_bold_white,bg_bold_red",
    }


def create_format_string(unicode, colored):
    builder = LoggingFormatStringBuilder(unicode, colored)
    builder.add_time()
    builder.add_level_name()
    builder.add_prompt_symbol()
    builder.add_message()
    builder.add_space()
    builder.add_line_number()
    return builder.string


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored_applogger": {
            "()": "colorlog.ColoredFormatter",
            "style": "{",
            "format": create_format_string(unicode=True, colored=True),
            "log_colors": LoggingColorProfiles.applogger_primary,
            "secondary_log_colors": {
                "primary": LoggingColorProfiles.applogger_primary,
                "emphasis": LoggingColorProfiles.apploger_emphasis,
                "dim": LoggingColorProfiles.dim_text,
                "reset": LoggingColorProfiles.nocolor,
            },
        },
        "colored_liblogger": {
            "()": "colorlog.ColoredFormatter",
            "style": "{",
            "format": create_format_string(unicode=True, colored=True),
            "log_colors": LoggingColorProfiles.liblogger_primary,
            "secondary_log_colors": {
                "primary": LoggingColorProfiles.liblogger_primary,
                "emphasis": LoggingColorProfiles.liblogger_primary,
                "dim": LoggingColorProfiles.dim_text,
                "reset": LoggingColorProfiles.nocolor,
            },
        },
    },
    "handlers": {
        "colored_applogger_console": {
            "formatter": "colored_applogger",
            "class": "logging.StreamHandler",
        },
        "colored_liblogger_console": {
            "formatter": "colored_liblogger",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["colored_liblogger_console"],
            "level": os.getenv("LOG_LEVEL_DJANGO", "INFO"),
            # "propagate": True,
        },
        "eventvr": {
            "handlers": ["colored_applogger_console"],
            "level": os.getenv("LOG_LEVEL_EVENTVR", "INFO"),
            # "propagate": False,
        },
    },
}
