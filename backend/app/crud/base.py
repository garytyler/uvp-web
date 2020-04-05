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

    async def get(self, id: uuid.UUID) -> Optional[ModelType]:
        return await self.model.filter(id=id).first()

    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        return await self.model.create(**obj_in_data)

    async def update(self, *, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(skip_defaults=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_obj = await self.model.create(**obj_data)
        return db_obj

    async def delete(self, *, id: uuid.UUID) -> ModelType:
        deleted_count = await self.model.filter(id=id).delete()
        return deleted_count
