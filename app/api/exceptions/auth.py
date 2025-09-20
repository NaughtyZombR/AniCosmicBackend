from api.exceptions.base import UnauthorizedException


class NoRefreshTokenException(UnauthorizedException):
    def __init__(self) -> None:
        super().__init__(detail="No refresh token")


class RefreshTokenExpiredException(UnauthorizedException):
    def __init__(self) -> None:
        super().__init__(detail="Refresh token expired")


class InvalidCredentialsException(UnauthorizedException):
    def __init__(self) -> None:
        super().__init__(
            detail="Invalid credentials",
        )


class AccessTokenExpiredException(UnauthorizedException):
    def __init__(self) -> None:
        super().__init__(detail="Access token expired")
