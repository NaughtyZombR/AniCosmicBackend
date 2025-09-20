from datetime import time


def time_from_seconds(seconds: float) -> time:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return time(
        hour=int(hours),
        minute=int(minutes),
        second=int(seconds),
    )
