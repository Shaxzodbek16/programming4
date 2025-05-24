from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import BaseModel

if TYPE_CHECKING:
    from app.api.models import Ingredient


class IngredientTransaction(BaseModel):
    __tablename__ = "ingredient_transactions"

    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id", ondelete="CASCADE"), nullable=False
    )
    ingredient: Mapped["Ingredient"] = relationship(
        "Ingredient", back_populates="transactions"
    )

    quantity: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    transaction_type: Mapped[str] = mapped_column(String(10), nullable=False)  # IN/OUT
    reference_id: Mapped[int | None] = mapped_column(Integer)
    note: Mapped[str | None] = mapped_column(String(255))

    happened_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "ingredient_id": self.ingredient_id,
            "quantity": str(self.quantity),
            "transaction_type": self.transaction_type,
            "reference_id": self.reference_id,
            "note": self.note,
            "happened_at": self.happened_at.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
