from app.crud.base import CRUDBase
from app.models.guests import Guest
from app.schemas.guests import GuestCreateDb, GuestUpdateDb


class CRUDGuest(CRUDBase[Guest, GuestCreateDb, GuestUpdateDb]):
    pass


crud_guests = CRUDGuest(Guest)
