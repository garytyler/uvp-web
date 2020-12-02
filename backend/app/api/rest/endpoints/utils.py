from typing import Any

from fastapi import APIRouter, Depends
from pydantic import EmailStr

from app.api.dependencies.users import get_current_active_superuser
from app.models.users import User
from app.schemas.messages import Message
from app.utils.mail import send_test_email

router = APIRouter()


@router.post("/utils/send-test-email", response_model=Message, status_code=201)
def test_email(
    email_to: EmailStr, current_user: User = Depends(get_current_active_superuser)
) -> Any:
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}
