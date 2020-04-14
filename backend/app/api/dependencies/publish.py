import json
import uuid

from app.crud.features import crud_features
from app.models.features import Feature
from app.schemas.features import FeatureOut
from app.services.broadcasting import broadcast
from fastapi.encoders import jsonable_encoder


async def publish_feature_by_obj(obj: Feature) -> None:
    await obj.fetch_related("guests", "presenters")
    feature_out = await FeatureOut.from_tortoise_orm(obj)
    feature_out_json = jsonable_encoder(feature_out)
    data = {"action": "receiveFeature", "feature": feature_out_json}
    await broadcast.publish(channel=str(obj.guest_channel), message=json.dumps(data))


async def publish_feature_by_id(id: uuid.UUID) -> None:
    feature_obj = await crud_features.get(id=id)
    if not feature_obj:
        print("Feature not found")  # TODO: Raise 404
    else:
        await publish_feature_by_obj(obj=feature_obj)
