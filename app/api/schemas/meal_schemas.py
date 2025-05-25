from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class MealIngredientBase(BaseModel):
    meal_id: int
    ingredient_id: int
    required_qty: float = Field(..., ge=0.01, le=10000.0)


class MealIngredientCreateSchema(MealIngredientBase):
    model_config = ConfigDict(from_attributes=True)


class MealIngredientReadSchema(MealIngredientBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MealIngredientUpdateSchema(BaseModel):
    required_qty: float | None = Field(None, ge=0.01, le=10000.0)
    meal_id: int | None = None
    ingredient_id: int | None = None


class MealListQuery(BaseModel):
    search: str | None = None
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)

    model_config = ConfigDict(from_attributes=True)


class MealIngredientListSchema(BaseModel):
    total: int
    page: int
    size: int
    search: str | None = None
    items: list[MealIngredientReadSchema]

    model_config = ConfigDict(from_attributes=True)


class MealBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    picture: str | None = Field(None, max_length=255)


class MealCreateSchema(MealBase):
    model_config = ConfigDict(from_attributes=True)


class MealReadSchema(MealBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MealUpdateSchema(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    picture: str | None = Field(None, max_length=255)


class MealListSchema(BaseModel):
    total: int
    page: int
    size: int
    search: str | None = None
    items: list[MealReadSchema]

    model_config = ConfigDict(from_attributes=True)


class MealLogBase(BaseModel):
    meal_id: int
    user_id: int
    portion_qty: int = Field(1, ge=1)
    served_at: datetime


class MealLogCreateSchema(MealLogBase):
    model_config = ConfigDict(from_attributes=True)


class MealLogReadSchema(MealLogBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MealLogUpdateSchema(BaseModel):
    portion_qty: int | None = Field(None, ge=1)
    meal_id: int | None = None


class MealLogListSchema(BaseModel):
    total: int
    page: int
    size: int
    search: str | None = None
    items: list[MealLogReadSchema]

    model_config = ConfigDict(from_attributes=True)
