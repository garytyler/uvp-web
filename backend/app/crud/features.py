from typing import List, Optional

from app.crud.base import CRUDBase
from app.models.features import Feature
from app.schemas.features import FeatureCreate, FeatureUpdate


class CRUDFeature(CRUDBase[Feature, FeatureCreate, FeatureUpdate]):
    async def get_by_slug(self, slug: str) -> Optional[Feature]:
        return await self.model.filter(slug=slug).first()

    async def get_all(self) -> List[Feature]:
        return await self.model.all()


crud_feature = CRUDFeature(Feature)
