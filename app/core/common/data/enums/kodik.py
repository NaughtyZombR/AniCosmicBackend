# core/common/data/enums.py
from enum import StrEnum, unique


@unique
class AnimeKind(StrEnum):
    """Тип аниме"""

    TV = "tv"  # Телесериал
    MOVIE = "movie"  # Фильм
    OVA = "ova"  # OVA (Original Video Animation)
    ONA = "ona"  # ONA (Original Net Animation)
    SPECIAL = "special"  # Спешл
    MUSIC = "music"  # Музыкальное аниме
    TV_13 = "tv_13"  # Сериал с эпизодами по 13 серий
    TV_24 = "tv_24"  # Сериал с эпизодами по 24 серии
    TV_48 = "tv_48"  # Сериал с эпизодами по 48 серий


@unique
class MPAA(StrEnum):
    """Возрастной рейтинг MPAA"""

    G = "G"  # Для всех
    PG = "PG"  # Родительский контроль
    PG13 = "PG-13"  # 13+
    R = "R"  # 17+ (ограничения)
    R_PLUS = "R+"  # 17+ с возможными жесткими сценами
    RX = "Rx"  # Только для взрослых


@unique
class MaterialStatus(StrEnum):
    """Статус материала"""

    ANONS = "anons"  # Анонсирован
    ONGOING = "ongoing"  # В процессе выпуска
    RELEASED = "released"  # Выпущен полностью


@unique
class TranslationType(StrEnum):
    """Тип перевода"""

    VOICE = "voice"  # Голосовой
    SUBTITLES = "subtitles"  # С субтитрами
