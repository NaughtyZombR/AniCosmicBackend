from api.exceptions.base import NotFoundException


class PostNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__(obj="Post")
