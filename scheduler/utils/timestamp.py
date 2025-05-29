import datetime

def get_millisecond_timestamp(dt: datetime.datetime) -> int:
    """
    Get the current timestamp in milliseconds.
    """
    return int(round(dt.timestamp() * 1000))


def get_current_millisecond_timestamp(plus_dt: datetime.timedelta | None = None) -> int:
    """
    Get the current timestamp in milliseconds.
    """
    if plus_dt:
        dt = datetime.datetime.now(tz=datetime.timezone.utc) + plus_dt
    else:
        dt = datetime.datetime.now(tz=datetime.timezone.utc)
    return get_millisecond_timestamp(dt)
