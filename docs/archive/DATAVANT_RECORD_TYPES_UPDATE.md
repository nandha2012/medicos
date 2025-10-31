# Datavant Record Types Update

## Summary

Updated the Datavant SmartRequest integration to use the correct record types for mom and infant medical record requests, as specified in the Datavant API documentation.

## Changes Made

### 1. Updated `smartrequest_faker.py`

- **Updated `get_record_types()`**: Replaced generic record types with Datavant-compliant record types for mom and infant requests
- **Added `get_infant_record_types()`**: Returns 33 record types specific to infant requests
- **Added `get_mom_record_types()`**: Returns 28 record types specific to mom requests  
- **Updated sample payload**: Changed example record types from `["Abstract", "Laboratory Results"]` to `["Laboratory and Hematology", "Nursing Notes", "Discharge Summary"]`

### 2. Updated `smartrequest_service.py`

- **Added `get_infant_record_types()`**: Production method for infant record types
- **Added `get_mom_record_types()`**: Production method for mom record types
- Both methods support both faker mode (for testing) and production mode

## Record Types Implemented

### Infant Record Types (33 types)
```python
[
    "Cardiology Reports", "Laboratory and Hematology", "Labor and Delivery Records", 
    "Audiology Report", "Admission Report", "Scanned Documents", "Medication Information", 
    "History and Physical", "Radiology Report", "Coding Summary", "Flowsheets", 
    "Occupational Therapy", "Physician Orders", "Speech Therapy", "Ultrasound", 
    "Demographic", "Orders and Results", "Facesheet", "Operative Report", 
    "Pathology Report", "Physician Progress Notes", "Physical Therapy Rehab records", 
    "Transfer Report", "Medication Orders", "Consults", "Problem List", 
    "Discharge Instructions", "Prenatal Care", "Discharge Summary", 
    "Birth Letter Confirmation", "Continuity of Care Document", "Nursing Notes", 
    "Toxicology Reports"
]
```

### Mom Record Types (28 types)
```python
[
    "Laboratory and Hematology", "Labor and Delivery Records", "Admission Report", 
    "Scanned Documents", "Medication Information", "History and Physical", 
    "Coding Summary", "Flowsheets", "Physician Orders", "Ultrasound", 
    "Demographic", "Orders and Results", "Facesheet", "ED Records", 
    "Operative Report", "Pathology Report", "Physician Progress Notes", 
    "Transfer Report", "Medication Orders", "Consults", "Problem List", 
    "Discharge Instructions", "Prenatal Care", "Discharge Summary", 
    "Birth Letter Confirmation", "Continuity of Care Document", "Nursing Notes", 
    "Toxicology Reports"
]
```

### Key Differences

**Infant-only record types (6):**
- Audiology Report
- Cardiology Reports  
- Occupational Therapy
- Physical Therapy Rehab records
- Radiology Report
- Speech Therapy

**Mom-only record types (1):**
- ED Records

**Common record types (27):** Most types are shared between mom and infant requests.

## Usage

### Basic Usage
```python
from app.services.smartrequest_service import SmartRequestService

service = SmartRequestService()

# Get infant record types
infant_types = service.get_infant_record_types()
print(f"Available infant record types: {len(infant_types)}")

# Get mom record types  
mom_types = service.get_mom_record_types()
print(f"Available mom record types: {len(mom_types)}")

# Get all available record types
all_types = service.get_record_types()
print(f"Total available record types: {len(all_types)}")
```

### Request Creation
```python
# For infant request
request_data = {
    # ... other fields ...
    "requestCriteria": [{
        "recordTypes": service.get_infant_record_types()[:5],  # Select specific types
        "startDate": "2024-01-01",
        "endDate": "2024-12-31"
    }]
}

# For mom request
request_data = {
    # ... other fields ...
    "requestCriteria": [{
        "recordTypes": service.get_mom_record_types()[:3],  # Select specific types  
        "startDate": "2024-01-01",
        "endDate": "2024-12-31"
    }]
}
```

## Files Added

1. **`datavant_record_types_example.py`**: Example script demonstrating usage
2. **`validate_record_types.py`**: Validation script to ensure implementation correctness
3. **`DATAVANT_RECORD_TYPES_UPDATE.md`**: This documentation file

## Testing

All changes have been tested and validated:

- ✅ Record types match exactly with provided arrays
- ✅ Integration with existing SmartRequest service works correctly
- ✅ Both faker mode and production mode supported
- ✅ Backward compatibility maintained

## References

- Datavant SmartRequest API documentation: `Requester API Quickstart Guide - 03_26_2025 (1).pdf`
- Record types specified in user request for mom and infant medical records
- Existing SmartRequest integration in `/app/services/`

## Notes

- Record types are case-sensitive and must match Datavant's exact naming
- Always validate record types against specific facility capabilities
- Consider requesting specific records rather than entire medical record for better quality
- The implementation supports both sandbox and production environments