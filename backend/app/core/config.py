from typing import Set

from pydantic import AnyUrl, BaseSettings, SecretStr


class Settings(BaseSettings):
    DEBUG: bool = False

    # Security
    SECRET_KEY: SecretStr
    ALLOWED_HOSTS: Set[str]
    HTTPS_REDIRECT: bool = True
    BACKEND_CORS_ORIGINS: Set[str]

    # Database
    DATABASE_URL: str

    # Caching
    REDIS_URL: AnyUrl

    # Tortoise
    TORTOISE_MODEL_MODULES: Set[str] = {
        "app.models.features",
        "app.models.guests",
        "app.models.presenters",
    }

    class Config:
        case_sensitive = True


settings = Settings()
