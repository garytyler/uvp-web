import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from tortoise.transactions import in_transaction

from app.api.dependencies.features import validate_feature_slug
from app.api.dependencies.users import get_current_active_user
from app.models.features import Feature
from app.models.users import User
from app.schemas.features import FeatureCreate, FeatureOut

router = APIRouter()


@router.post(
    "/features",
    response_model=FeatureOut,
)
async def create_feature(
    feature_in: FeatureCreate = Depends(validate_feature_slug),
    current_active_user: User = Depends(get_current_active_user),
):

    if feature_obj := await Feature.create(**feature_in.dict()):
        await feature_obj.fetch_related("guests", "presenters")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return feature_obj


@router.get("/features/{id_or_slug}", response_model=FeatureOut)
async def get_feature_single(id_or_slug: str):
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


@router.get(
    "/features", response_model=List, dependencies=[Depends(get_current_active_user)]
)
async def get_feature_list(
    user_id: Optional[uuid.UUID] = None,
):
    search_kwargs = {}
    if user_id:
        search_kwargs["user_id"] = user_id
    feature_objs = await Feature.filter(**search_kwargs)
    if not feature_objs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return list(feature_objs)


@router.delete(
    "/features/{id}",
    response_model=int,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_feature(id: uuid.UUID):
    deleted_count = await Feature.filter(id=id).delete()
    if not deleted_count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return deleted_count
