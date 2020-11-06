import uuid
from typing import Optional

from fastapi.encoders import jsonable_encoder

from app.core.redis import redis
from app.models.features import Feature
from app.schemas.features import FeatureOut


async def publish_feature_by_obj(feature_obj: Feature) -> int:
    await feature_obj.fetch_related("guests", "presenters")
    feature_out = await FeatureOut.from_tortoise_orm(feature_obj)
    data = {"action": "receiveCurrentFeature", "feature": jsonable_encoder(feature_out)}
    return await redis.publish_json(str(feature_obj.interactor_channel_name), data)


async def publish_feature(id: uuid.UUID) -> Optional[int]:
    if not (feature_obj := await Feature.get_or_none(id=id)):
        # TODO: use an exception handler to log a 404 Feature not found
        return None
    return await publish_feature_by_obj(feature_obj=feature_obj)
