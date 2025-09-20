from core.schemas.base import BaseSchema, NonEmptyString
from pydantic import Field, PositiveInt


class _BaseSMTPConfig(BaseSchema):
    hostname: NonEmptyString = Field(
        description="Имя хоста SMTP",
        examples=["smtp.gmail.com"],
    )
    port: PositiveInt = Field(
        description="Порт SMTP",
        examples=[587],
    )
    username: NonEmptyString = Field(
        description="Имя пользователя SMTP",
        examples=["username"],
    )


class SMTPConfigRead(_BaseSMTPConfig):
    pass


class SMTPConfigUpdate(_BaseSMTPConfig):
    password: NonEmptyString = Field(
        description="Пароль SMTP",
        examples=["password"],
    )
