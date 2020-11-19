from fastapi import APIRouter

from app.core.security import get_password_hash
from app.models.users import User
from app.schemas.users import UserCreate, UserIn, UserOut

router = APIRouter()


@router.post("/users", response_model=UserOut)
async def create_new_user(user_in: UserIn):
    user_create = UserCreate(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
    )
    user_obj = await User.create(**user_create.dict())
    return user_obj
