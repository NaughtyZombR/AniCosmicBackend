from api.exceptions.smtp import SMTPConfigNotFoundException
from core.models import SMTPConfig
from core.schemas.smtp import SMTPConfigUpdate
from core.services.base import ModelService
from core.services.repositories.smtp import SMTPConfigRepository


class EmailService(ModelService[SMTPConfig, None, SMTPConfigUpdate]):
    @property
    def model_repository(self) -> type[SMTPConfigRepository]:
        return SMTPConfigRepository

    @property
    def not_found_error(self) -> type[SMTPConfigNotFoundException]:
        return SMTPConfigNotFoundException

    async def get(self) -> SMTPConfig:
        config = await self._repository.get()
        if config is None:
            raise self.not_found_error
        return config

    async def put(self, schema: SMTPConfigUpdate) -> SMTPConfig:
        config = await self._repository.update(schema)
        await self.save_changes()
        return config
