from functools import lru_cache
from typing import Any, Dict, Optional, Set

from pydantic import AnyHttpUrl, AnyUrl, BaseSettings, PostgresDsn, SecretStr, validator


class Settings(BaseSettings):
    # Project
    PROJECT_TITLE: str
    PROJECT_DESCRIPTION: str

    # DNS
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl

    # Security
    SECRET_KEY: SecretStr
    ALLOWED_HOSTS: Set[str]
    BACKEND_CORS_ORIGINS: Set[str]
    HASH_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Mode
    DEBUG: bool = False

    # Database
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DATABASE_URL: Optional[str] = None

    @validator("DATABASE_URL", pre=True)
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgres",
            user=values.get("POSTGRES_USER", ""),
            password=values.get("POSTGRES_PASSWORD", ""),
            host=values.get("POSTGRES_HOST", ""),
            path=f"/{values.get('POSTGRES_DB', '').lstrip('/')}",
        )

    # Redis
    REDIS_URL: AnyUrl

    class Config:
        case_sensitive = True


@lru_cache
def get_settings():
    return Settings()
