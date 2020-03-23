from fastapi import APIRouter

from app.services.broadcast import broadcast

router = APIRouter()


@router.post("/broadcast/{channel_name}/{message}")
async def broadcast_message(channel_name: str, message: str):
    print(channel_name, message)
    await broadcast.publish(channel="chatroom", message=message)
