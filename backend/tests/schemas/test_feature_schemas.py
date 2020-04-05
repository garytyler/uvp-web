import pytest
from app.schemas.features import FeatureOut
from async_asgi_testclient import TestClient
from tests._utils.features import create_random_feature
from tests._utils.guests import create_random_guest


@pytest.mark.asyncio
async def test_schemas_feature_out_guests(app):
    async with TestClient(app):
        feature = await create_random_feature()
        for _ in range(3):
            await create_random_guest(feature)
        await feature.fetch_related("guests")
        feature_out = FeatureOut.from_orm(feature)
        feature_guests_ids = [i.id for i in feature.guests]
        feature_out_guests_ids = [i["id"] for i in feature_out.dict()["guests"]]
        assert feature_guests_ids == feature_out_guests_ids
