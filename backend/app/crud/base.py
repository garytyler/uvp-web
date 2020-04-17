import uuid
from typing import Generic, Optional, Type, TypeVar

from app.models.base import CustomTortoiseBase
from app.schemas.base import CustomPydanticBase
from fastapi.encoders import jsonable_encoder

ModelType = TypeVar("ModelType", bound=CustomTortoiseBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=CustomPydanticBase)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=CustomPydanticBase)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD)."""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(
        self, *, id: uuid.UUID, fetch_related: list = []
    ) -> Optional[ModelType]:
        obj = await self.model.filter(id=id).first()
        if obj and fetch_related:
            await obj.fetch_related(*fetch_related)
        return obj

    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data: dict = jsonable_encoder(obj_in)
        return await self.model.create(**obj_in_data)

    async def update(self, *, id: uuid.UUID, obj_in: UpdateSchemaType) -> ModelType:
        obj_in_data: dict = jsonable_encoder(obj_in)
        count_updated = await self.model.filter(id=id).update(**obj_in_data)
        return count_updated

    async def delete(self, *, id: uuid.UUID) -> int:
        deleted_count = await self.model.filter(id=id).delete()
        return deleted_count
