from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from tortoise.transactions import in_transaction

from app.api.dependencies.users import get_current_active_user
from app.core.security import get_password_hash
from app.models.users import User
from app.schemas.users import UserDbUpdate, UserInCreate, UserInUpdate, UserOut

router = APIRouter()


@router.get("/users/current", response_model=UserOut)
async def get_current_user(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/users", response_model=List[UserOut])  # type: ignore
async def get_users():
    return await User.all()


@router.patch("/users/current", response_model=UserOut)
async def update_current_user(
    user_in: UserInUpdate,
    current_user_obj: User = Depends(get_current_active_user),
):
    user_db = UserDbUpdate()
    if user_in.password is not None:
        user_db.hashed_password = get_password_hash(user_in.password)
    if user_in.email is not None:
        user_db.email = user_in.email
    if user_in.is_active is not None:
        user_db.is_active = user_in.is_active
    async with in_transaction():
        await current_user_obj.update_from_dict(user_db.dict(exclude_unset=True))
        await current_user_obj.save(
            update_fields=user_db.dict(exclude_unset=True).keys()
        )
    return current_user_obj


@router.get("/users/{id}", response_model=UserOut)
async def read_user_by_id(id: UUID):
    if not (user_obj := await User.get_or_none(id=id)):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User already exists",
        )
    return user_obj


@router.post("/users", response_model=UserOut)
async def create_new_user(user_in: UserInCreate):
    user_obj, created = await User.get_or_create(
        email=user_in.email,
        defaults=dict(
            hashed_password=get_password_hash(user_in.password),
            is_active=user_in.is_active,
        ),
    )
    if not created:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User already exists",
        )
    return user_obj
