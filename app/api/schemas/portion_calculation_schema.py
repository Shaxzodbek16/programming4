from pydantic import BaseModel, ConfigDict, Field
from app.api.schemas.base import QueryList
from app.api.schemas.meal_schemas import MealReadSchema


class PortionCalculationReadSchema(BaseModel):
    meal: MealReadSchema
    portion_count: int = Field(..., ge=0)
    model_config = ConfigDict(from_attributes=True)


class PortionCalculationListSchema(QueryList):
    items: list[PortionCalculationReadSchema]
    model_config = ConfigDict(from_attributes=True)
