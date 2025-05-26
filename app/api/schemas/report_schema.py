from pydantic import BaseModel, Field
from datetime import datetime


class PortionByDay(BaseModel):
    date: datetime
    total_portions: int


class PortionByMonth(BaseModel):
    year: int
    month: int
    total_portions: int | None = None


class PortionByYear(BaseModel):
    year: int
    total_portions: int


class MealLogPortionStats(BaseModel):
    daily: list[PortionByDay] = Field(default_factory=list)
    monthly: list[PortionByMonth] = Field(default_factory=list)
    yearly: list[PortionByYear] = Field(default_factory=list)


class MealLogQueryParams(BaseModel):
    year: int = Field(..., ge=1, description="Year to summarize")
    month: int = Field(1, ge=1, le=12, description="Month to summarize (optional)")
