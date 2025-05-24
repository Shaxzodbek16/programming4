from pydantic import BaseModel, Field, ConfigDict


class IngredientBaseSchema(BaseModel):
    name: str = Field(..., max_length=100)
    unit_id: int
    quantity: float = Field(0, ge=0)
    min_threshold: float = Field(0, ge=0)

    model_config = ConfigDict(from_attributes=True)


class IngredientCreateSchema(IngredientBaseSchema):
    pass


class IngredientUpdateSchema(BaseModel):
    name: str | None = Field(None, max_length=100)
    unit_id: int | None
    quantity: float | None = Field(None, ge=0)
    min_threshold: float | None = Field(None, ge=0)

    model_config = ConfigDict(from_attributes=True)


class IngredientReadSchema(IngredientBaseSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class IngredientListQuery(BaseModel):
    search: str | None = None
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)

    model_config = ConfigDict(from_attributes=True)


class IngredientListSchema(BaseModel):
    total: int
    page: int
    size: int
    items: list[IngredientReadSchema]

    search: str | None = None

    model_config = ConfigDict(from_attributes=True)
