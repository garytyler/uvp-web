""" Production Settings """
import os

import dj_database_url

from ._base import *  # noqa: F403,F401

# Domain name
ALLOWED_HOSTS: list = []


# Security
DEBUG = bool(os.getenv("DJANGO_DEBUG", ""))
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")


# Database
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=int(os.getenv("DATABASE_CONN_MAX_AGE", default=0)),
    )
}
