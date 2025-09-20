from api.exceptions.base import BadRequestException, NotFoundException


class FileNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__(obj="File")


class InvalidFileException(BadRequestException):
    def __init__(self) -> None:
        super().__init__(detail="File is invalid")
