import os
from distutils.util import strtobool

import dj_database_url
from configurations import Configuration, values


class Common(Configuration):

    # Build paths inside the seevr like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PROJECT_DIR = os.path.join(BASE_DIR, "seevr")

    # Quick-start development settings - unsuitable for production

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.SecretValue()

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(False)

    # Allowed hosts
    ALLOWED_HOSTS = values.ListValue([])

    # Application definition
    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "whitenoise.runserver_nostatic",
        "django.contrib.staticfiles",
        "rest_framework",
        "channels",
        "beatserver",
        "webpack_loader",
        "seevr.accounts",
        "seevr.live",
    ]

    MIDDLEWARE = [
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "seevr.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [os.path.join(PROJECT_DIR, "templates")],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ]
            },
        }
    ]

    WSGI_APPLICATION = "seevr.wsgi.application"

    # Database
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=int(os.getenv("CONN_MAX_AGE", default=0))
        )
    }
    # DATABASES = {
    #     "default": {
    #         "ENGINE": "django.db.backends.sqlite3",
    #         "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    #     }
    # }

    # Password validation
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        },
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]

    # Internationalization

    LANGUAGE_CODE = "en-us"

    TIME_ZONE = "UTC"

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Caching
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": os.environ.get("REDIS_URL", "redis://localhost:6379/0"),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
            },
        }
    }

    # User data
    AUTH_USER_MODEL = "accounts.User"
    # SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

    # # Channels
    ASGI_APPLICATION = "seevr.routing.application"
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [os.environ.get("REDIS_URL", "redis://localhost:6379/0")]
            },
        }
    }

    # Logging
    LOGGING = {
        "version": 1,
        "loggers": {"django": {"level": os.getenv("LOG_LEVEL_DJANGO", "INFO")}},
    }

    # django-webpack-loader
    WEBPACK_LOADER = {
        "DEFAULT": {
            "CACHE": not DEBUG,
            "BUNDLE_DIR_NAME": "dist/",
            "STATS_FILE": os.path.join(BASE_DIR, "frontend", "webpack-stats.json"),
        }
    }

    # Static files (CSS, JavaScript, Images)
    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    STATICFILES_DIRS = (os.path.join(PROJECT_DIR, "static"),)

    # Live application settings
    GUEST_STATUS_PING_TIMEOUT = int(os.environ.get("GUEST_STATUS_PING_TIMEOUT", 3))
    GUEST_STATUS_CHECK_INTERVAL = int(os.environ.get("GUEST_STATUS_CHECK_INTERVAL", 4))
    USE_THREAD_BASED_FEATURE_OBSERVERS = strtobool(
        os.environ.get("USE_THREAD_BASED_FEATURE_OBSERVERS", "False")
    )

    # LOGIN_URL = "/accounts/login/"


class Production(Common):
    pass


class Development(Common):
    """
    The in-development settings and the default configuration.
    """

    DEBUG = True

    ALLOWED_HOSTS: list = []

    INTERNAL_IPS = ["127.0.0.1"]

    # Template debugging
    # Requires current host in INTERNAL_IPS
    TEMPLATE_DEBUG = True

    # Channels
    CHANNEL_LAYERS = Common.CHANNEL_LAYERS
    if os.getenv("IN_MEMORY_CHANNEL_LAYER"):
        CHANNEL_LAYERS["default"] = {"BACKEND": "channels.layers.InMemoryChannelLayer"}

    # Expire sessions at browser close
    SESSION_EXPIRE_AT_BROWSER_CLOSE = strtobool(
        os.getenv("SESSION_EXPIRE_AT_BROWSER_CLOSE", "False")
    )
