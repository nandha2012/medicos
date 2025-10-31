# Datavant Date Range Update

## Summary

Updated Datavant SmartRequest date logic to use **current date as start date** and **current date + 5 days as end date** instead of using form data. Implemented using the dedicated `app/utils/dates.py` utility file.

## Changes Made

### 1. Enhanced `app/utils/dates.py`

Added new utility functions for Datavant date handling:

```python
def get_datavant_date_range() -> tuple[str, str]:
    """Get date range for Datavant requests: current date to current date + 5 days"""
    today = datetime.now()
    start_date = today.strftime("%Y-%m-%d")
    end_date = (today + timedelta(days=5)).strftime("%Y-%m-%d")
    return start_date, end_date

def get_current_date_str() -> str:
    """Returns the current date as YYYY-MM-DD string"""

def get_date_plus_days(days: int) -> str:
    """Returns a date string that is 'days' from today in YYYY-MM-DD format"""
```

### 2. Updated `app/services/record_service.py`

**Before:**
```python
# Used form data (could be empty or inconsistent)
startDate=getattr(data, 'mr_start_date', ''),
endDate=getattr(data, 'mr_end_date', '')
```

**After:**
```python
# Uses calculated date range with logging
from utils.dates import get_datavant_date_range

# Get date range for the request
date_range = get_datavant_date_range()
print(f"🗓️ Using Datavant date range: {date_range[0]} to {date_range[1]}")

requestCriteria=[RequestCriteria(
    recordTypes=_get_record_types_for_datavant_request(data, request_for),
    startDate=date_range[0],  # Current date
    endDate=date_range[1]     # Current date + 5 days
)]
```

### 3. Removed Unused Code

- Removed local `_get_datavant_date_range()` function
- Removed unnecessary `timedelta` import from record_service.py
- Centralized all date logic in the utils module

## Current Behavior

### Date Range Logic
- **Start Date**: Current date (e.g., `2025-08-16`)
- **End Date**: Current date + 5 days (e.g., `2025-08-21`)
- **Format**: `YYYY-MM-DD` (ISO 8601)

### Logging
Each Datavant request now logs the date range being used:
```
🗓️ Using Datavant date range: 2025-08-16 to 2025-08-21
```

### Consistency
All request types (Mother, Infant, Combined) use the same date logic:

| Request Type | Start Date | End Date | Example |
|---|---|---|---|
| Mother (`"1"`) | Current | Current + 5 days | 2025-08-16 to 2025-08-21 |
| Infant (`"2"`) | Current | Current + 5 days | 2025-08-16 to 2025-08-21 |
| Combined (other) | Current | Current + 5 days | 2025-08-16 to 2025-08-21 |

## Testing Results

✅ **Date Utility Functions**: All functions return correct dates  
✅ **Datavant Integration**: Request creation uses calculated dates  
✅ **Consistency**: All request types use same date logic  
✅ **Format Validation**: Dates are in correct YYYY-MM-DD format  
✅ **Logging**: Date ranges are properly logged  

### Test Output Example
```
🗓️ Using Datavant date range: 2025-08-16 to 2025-08-21

📅 Date Range in Request:
   Start Date: 2025-08-16
   End Date: 2025-08-21
   ✅ Start date is current date
   ✅ End date is current date + 5 days
```

## Benefits

1. **Predictable Dates**: Always uses current date + 5 days regardless of form data
2. **Consistency**: All requests use the same date calculation logic
3. **Maintainable**: Centralized in utils/dates.py for easy updates
4. **Extensible**: Additional date functions available for future use
5. **Logged**: Clear visibility into date ranges being used
6. **Format Safe**: Guarantees YYYY-MM-DD format compliance

## Utility Functions Available

Beyond the Datavant-specific functions, the dates utility now provides:

```python
# Datavant-specific
get_datavant_date_range() -> tuple[str, str]
get_current_date_str() -> str
get_date_plus_days(days: int) -> str

# General utilities (existing)
get_current_time() -> datetime
get_current_time_str(fmt: Optional[str] = None) -> str
add_time_to_str(time_str: str, time_delta: int, period) -> str
# ... and more
```

## Files Modified

- ✅ `app/utils/dates.py`: Added Datavant date functions
- ✅ `app/services/record_service.py`: Updated to use date utilities
- ✅ `DATAVANT_DATE_UPDATE.md`: This documentation

## Usage

The date logic is now automatic in all Datavant requests:

```python
# Automatically uses current date + 5 days
datavant_request = get_datavant_request_data(redcap_data, request_for)
print(datavant_request.requestCriteria[0].startDate)  # 2025-08-16
print(datavant_request.requestCriteria[0].endDate)    # 2025-08-21
```

**No manual date configuration needed - the system automatically calculates appropriate date ranges for all Datavant requests.**