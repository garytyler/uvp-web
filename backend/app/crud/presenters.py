from app.crud.base import CRUDBase
from app.models.presenters import Presenter
from app.schemas.presenters import PresenterCreateDb, PresenterUpdateDb


class CRUDPresenter(CRUDBase[Presenter, PresenterCreateDb, PresenterUpdateDb]):
    async def create(self, obj_in=None) -> Presenter:
        return await super().create(obj_in=PresenterCreateDb())


crud_presenters = CRUDPresenter(Presenter)
