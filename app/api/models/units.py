from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.core.models.base import BaseModel

if TYPE_CHECKING:
    from app.api.models import Ingredient


class Unit(BaseModel):
    __tablename__ = "units"

    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(50), nullable=True)

    ingredients: Mapped[list["Ingredient"]] = relationship(
        "Ingredient", back_populates="unit", cascade="all, delete"
    )

    def to_dict(self) -> dict[str, str | None]:
        return {
            "id": self.id,
            "code": self.code,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def update(self, **kwargs) -> "Unit":
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        setattr(self, "updated_at", datetime.now())
        return self
