from typing import Generic, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder

from app.models.base import CustomTortoiseBase
from app.schemas.base import CustomPydanticBase

ModelType = TypeVar("ModelType", bound=CustomTortoiseBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=CustomPydanticBase)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=CustomPydanticBase)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD)."""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, id: str) -> Optional[ModelType]:
        return await self.model.filter(id=id).first()

    # async def get_multi(self, *, skip=0, limit=100) -> List[ModelType]:
    #     return await self.model.offset(skip).limit(limit).all()

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

    # async def remove(self, *, id: int) -> ModelType:
    #     obj = await self.model.get(id)
    #     await self.model.delete(obj)
    #     return obj
