from fastapi import APIRouter, HTTPException, Request

from app.crud.guests import crud_guest
from app.schemas.guests import GuestCreate, GuestOut

router = APIRouter()


@router.post("/features/{feature_id}/guest", response_model=GuestOut)
async def create_current_guest(request: Request, guest_in: GuestCreate):
    guest_id = request.session.get("guest_id")
    if guest_id:
        raise HTTPException(status_code=400, detail="Guest already exists")
    else:
        guest = await crud_guest.create(obj_in=guest_in)
        request.session["guest_id"] = str(guest.id)
    return guest


@router.get("/guest", response_model=GuestOut)
async def get_current_guest(request: Request, guest_in: GuestCreate):
    guest_id = request.session.get("guest_id")
    if guest_id:
        raise HTTPException(status_code=400, detail="Guest already exists")
    else:
        guest = await crud_guest.create(obj_in=guest_in)
        request.session["guest_id"] = str(guest.id)
    return guest


@router.get("/guests/{guest_id}", response_model=GuestOut)
async def get_feature(guest_id: str):
    guest = await crud_guest.get(id=guest_id)
    return guest
