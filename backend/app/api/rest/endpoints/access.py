from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies.users import authenticate_user
from app.core.security import (
    create_access_token,
    generate_password_reset_token,
    get_password_hash,
    verify_password_reset_token,
)
from app.schemas.messages import Message
from app.schemas.tokens import TokenOut
from app.schemas.users import User
from app.utils.mail import send_reset_password_email

router = APIRouter()


@router.post("/access/token", response_model=TokenOut)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(
        email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/access/request-password-recovery/{email}", response_model=Message)
async def request_password_recovery(email: str) -> Any:
    user_obj = await User.get_or_none(email=email)
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=user_obj.email,
        token=password_reset_token,
    )
    return {"msg": "Password recovery email sent"}


@router.post("/access/reset-password", response_model=Message)
async def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
) -> Any:
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user_obj = await User.get_or_none(email=email)
    if not user_obj:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not user_obj.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    user_obj.hashed_password = get_password_hash(new_password)
    await user_obj.save()
    # await user_obj.save(update_fields=["hashed_password"])
    return {"msg": "Password updated successfully"}
