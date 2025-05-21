from datetime import datetime

from sqlalchemy import Integer, DateTime, func
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )

    def update(self, **kwargs) -> "BaseModel":
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        setattr(self, "updated_at", datetime.now())
        return self

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id})>"

    def __str__(self):
        return f"<{self.__class__.__name__}"

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
