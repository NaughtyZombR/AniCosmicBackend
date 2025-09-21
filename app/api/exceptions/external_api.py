from api.exceptions.base import FailedDependencyException


class KodikBadResponseException(FailedDependencyException):
    def __init__(self) -> None:
        super().__init__(detail="Bad response from Kodik API")
