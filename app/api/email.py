from api.dependencies.services import EmailServiceDep
from api.dependencies.user import Admin
from api.tags import APITags
from core.models import SMTPConfig
from core.schemas.smtp import SMTPConfigRead, SMTPConfigUpdate
from fastapi import APIRouter

router = APIRouter(
    prefix="/email",
    tags=[APITags.Email],
)


@router.get("/configuration", response_model=SMTPConfigRead)
async def get_email_configuration(
    email_service: EmailServiceDep,
    _: Admin,
) -> SMTPConfig:
    return await email_service.get()


@router.put("/configuration", response_model=SMTPConfigRead)
async def update_email_configuration(
    schema: SMTPConfigUpdate,
    email_service: EmailServiceDep,
    _: Admin,
) -> SMTPConfig:
    return await email_service.put(schema)
