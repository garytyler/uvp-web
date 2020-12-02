from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Optional, Set

from pydantic import (
    AnyHttpUrl,
    AnyUrl,
    BaseSettings,
    EmailStr,
    PostgresDsn,
    SecretStr,
    validator,
)


class Settings(BaseSettings):
    class Config:
        case_sensitive = True

    BASE_DIR: Path = Path(__file__).parent.parent.parent

    # Project
    PROJECT_NAME: str
    PROJECT_DESCRIPTION: str

    # DNS
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl

    # Security
    SECRET_KEY: SecretStr
    ALLOWED_HOSTS: Set[str]
    BACKEND_CORS_ORIGINS: Set[str]
    HASH_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 360

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

    # Email
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAIL_PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 24
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("SMTP_USER")
            and values.get("SMTP_PASSWORD")
            and values.get("EMAILS_FROM_EMAIL")
        )


@lru_cache
def get_settings():
    return Settings()
