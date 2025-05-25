from __future__ import annotations

from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import ForeignKey, Integer, Numeric, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import BaseModel

if TYPE_CHECKING:
    from app.api.models import Ingredient
    from app.api.models import User
    from app.api.models import MealIngredient, MealLog


class Meal(BaseModel):
    __tablename__ = "meals"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    picture: Mapped[str | None] = mapped_column(String(100))

    ingredients: Mapped[list["MealIngredient"]] = relationship(
        "MealIngredient", back_populates="meal", cascade="all, delete-orphan"
    )
    logs: Mapped[list["MealLog"]] = relationship(
        "MealLog", back_populates="meal", cascade="all, delete-orphan"
    )

    # --- helpers
    def required_totals(self, portions: int = 1) -> dict[int, float]:
        return {mi.ingredient_id: mi.required_qty * portions for mi in self.ingredients}

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "picture": self.picture,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class MealIngredient(BaseModel):
    __tablename__ = "meal_ingredients"

    meal_id: Mapped[int] = mapped_column(
        ForeignKey("meals.id", ondelete="CASCADE"), nullable=False
    )
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id"), nullable=False
    )

    required_qty: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    meal: Mapped["Meal"] = relationship("Meal", back_populates="ingredients")
    ingredient: Mapped["Ingredient"] = relationship(
        "Ingredient", back_populates="meal_ingredients"
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "meal_id": self.meal_id,
            "ingredient_id": self.ingredient_id,
            "required_qty": self.required_qty,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class MealLog(BaseModel):
    __tablename__ = "meal_logs"

    meal_id: Mapped[int] = mapped_column(ForeignKey("meals.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    portion_qty: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    served_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )

    meal: Mapped["Meal"] = relationship("Meal", back_populates="logs")
    user: Mapped["User"] = relationship("User", back_populates="meal_logs")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "meal_id": self.meal_id,
            "user_id": self.user_id,
            "portion_qty": self.portion_qty,
            "served_at": self.served_at.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
