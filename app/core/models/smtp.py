import uuid

from core.models.base import BaseModel
from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column


class SMTPConfig(BaseModel):
    __tablename__ = "smtp_config"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid.uuid4,
    )
    hostname: Mapped[str]
    port: Mapped[int]
    username: Mapped[str]
    password: Mapped[str]
