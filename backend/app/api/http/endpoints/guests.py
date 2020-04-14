import uuid

from app.api.dependencies.publish import publish_feature
from app.crud.guests import crud_guests
from app.models.guests import Guest
from app.schemas.guests import GuestCreate, GuestOut, GuestUpdate
from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, status

router = APIRouter()


@router.post("/guests/current", response_model=GuestOut)
async def post_current_guest(
    request: Request, guest_in: GuestCreate, background_tasks: BackgroundTasks,
):
    guest_id = request.session.get("guest_id")
    if guest_id and await crud_guests.get(id=guest_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Guest already exists",
        )
    guest = await crud_guests.create(obj_in=guest_in)
    background_tasks.add_task(publish_feature, id=guest.feature_id)
    request.session["guest_id"] = str(guest.id)
    return guest


@router.patch("/guests/{guest_id}", response_model=GuestOut)
async def update_current_guest(
    request: Request,
    background_tasks: BackgroundTasks,
    guest_id: uuid.UUID,
    guest_in: GuestUpdate,
):
    count_updated = await crud_guests.update(id=guest_id, obj_in=guest_in)
    if not count_updated:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED)
    background_tasks.add_task(publish_feature, id=guest_in.feature_id)
    return await crud_guests.get(id=guest_id)


@router.get("/guests/current", response_model=GuestOut)
async def get_current_guest(request: Request):
    guest_id = request.session.get("guest_id")
    if not guest_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    guest = await crud_guests.get(id=guest_id)
    if not guest:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await guest.fetch_related("feature")
    return guest


@router.get("/guests/{guest_id}", response_model=GuestOut)
async def get_guest(guest_id: str):
    guest = await crud_guests.get(id=uuid.UUID(guest_id))
    return guest


@router.delete("/features/{feature_id}/guests/{guest_id}")
async def delete_guest(
    request: Request,
    background_tasks: BackgroundTasks,
    feature_id=uuid.UUID,
    guest_id=uuid.UUID,
):
    guest = await Guest.filter(id=guest_id, feature_id=feature_id).first()
    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Guest not found"
        )
    deleted_count = await guest.delete()
    if str(guest_id) == request.session.get("guest_id"):
        del request.session["guest_id"]
    background_tasks.add_task(publish_feature, id=feature_id)
    return deleted_count
