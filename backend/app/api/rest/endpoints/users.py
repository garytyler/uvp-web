from typing import List
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic import EmailStr
from tortoise.transactions import in_transaction

from app.api.dependencies.users import get_current_active_user
from app.core.security import get_password_hash
from app.models.users import User
from app.schemas.users import UserCreate, UserIn, UserOut, UserUpdate

router = APIRouter()


@router.get("/users/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/users", response_model=List[UserOut])  # type: ignore
async def read_users():
    return await User.all()


@router.get("/users/{id}", response_model=UserOut)
async def read_user_by_id(id: UUID):
    if not (user_obj := await User.get_or_none(id=id)):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User already exists",
        )
    return user_obj


@router.patch("/users/me", response_model=UserOut)
async def update_user_me(
    password: str = Body(...),
    email: EmailStr = Body(...),
):
    user_update = UserUpdate()
    if password is not None:
        user_update.hashed_password = get_password_hash(password)
    if email is not None:
        user_update.email = email
    async with in_transaction():
        if not (user_obj := await User.get_or_none(pk=id)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        await user_obj.update_from_dict(user_update.dict(exclude_unset=True))
        await user_obj.save(update_fields=user_update.dict(exclude_unset=True).keys())
    return user_obj


@router.post("/users", response_model=UserOut)
async def create_new_user(user_in: UserIn):
    user_create = UserCreate(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
    )
    user_obj, created = await User.get_or_create(**user_create.dict())
    if not created:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User already exists",
        )
    return user_obj
