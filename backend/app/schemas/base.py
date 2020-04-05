from pydantic import BaseModel


class CustomPydanticBase(BaseModel):
    class Config:
        orm_mode = True
