from api.exceptions.base import NotFoundException


class AnimeMaterialNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__(obj="AnimeMaterial")
