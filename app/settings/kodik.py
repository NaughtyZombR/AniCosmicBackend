from core.schemas.base import NonEmptyString
from pydantic import Field, HttpUrl
from settings.base import CommonBaseSettings


class KodikAPISettings(CommonBaseSettings):
    host: HttpUrl = "https://kodikapi.com"
    token: NonEmptyString = Field(validation_alias="KODIK_API_TOKEN")
    translation_id: NonEmptyString = Field(
        validation_alias="KODIK_TRANSLATION_ID"
    )


kodik_settings = KodikAPISettings()
