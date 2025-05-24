from __future__ import annotations


from sqlalchemy import Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import BaseModel


class Report(BaseModel):
    __tablename__ = "reports"

    report_month: Mapped[int] = mapped_column(Integer, nullable=False)
    report_year: Mapped[int] = mapped_column(Integer, nullable=False)
    total_served_portions: Mapped[int] = mapped_column(Integer, nullable=False)
    possible_served_portions: Mapped[int] = mapped_column(Integer, nullable=False)
    difference_percentage: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "report_month": self.report_month,
            "report_year": self.report_year,
            "total_served_portions": self.total_served_portions,
            "possible_served_portions": self.possible_served_portions,
            "difference_percentage": str(self.difference_percentage),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
