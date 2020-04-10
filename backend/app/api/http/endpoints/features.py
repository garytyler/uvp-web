import uuid
from typing import List

from app.api.dependencies.features import validate_feature_slug
from app.crud.features import crud_features
from app.schemas.features import FeatureCreate, FeatureOut
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.post("/features", response_model=FeatureOut)
async def create_feature(feature_in: FeatureCreate = Depends(validate_feature_slug)):
    feature = await crud_features.create(obj_in=feature_in)
    if feature:
        await feature.fetch_related("guests", "presenters")
    else:
        raise HTTPException(status_code=404, detail="Could not create item")
    return feature


@router.get("/features/{id_or_slug}", response_model=FeatureOut)
async def get_feature(id_or_slug: str):
    try:
        feature_uuid: uuid.UUID = uuid.UUID(id_or_slug, version=4)
    except ValueError:
        feature = await crud_features.get_by_slug(slug=id_or_slug)  # type: ignore
    else:
        feature = await crud_features.get(id=feature_uuid)  # type: ignore

    if feature:
        await feature.fetch_related("guests", "presenters")
    else:
        raise HTTPException(status_code=404, detail="Could not create item")
    return feature


@router.get("/features", response_model=List[FeatureOut])
async def get_all_features():
    features = await crud_features.get_all()
    for i in features:
        await i.fetch_related("guests", "presenters")
    return features


@router.delete("/features/{id}", response_model=int)
async def delete_feature(id: uuid.UUID):
    deleted_count = await crud_features.delete(id=id)
    if not deleted_count:
        raise HTTPException(status_code=404, detail="Item not found")
    return deleted_count
