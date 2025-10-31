# Datavant Facility CSV Integration

## Summary

Implemented facility data integration with Datavant CSV file for SmartRequest API calls. The system now uses facility data from `Datavant_ Facility_List.csv` instead of form data for creating medical record requests.

## Changes Made

### 1. Added CSV Loading Functionality

```python
def load_datavant_facilities() -> List[Dict[str, Any]]:
    """Load and cache facility data from Datavant CSV"""
    # Loads 47,505+ facilities from CSV with caching
```

**Features:**
- **Caching**: Loads CSV once and caches in memory for performance
- **Error Handling**: Graceful fallback if CSV loading fails
- **Data Standardization**: Maps CSV columns to Datavant API format

### 2. Added Facility Lookup Functions

```python
def get_facility_by_site(site_number: str) -> Optional[Dict[str, Any]]:
    """Get facility by site number (e.g., '00101')"""

def get_first_facility() -> Optional[Dict[str, Any]]:
    """Get first facility from CSV (current default)"""
```

### 3. Updated Datavant Request Creation

```python
def _get_facility_for_datavant_request(data: RedcapResponseFirst) -> Facility:
    """Get facility for Datavant request, prioritizing CSV over form data"""
    
# BEFORE: Used form data
facility=Facility(
    addressLine1=getattr(data, 'mr_address_line_1', ''),
    city=getattr(data, 'mr_city', ''),
    # ... more form fields
)

# AFTER: Uses CSV data  
facility=_get_facility_for_datavant_request(data)
```

## CSV File Structure

The `Datavant_ Facility_List.csv` contains **47,505 facilities** with these key fields:

| CSV Column | API Field | Example |
|---|---|---|
| `SITE` | `site` | "00101" |
| `Health System ` | `healthSystem` | "BOWEN HEFLEY ORTHOPEDICS (AR)" |
| `SiteName` | `siteName` | "BOWEN HEFLEY ORTHOPEDICS- LITTLE ROCK OFFICE" |
| `Address` | `addressLine1` | "#5 ST VINCENT CR" |
| `Address2` | `addressLine2` | "1ST AND 4TH FL" |
| `City` | `city` | "LITTLE ROCK" |
| `State` | `state` | "AR" |
| `ZIP` | `zip` | "72205" |
| `PHONE` | `phone` | "5016636455" |
| `Fax` | `fax` | "" |

## Current Implementation

### Default Behavior
Currently uses the **first facility** from the CSV file as requested:

```
✅ Default Facility:
   Site: 00101
   Name: BOWEN HEFLEY ORTHOPEDICS- LITTLE ROCK OFFICE
   Health System: BOWEN HEFLEY ORTHOPEDICS (AR)
   Address: #5 ST VINCENT CR, 1ST AND 4TH FL
   City: LITTLE ROCK, AR 72205
   Phone: 5016636455
```

### Fallback Logic
1. **Priority 1**: Use CSV facility data (current: first facility)
2. **Priority 2**: Fallback to form data if CSV loading fails

## Future Enhancement Ready

The code is prepared for **facility matching** based on RedCap detail response:

```python
# TODO: Future implementation
facility_number = getattr(data, 'facility_number', None)
if facility_number:
    csv_facility = get_facility_by_site(str(facility_number).zfill(5))
    if csv_facility:
        return create_facility_from_csv_data(csv_facility)
```

**When facility matching is implemented:**
1. Extract facility number from RedCap detail response
2. Pad to 5 digits (e.g., "101" → "00101")
3. Lookup matching facility in CSV by `SITE` column
4. Use matched facility data for Datavant request

## Testing Results

✅ **CSV Loading**: Successfully loads 47,505 facilities  
✅ **First Facility**: Correctly retrieves default facility  
✅ **Site Lookup**: Successfully finds facilities by site number  
✅ **Data Format**: All required fields present and valid  
✅ **Integration**: Works correctly with Datavant request creation  
✅ **Fallback**: Gracefully handles CSV loading failures  

## Usage Examples

### Get Default Facility
```python
facility = get_first_facility()
# Returns: BOWEN HEFLEY ORTHOPEDICS- LITTLE ROCK OFFICE (Site: 00101)
```

### Lookup by Site Number
```python
facility = get_facility_by_site("00115")
# Returns: CONWAY REGIONAL REHABILITATION HOSPITAL
```

### Create Datavant Request
```python
# Automatically uses CSV facility data
datavant_request = get_datavant_request_data(redcap_data, request_for)
print(datavant_request.facility.siteName)
# Output: BOWEN HEFLEY ORTHOPEDICS- LITTLE ROCK OFFICE
```

## Files Modified

- `app/services/record_service.py`: Core facility integration logic
- Added `test_facility_integration.py`: Comprehensive test suite

## Benefits

1. **Accurate Data**: Uses official Datavant facility information
2. **Performance**: CSV caching prevents repeated file reads  
3. **Reliability**: Fallback logic prevents request failures
4. **Future-Ready**: Prepared for facility matching implementation
5. **Maintainable**: Clear separation of concerns and documented TODO

## Next Steps

When facility matching is needed:
1. Identify the field in RedCap detail response containing facility number
2. Update `_get_facility_for_datavant_request()` to use facility matching
3. Test facility matching with various site numbers
4. Handle edge cases (facility not found, invalid format, etc.)