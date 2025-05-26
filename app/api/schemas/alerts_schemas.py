from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

from app.api.schemas.base import QueryList


class AlertBaseSchema(BaseModel):
    ingredient_id: int
    alert_type: str = Field(..., max_length=30)
    message: str
    resolved_at: datetime | None = None


class AlertCreateSchema(AlertBaseSchema):
    model_config = ConfigDict(from_attributes=True)


class AlertReadSchema(AlertBaseSchema):
    id: int
    is_resolved: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AlertsQuery(QueryList):
    is_resolved: bool | None = None
    model_config = ConfigDict(from_attributes=True)


class AlertListSchema(QueryList):
    total: int
    items: list[AlertReadSchema] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)
