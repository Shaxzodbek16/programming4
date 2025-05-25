from pydantic import BaseModel, Field, ConfigDict


class QueryList(BaseModel):
    search: str | None = None
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)

    model_config = ConfigDict(from_attributes=True)
