from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class UnitBaseSchema(BaseModel):
    code: str = Field(..., max_length=10)
    description: str | None = Field(None, max_length=50)

    model_config = ConfigDict(from_attributes=True)


class UnitCreateSchema(UnitBaseSchema):
    pass


class UnitUpdateSchema(BaseModel):
    code: str | None = Field(None, max_length=10)
    description: str | None = Field(None, max_length=50)

    model_config = ConfigDict(from_attributes=True)


class UnitReadSchema(UnitBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
