from core.schemas.base import BaseSchema


class HealthCheckRead(BaseSchema):
    database: bool
