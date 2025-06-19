from datetime import datetime, timedelta
from typing import Optional

DEFAULT_TIME_FORMAT = "%Y-%m-%d %H:%M"

def get_current_time() -> datetime:
    """Returns the current datetime object."""
    return datetime.now()

def get_one_hour_before() -> datetime:
    """Returns the datetime object one hour before now."""
    return datetime.now() - timedelta(hours=1)

def get_current_time_str(fmt: Optional[str] = None) -> str:
    """
    Returns the current time as a formatted string.
    Uses default format '%Y-%m-%d %H:%M' if fmt is None.
    """
    fmt = fmt or DEFAULT_TIME_FORMAT
    return datetime.now().strftime(fmt)

def get_one_hour_before_str(fmt: Optional[str] = None) -> str:
    """
    Returns the time one hour ago as a formatted string.
    Uses default format '%Y-%m-%d %H:%M' if fmt is None.
    """
    fmt = fmt or DEFAULT_TIME_FORMAT
    return (datetime.now() - timedelta(hours=1)).strftime(fmt)
