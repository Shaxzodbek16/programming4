from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import BaseModel

if TYPE_CHECKING:
    from app.api.models import Ingredient


class Alert(BaseModel):
    __tablename__ = "alerts"

    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id", ondelete="CASCADE"), nullable=False
    )
    ingredient: Mapped["Ingredient"] = relationship(
        "Ingredient", back_populates="alerts"
    )

    alert_type: Mapped[str] = mapped_column(String(30), nullable=False)
    message: Mapped[str] = mapped_column(String(255), nullable=False)
    is_resolved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime)

    def resolve(self) -> "Alert":
        self.is_resolved = True
        self.resolved_at = datetime.utcnow()
        return self

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "ingredient_id": self.ingredient_id,
            "alert_type": self.alert_type,
            "message": self.message,
            "is_resolved": self.is_resolved,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
