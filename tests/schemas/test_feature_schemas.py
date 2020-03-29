import pytest
from async_asgi_testclient import TestClient

from app.models.features import Feature
from app.schemas.features import FeatureCreate, FeatureOut
from tests._utils.features import create_random_feature
from tests._utils.guests import create_random_guest
from tests._utils.strings import create_random_string


@pytest.mark.asyncio
async def test_schemas_feature_create_autogenerates_slug(app):
    async with TestClient(app):
        title = create_random_string(
            min_length=5,
            max_length=20,
            min_words=2,
            max_words=6,
            uppercase_letters=True,
            lowercase_letters=True,
            numbers=True,
        )
        feature_in = FeatureCreate(title=title)
        feature = await Feature.create(**feature_in.dict())
        assert feature.title == title
        assert len(feature.slug)
        assert len(feature.slug.split()) == 1
        assert len(feature.slug.split()) < len(title.split())


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
