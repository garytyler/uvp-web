from app.crud.base import CRUDBase
from app.models.guests import Guest
from app.schemas.guests import GuestCreate, GuestUpdate


class CRUDGuest(CRUDBase[Guest, GuestCreate, GuestUpdate]):
    pass


crud_guests = CRUDGuest(Guest)
