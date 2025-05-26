from __future__ import annotations

from datetime import datetime, UTC, timedelta
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, DateTime, ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import BaseModel

if TYPE_CHECKING:
    from app.api.models import MealLog
    from app.api.models import UserOTP


class Role(BaseModel):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    users: Mapped[list["User"]] = relationship("User", back_populates="role")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class User(BaseModel):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    profile_picture: Mapped[str | None] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"), nullable=False, default=4
    )
    role: Mapped["Role"] = relationship("Role", back_populates="users")

    # outbound relationships
    otp_codes: Mapped[list["UserOTP"]] = relationship(
        "UserOTP", back_populates="user", cascade="all, delete-orphan"
    )
    meal_logs: Mapped[list["MealLog"]] = relationship("MealLog", back_populates="user")

    # convenience
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def activate(self) -> "User":
        setattr(self, "is_active", True)
        return self

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "profile_picture": self.profile_picture,
            "email": self.email,
            "is_active": self.is_active,
            "role_id": self.role_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class UserOTP(BaseModel):
    __tablename__ = "user_otp"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    otp_code: Mapped[int] = mapped_column(BigInteger, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now() + timedelta(minutes=5)
    )

    user: Mapped["User"] = relationship("User", back_populates="otp_codes")

    # helpers
    def is_expired(self) -> bool:
        return datetime.now(UTC) >= self.expires_at

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "otp_code": self.otp_code,
            "expires_at": self.expires_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
