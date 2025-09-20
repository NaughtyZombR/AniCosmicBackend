from typing import Annotated, Generic, NamedTuple, TypeVar

from core.schemas.base import BaseSchema
from pydantic import Field, NonNegativeInt, PositiveInt

PageField = Annotated[
    PositiveInt, Field(default=1, description="Номер страницы", examples=[1, 5])
]
PerPageField = Annotated[
    PositiveInt,
    Field(
        default=10,
        le=100,
        description="Количество объектов на странице",
        examples=[10, 20],
    ),
]
TotalField = Annotated[
    NonNegativeInt,
    Field(
        description="Общее количество существующих объектов",
        examples=[100, 2000],
    ),
]


class OffsetLimit(NamedTuple):
    offset: NonNegativeInt
    limit: PositiveInt


class PaginationParams(BaseSchema):
    page: PageField
    per_page: PerPageField

    def to_offset_limit(self) -> OffsetLimit:
        offset = (self.page - 1) * self.per_page
        return OffsetLimit(offset=offset, limit=self.per_page)


class PaginationParamsMeta(PaginationParams):
    total: TotalField


_ItemSchema = TypeVar("_ItemSchema", bound=BaseSchema)


class PaginationPageRead(PaginationParamsMeta, Generic[_ItemSchema]):
    items: list[_ItemSchema]
