from pydantic import PositiveInt, SecretStr
from settings.base import CommonBaseSettings


class AuthSettings(CommonBaseSettings):
    jwt_secret_key: SecretStr
    reset_password_token_secret: SecretStr
    verification_token_secret: SecretStr

    algorithm: str = "HS256"
    access_token_expiration_seconds: PositiveInt = 1 * 60 * 60  # 1 час
    refresh_token_expiration_seconds: PositiveInt = 30 * 24 * 60 * 60  # 30 дней


auth_settings = AuthSettings()
