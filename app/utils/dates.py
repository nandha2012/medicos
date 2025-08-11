from datetime import datetime, timedelta
from typing import Literal, Optional

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

def add_time_to_str(time_str: str, time_delta: int, period: Literal['hours', 'minutes', 'seconds']) -> str:
    """
    Adds a specified number of hours to a time string.
    """
    return (datetime.strptime(time_str, DEFAULT_TIME_FORMAT) + timedelta(**{period: time_delta})).strftime(DEFAULT_TIME_FORMAT)

def subtract_time_from_str(time_str: str, time_delta: int, period: Literal['hours', 'minutes', 'seconds', 'days']) -> str:
    """
    Subtracts a specified number of hours from a time string.
    """
    return (datetime.strptime(time_str, DEFAULT_TIME_FORMAT) - timedelta(**{period: time_delta})).strftime(DEFAULT_TIME_FORMAT)

def get_one_hour_before_str(fmt: Optional[str] = None) -> str:
    """
    Returns the time one hour ago as a formatted string.
    Uses default format '%Y-%m-%d %H:%M' if fmt is None.
    """
    fmt = fmt or DEFAULT_TIME_FORMAT
    return (datetime.now() - timedelta(hours=1)).strftime(fmt)
    
def get_start_of_today_str(fmt: Optional[str] = None) -> str:
    """
    Returns the start of today (00:00:00) as a formatted string.
    Uses default format '%Y-%m-%d %H:%M' if fmt is None.
    """
    fmt = fmt or DEFAULT_TIME_FORMAT
    start_of_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    return start_of_day.strftime(fmt)

def generate_dir_name():
    now = datetime.now()
    return now.strftime("%m_%d_%Y")

