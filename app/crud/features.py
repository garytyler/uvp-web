from app.crud.base import CRUDBase
from app.models.features import Feature
from app.schemas.features import FeatureCreate, FeatureUpdate


class CRUDFeature(CRUDBase[Feature, FeatureCreate, FeatureUpdate]):
    pass


crud_feature = CRUDFeature(Feature)
