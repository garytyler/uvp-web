import pytest
from async_asgi_testclient import TestClient

from app.schemas.features import FeatureOut


@pytest.mark.asyncio
async def test_schemas_feature_out_guests(
    app, create_random_feature_obj, create_random_guest_obj
):
    async with TestClient(app):
        feature = await create_random_feature_obj()
        for _ in range(3):
            await create_random_guest_obj(feature)
        await feature.fetch_related("guests", "presenters")
        feature_out = FeatureOut.from_orm(feature)
        feature_guests_ids = [i.id for i in feature.guests]
        feature_out_guests_ids = [i["id"] for i in feature_out.dict()["guests"]]
        assert feature_guests_ids == feature_out_guests_ids
