from api.exceptions.base import NotFoundException


class SMTPConfigNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__(obj="SMTP Config")
