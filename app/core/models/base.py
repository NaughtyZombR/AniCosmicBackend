from datetime import datetime

from core.common.formatters import to_snake_case
from database import Base
from sqlalchemy import DateTime, func, text
from sqlalchemy.orm import Mapped, declared_attr, mapped_column


class BaseModel(Base):
    __abstract__ = True

    _repr_cols_num = 3
    _repr_cols = tuple()

    @declared_attr.directive
    def __tablename__(cls) -> str:  # noqa
        """Переводит название класса в snake_case того же числа (единичного,
        множественного), что и имя класса"""
        return to_snake_case(cls.__name__)

    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к
        неожиданным подгрузкам"""
        columns = []
        for index, column in enumerate(self.__table__.columns.keys()):
            if column in self._repr_cols or index < self._repr_cols_num:
                columns.append(f"{column}={getattr(self, column)}")

        return f"<{self.__class__.__name__} {', '.join(columns)}>"


class TimestampMixin(BaseModel):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("timezone('utc', now())"),
        comment="Дата создания",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("timezone('utc', now())"),
        onupdate=func.now(),
        comment="Дата последнего обновления",
    )


class SoftDeleteMixin(BaseModel):
    __abstract__ = True

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Дата удаления",
    )
