from datetime import datetime, timedelta
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from app.core.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/access/token")


def create_access_token(data: dict = {}):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        str(get_settings().SECRET_KEY),
        algorithm=get_settings().HASH_ALGORITHM,
    )
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def generate_password_reset_token(email: str) -> str:
    settings = get_settings()
    delta = timedelta(hours=settings.EMAIL_PASSWORD_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email, "email": email},
        key=str(settings.SECRET_KEY),
        algorithm=settings.HASH_ALGORITHM,
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    settings = get_settings()
    try:
        decoded_token = jwt.decode(
            token, str(settings.SECRET_KEY), algorithms=[settings.HASH_ALGORITHM]
        )
        return decoded_token["email"]
    except jwt.JWTError:
        return None
