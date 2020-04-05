import uuid
from typing import List

from app.api.dependencies.features import validate_feature_slug
from app.crud.features import crud_feature
from app.schemas.features import FeatureCreate, FeatureOut
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.post("/features", response_model=FeatureOut)
async def create_feature(feature_in: FeatureCreate = Depends(validate_feature_slug)):
    feature = await crud_feature.create(obj_in=feature_in)
    if feature:
        await feature.fetch_related("guests")
    else:
        raise HTTPException(status_code=404, detail="Could not create item")
    return feature


@router.get("/features/{id_or_slug}", response_model=FeatureOut)
async def read_feature(id_or_slug: str):
    try:
        id_or_slug = uuid.UUID(id_or_slug, version=4)
    except ValueError:
        feature = await crud_feature.get_by_slug(slug=id_or_slug)
    else:
        feature = await crud_feature.get(id=id_or_slug)

    if feature:
        await feature.fetch_related("guests")
    else:
        raise HTTPException(status_code=404, detail="Could not create item")
    return feature


@router.get("/features", response_model=List[FeatureOut])
async def read_features():
    features = await crud_feature.get_all()
    for i in features:
        await i.fetch_related("guests")
    return features


@router.delete("/features/{id}", response_model=int)
async def delete_feature(id: str):
    deleted_count = await crud_feature.delete(id=id)
    if not deleted_count:
        raise HTTPException(status_code=404, detail="Item not found")
    return deleted_count
