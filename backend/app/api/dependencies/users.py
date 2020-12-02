from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from app.core.config import get_settings
from app.core.security import oauth2_scheme, verify_password
from app.models.users import User
from app.schemas.tokens import TokenData


async def authenticate_user(email: str, password: str):
    user = await User.get(email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            str(get_settings().SECRET_KEY),
            algorithms=[get_settings().HASH_ALGORITHM],
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = await User.get(email=token_data.username)

    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Current user is not active")
    return current_user


async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="Current user has insufficient privileges"
        )
    return current_user
