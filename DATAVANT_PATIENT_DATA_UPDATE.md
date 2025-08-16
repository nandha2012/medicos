# Datavant Patient Data Update

## Summary

Updated Datavant SmartRequest patient details to use **birth certificate mom data** from the details API instead of medical record fields. This ensures the patient information in Datavant requests uses the correct mother's information from birth certificate records.

## Changes Made

### Patient Data Field Mapping

**Before (Medical Record fields):**
```python
patient=Patient(
    firstName=getattr(data, 'mr_first_name', ''),      # Medical record
    lastName=getattr(data, 'mr_last_name', ''),        # Medical record  
    dateOfBirth=getattr(data, 'mr_date_of_birth', ''), # Medical record
    ssn=getattr(data, 'mr_ssn', ''),                   # Medical record
    customId=getattr(data, 'mr_custom_id', data.mg_idpreg)
)
```

**After (Birth Certificate Mom fields):**
```python
patient=Patient(
    firstName=getattr(data, 'bc_momnamefirst', ''),    # Birth certificate mom
    lastName=getattr(data, 'bc_momnamelast', ''),      # Birth certificate mom
    dateOfBirth=getattr(data, 'bc_mom_dob', ''),       # Birth certificate mom
    ssn=getattr(data, 'bc_momssn', ''),                # Birth certificate mom  
    customId=getattr(data, 'mr_custom_id', data.mg_idpreg)  # Unchanged
)
```

### Field Mapping Table

| Patient Field | Old Source | New Source | Description |
|---|---|---|---|
| `firstName` | `mr_first_name` | `bc_momnamefirst` | Mother's first name from birth certificate |
| `lastName` | `mr_last_name` | `bc_momnamelast` | Mother's last name from birth certificate |
| `dateOfBirth` | `mr_date_of_birth` | `bc_mom_dob` | Mother's date of birth from birth certificate |
| `ssn` | `mr_ssn` | `bc_momssn` | Mother's SSN from birth certificate |
| `customId` | `mr_custom_id` or `mg_idpreg` | **Unchanged** | Record identifier (no change) |

### Added Patient Data Logging

Added logging to show what patient data is being used:

```python
# Log patient data being used
patient_name = f"{getattr(data, 'bc_momnamefirst', '')} {getattr(data, 'bc_momnamelast', '')}".strip()
print(f"👤 Using patient data: {patient_name} (DOB: {getattr(data, 'bc_mom_dob', 'N/A')})")
```

## Example Output

### With Birth Certificate Data
```
👤 Using patient data: Sarah Johnson (DOB: 1985-03-15)

Patient Details:
- First Name: 'Sarah'
- Last Name: 'Johnson'  
- Date of Birth: '1985-03-15'
- SSN: '123456789'
- Custom ID: 'TEST123'
```

### Without Birth Certificate Data (Fallback)
```
👤 Using patient data:  (DOB: N/A)

Patient Details:
- First Name: '' (empty)
- Last Name: '' (empty)
- Date of Birth: '' (empty) 
- SSN: '' (empty)
- Custom ID: 'TEST456'
```

## Behavior

### Data Source Priority
1. **Primary**: Birth certificate mom fields (`bc_mom*`)
2. **Fallback**: Empty strings if BC mom fields not available
3. **Note**: Medical record fields (`mr_*`) are no longer used for patient data

### Consistency Across Request Types
All request types use the same patient data source:

| Request Type | Patient Data Source | Example |
|---|---|---|
| Mother (`"1"`) | Birth certificate mom | Sarah Johnson (1985-03-15) |
| Infant (`"2"`) | Birth certificate mom | Sarah Johnson (1985-03-15) |
| Combined (other) | Birth certificate mom | Sarah Johnson (1985-03-15) |

### Fallback Behavior
- If birth certificate mom fields are missing/empty, uses empty strings
- Does **not** fall back to medical record fields
- `customId` continues to use `mg_idpreg` as record identifier

## Testing Results

✅ **Field Mapping**: All patient fields use birth certificate mom data  
✅ **Fallback Logic**: Empty strings when BC mom data unavailable  
✅ **Consistency**: All request types use same patient data source  
✅ **Logging**: Patient data usage is properly logged  
✅ **Custom ID**: Record identifier unchanged and working  

### Test Examples

**With BC Mom Data:**
```
Patient: Maria Garcia
DOB: 1990-07-22, SSN: 555123456
```

**Without BC Mom Data:**
```
Patient:  
DOB: , SSN: 
```

## API Fields Used

The Datavant patient details now use these fields from the details API:

```python
# From details API response
data.bc_momnamefirst   # → patient.firstName
data.bc_momnamelast    # → patient.lastName  
data.bc_mom_dob        # → patient.dateOfBirth
data.bc_momssn         # → patient.ssn
data.mg_idpreg         # → patient.customId (unchanged)
```

## Benefits

1. **Accurate Patient Data**: Uses official birth certificate mother information
2. **Consistent Source**: All patient fields come from same data source (BC mom)
3. **Data Integrity**: No mixing of medical record and birth certificate data
4. **Appropriate Context**: Mother's data for mother/infant medical record requests
5. **Clear Logging**: Visibility into what patient data is being used
6. **Fallback Safety**: Graceful handling when BC mom data unavailable

## Files Modified

- ✅ `app/services/record_service.py`: Updated patient data field mapping and added logging
- ✅ `test_patient_data_update.py`: Comprehensive test suite for patient data
- ✅ `DATAVANT_PATIENT_DATA_UPDATE.md`: This documentation

## Usage

Patient data is now automatically sourced from birth certificate mom fields:

```python
# Automatically uses birth certificate mom data
datavant_request = get_datavant_request_data(redcap_data, request_for)
patient = datavant_request.patient

print(f"Patient: {patient.firstName} {patient.lastName}")  # Birth certificate mom name
print(f"DOB: {patient.dateOfBirth}")                       # Birth certificate mom DOB
print(f"SSN: {patient.ssn}")                              # Birth certificate mom SSN
```

**No manual configuration needed - the system automatically uses birth certificate mother data for all Datavant patient information.**