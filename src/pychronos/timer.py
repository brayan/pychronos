from pychronos.constants import LAST_MINUTES, IN_PROGRESS, BREAK


def get_status(now):
    time = now.time()
    minutes = time.minute()
    seconds = time.second()
    if 0 <= minutes < 50:
        if minutes > 40 or (minutes == 40 and seconds > 0):
            return LAST_MINUTES
        return IN_PROGRESS
    return BREAK


def calculate_timer(now):
    time = now.time()
    if 0 <= time.minute() < 50:
        minutes = 49 - time.minute()
    else:
        minutes = 59 - time.minute()
    seconds = 60 - time.second()
    if seconds == 60:
        seconds = 0
        minutes += 1
    return minutes, seconds
