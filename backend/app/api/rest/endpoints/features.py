import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from tortoise.transactions import in_transaction

from app.api.dependencies.features import validate_feature_slug
from app.models.features import Feature
from app.schemas.features import FeatureCreate, FeatureOut

router = APIRouter()


@router.post("/features", response_model=FeatureOut)
async def create_feature(feature_in: FeatureCreate = Depends(validate_feature_slug)):
    if feature_obj := await Feature.create(**feature_in.dict()):
        await feature_obj.fetch_related("guests", "presenters")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return feature_obj


@router.get("/features/{id_or_slug}", response_model=FeatureOut)
async def get_feature(id_or_slug: str):
    try:
        feature_id: uuid.UUID = uuid.UUID(id_or_slug, version=4)
    except ValueError:
        feature_obj = await Feature.get_or_none(slug=id_or_slug)
    else:
        feature_obj = await Feature.get_or_none(id=feature_id)

    if feature_obj:
        await feature_obj.fetch_related("guests", "presenters")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return feature_obj


@router.get("/features", response_model=List[FeatureOut])  # type: ignore
async def get_all_features():
    async with in_transaction():
        features = await Feature.all()
        for i in features:
            await i.fetch_related("guests", "presenters")
    return features


@router.delete("/features/{id}", response_model=int)
async def delete_feature(id: uuid.UUID):
    deleted_count = await Feature.filter(id=id).delete()
    if not deleted_count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return deleted_count
