from fastapi import HTTPException
from fastapi.routing import APIRouter

from app.crud.features import crud_feature
from app.schemas.features import FeatureCreate, FeatureOut

router = APIRouter()


@router.post("/features", response_model=FeatureOut)
async def create_feature(feature_in: FeatureCreate):
    feature = await crud_feature.create(obj_in=feature_in)
    if feature:
        await feature.fetch_related("guests")
    else:
        raise HTTPException(status_code=404, detail="Could not create item")
    return feature


@router.get("/features/{feature_id}", response_model=FeatureOut)
async def get_feature(feature_id: str):
    feature = await crud_feature.get(id=feature_id)
    if feature:
        await feature.fetch_related("guests")
    else:
        raise HTTPException(status_code=404, detail="Could not create item")
    return feature
