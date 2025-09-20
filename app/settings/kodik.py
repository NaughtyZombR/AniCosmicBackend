from pydantic import Field, HttpUrl

from core.schemas.base import NonEmptyString
from settings.base import CommonBaseSettings


class KodikAPISettings(CommonBaseSettings):
    host: HttpUrl = Field(
        validation_alias="KODIK_API_HOST"
    )
    token: NonEmptyString = Field(
        validation_alias="KODIK_API_TOKEN"
    )
    translation_id: NonEmptyString = Field(
        validation_alias="KODIK_TRANSLATION_ID"
    )


kodik_settings = KodikAPISettings()
