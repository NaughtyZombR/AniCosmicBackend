from pydantic import Field, PostgresDsn, SecretStr
from settings.base import CommonBaseSettings


class DatabaseSettings(CommonBaseSettings):
    host: str = Field(validation_alias="DB_HOST")
    port: int = Field(validation_alias="DB_PORT")
    password: SecretStr = Field(validation_alias="DB_PASSWORD")
    name: str = Field(validation_alias="DB_NAME")
    user: SecretStr = Field(validation_alias="DB_USER")

    @property
    def url(self) -> str:
        host = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.user.get_secret_value(),
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            path=self.name,
        )
        return str(host)

    @property
    def sync_url(self) -> str:
        host = PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=self.user.get_secret_value(),
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            path=self.name,
        )
        return str(host)


db_settings = DatabaseSettings()
