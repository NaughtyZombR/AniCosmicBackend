from typing import Annotated

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    Field,
    PositiveInt,
)

IntID = Annotated[
    PositiveInt,
    Field(description="Численный идентификатор", examples=[1, 768519797]),
]
NonEmptyString = Annotated[
    str,
    Field(
        min_length=1, description="Не пустая строка", examples=["string", "s"]
    ),
]
type DictStrAny = dict[str, ...]

SchemaValidationError = ValueError("Произошла ошибка при валидации схемы")


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TimestampSchema(BaseSchema):
    created_at: AwareDatetime
    updated_at: AwareDatetime


class SoftDeleteSchema(BaseSchema):
    deleted_at: AwareDatetime
