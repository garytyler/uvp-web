import uuid

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, status
from tortoise.transactions import in_transaction

from app.api.dependencies.publish import publish_feature
from app.models.guests import Guest
from app.schemas.guests import GuestCreate, GuestOut, GuestUpdate

router = APIRouter()


@router.post("/guests/current", response_model=GuestOut)
async def create_current_guest(
    request: Request,
    guest_in: GuestCreate,
    background_tasks: BackgroundTasks,
):
    if guest_id := request.session.get("guest_id"):
        if guest_obj := Guest.get_or_none(id=guest_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Guest already exists",
            )
    guest_obj = await Guest.create(**guest_in.dict(exclude_unset=True))
    request.session["guest_id"] = str(guest_obj.id)
    background_tasks.add_task(publish_feature, id=guest_obj.feature_id)
    return guest_obj


@router.get("/guests/current", response_model=GuestOut)
async def get_current_guest(request: Request):
    guest_id = request.session.get("guest_id")
    if not guest_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not (guest_obj := await Guest.get_or_none(id=guest_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await guest_obj.fetch_related("feature")
    return guest_obj


@router.patch("/guests/{guest_id}", response_model=GuestOut)
async def update_guest(
    background_tasks: BackgroundTasks,
    guest_id: uuid.UUID,
    guest_in: GuestUpdate,
):
    async with in_transaction():
        if not (guest_obj := await Guest.get_or_none(pk=guest_id)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        guest_in_data = guest_in.dict(exclude_unset=True)
        await guest_obj.update_from_dict(guest_in_data)
        await guest_obj.save(update_fields=guest_in_data.keys())
    background_tasks.add_task(publish_feature, id=guest_in.feature_id)
    return guest_obj


@router.get("/guests/{guest_id}", response_model=GuestOut)
async def get_guest(guest_id: str):
    if not (guest_obj := await Guest.get_or_none(id=uuid.UUID(guest_id))):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return guest_obj


# TODO: use a /features patch call to do this
@router.delete("/features/{feature_id}/guests/{guest_id}")
async def remove_guest_from_feature(
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
