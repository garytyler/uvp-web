import uuid

from app.api.dependencies.publish import publish_feature_by_id
from app.crud.guests import crud_guests
from app.models.guests import Guest
from app.schemas.guests import GuestCreateDb, GuestCreateIn, GuestOut, GuestUpdateDb
from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, status

router = APIRouter()


@router.post("/features/{feature_id}/guests/current", response_model=GuestOut)
async def post_current_guest(
    request: Request, feature_id: str, guest_in: GuestCreateIn
):
    guest_id = request.session.get("guest_id")
    if guest_id and await crud_guests.get(id=guest_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Guest already exists",
        )
    guest_db = GuestCreateDb(name=guest_in.name, feature_id=uuid.UUID(feature_id))
    guest = await crud_guests.create(obj_in=guest_db)
    request.session["guest_id"] = str(guest.id)
    return guest


@router.put("/features/{feature_id}/guests/current", response_model=GuestOut)
async def put_current_guest(
    request: Request,
    background_tasks: BackgroundTasks,
    feature_id: uuid.UUID,
    guest_in: GuestCreateIn,
):
    guest_id = request.session.get("guest_id")
    if guest_id and await crud_guests.get(id=guest_id):
        guest_update_db = GuestUpdateDb(name=guest_in.name, feature_id=feature_id)
        guest = await crud_guests.update(id=guest_id, obj_in=guest_update_db)
    else:
        guest_create_db = GuestCreateDb(name=guest_in.name, feature_id=feature_id)
        guest = await crud_guests.create(obj_in=guest_create_db)
    request.session["guest_id"] = str(guest.id)
    background_tasks.add_task(publish_feature_by_id, id=feature_id)
    return guest


@router.get("/guests/current", response_model=GuestOut)
async def get_current_guest(request: Request):
    guest_id = request.session.get("guest_id")
    if not guest_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    guest = await crud_guests.get(id=guest_id)
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
    background_tasks.add_task(publish_feature_by_id, id=feature_id)
    return deleted_count
