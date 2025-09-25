from api.exceptions.base import NotFoundException


class GenreNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__(obj="Genre")
