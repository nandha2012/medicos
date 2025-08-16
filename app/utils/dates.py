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

def get_datavant_date_range() -> tuple[str, str]:
    """
    Get date range for Datavant requests: current date to current date + 5 days
    
    Returns:
        Tuple of (start_date, end_date) in YYYY-MM-DD format
    """
    today = datetime.now()
    start_date = today.strftime("%Y-%m-%d")
    end_date = (today + timedelta(days=5)).strftime("%Y-%m-%d")
    return start_date, end_date

def get_current_date_str() -> str:
    """
    Returns the current date as YYYY-MM-DD string.
    """
    return datetime.now().strftime("%Y-%m-%d")

def get_date_plus_days(days: int) -> str:
    """
    Returns a date string that is 'days' from today in YYYY-MM-DD format.
    
    Args:
        days: Number of days to add (positive for future, negative for past)
        
    Returns:
        Date string in YYYY-MM-DD format
    """
    target_date = datetime.now() + timedelta(days=days)
    return target_date.strftime("%Y-%m-%d")

