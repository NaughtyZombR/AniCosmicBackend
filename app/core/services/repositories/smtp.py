from uuid import UUID

from core.models import SMTPConfig
from core.schemas.smtp import SMTPConfigUpdate
from core.services.repositories.SQLAlchemy import SQLAlchemyRepository


class SMTPConfigRepository(
    SQLAlchemyRepository[SMTPConfig, None, SMTPConfigUpdate]
):
    @property
    def model(self) -> type[SMTPConfig]:
        return SMTPConfig

    @property
    def model_pk(self) -> UUID:
        return SMTPConfig.id

    async def get(self) -> SMTPConfig | None:
        smtp_config = await self.get_one_where(where=())
        return smtp_config

    async def update(self, schema: SMTPConfigUpdate) -> SMTPConfig:
        smtp_config = await self.get_one_where(where=())
        if smtp_config is None:
            return await self.create_from_orm(
                self.model(
                    hostname=schema.hostname,
                    port=schema.port,
                    username=schema.username,
                    password=schema.password,
                )
            )
        else:
            return await self.update_by_pk(smtp_config.id, schema)
