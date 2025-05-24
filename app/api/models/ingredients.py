from __future__ import annotations

from typing import TYPE_CHECKING

from datetime import datetime
from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import BaseModel

if TYPE_CHECKING:
    from app.api.models import Unit
    from app.api.models import IngredientTransaction
    from app.api.models import MealIngredient
    from app.api.models import Alert


class Ingredient(BaseModel):
    __tablename__ = "ingredients"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"), nullable=False)
    unit: Mapped["Unit"] = relationship("Unit", back_populates="ingredients")

    quantity: Mapped[float] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    min_threshold: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    # --- relationships
    transactions: Mapped[list["IngredientTransaction"]] = relationship(
        "IngredientTransaction",
        back_populates="ingredient",
        cascade="all, delete-orphan",
    )
    meal_ingredients: Mapped[list["MealIngredient"]] = relationship(
        "MealIngredient", back_populates="ingredient"
    )
    alerts: Mapped[list["Alert"]] = relationship(
        "Alert", back_populates="ingredient", cascade="all, delete-orphan"
    )

    def update(self, **kwargs) -> "Ingredient":
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        setattr(self, "updated_at", datetime.now())
        return self

    @property
    def is_low_stock(self) -> bool:
        return self.quantity <= self.min_threshold

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "unit_id": self.unit_id,
            "quantity": str(self.quantity),
            "min_threshold": str(self.min_threshold),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
