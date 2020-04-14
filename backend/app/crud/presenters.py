from app.crud.base import CRUDBase
from app.models.presenters import Presenter
from app.schemas.presenters import PresenterCreate, PresenterUpdate


class CRUDPresenter(CRUDBase[Presenter, PresenterCreate, PresenterUpdate]):
    pass


crud_presenters = CRUDPresenter(Presenter)
