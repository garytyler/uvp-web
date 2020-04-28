import uuid
from typing import Optional

from app.core.redis import redis
from app.crud.features import crud_features
from app.models.features import Feature
from app.schemas.features import FeatureOut
from fastapi.encoders import jsonable_encoder


async def publish_feature_by_obj(feature_obj: Feature) -> int:
    await feature_obj.fetch_related("guests", "presenters")
    feature_out = await FeatureOut.from_tortoise_orm(feature_obj)
    data = {"action": "receiveCurrentFeature", "feature": jsonable_encoder(feature_out)}
    return await redis.publish_json(str(feature_obj.interactor_channel_name), data)


async def publish_feature(id: uuid.UUID) -> Optional[int]:
    feature_obj = await crud_features.get(id=id)
    if not feature_obj:
        print("Feature not found")  # TODO: Raise 404
        return None
    return await publish_feature_by_obj(feature_obj=feature_obj)
