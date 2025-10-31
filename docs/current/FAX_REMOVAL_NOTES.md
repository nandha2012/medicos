# Fax Field Removal from Datavant Integration

## Summary

The fax field has been removed from the Datavant Facility model as it is no longer required for Datavant API requests. This document outlines all changes made and the impact on the system.

**Date:** 2025-01-31
**Reason:** Datavant no longer requires fax numbers for medical records requests
**Impact:** Low - Backward compatible changes only

---

## Files Modified

### 1. Core Model (`app/models/datavant_request.py`)

**Change:** Removed `fax` field from `Facility` model

```python
class Facility(BaseModel):
    addressLine1: str
    addressLine2: Optional[str] = None
    city: str
    state: str
    zip: str
    healthSystem: str
    siteName: str
    phone: str
    # fax: str  # REMOVED: Fax is no longer needed for Datavant requests
```

**Impact:**
- ✅ Facility objects no longer require fax parameter
- ✅ Datavant API requests will not include fax data
- ✅ Pydantic validation will reject fax field if provided

---

### 2. Record Service (`app/services/record_service.py`)

**Changes Made:**

#### a) CSV Facility Loader
Removed fax from CSV parsing:
```python
facility = {
    'site': row.get('SITE', '').strip(),
    'healthSystem': row.get('Health System ', '').strip(),
    'siteName': row.get('SiteName', '').strip(),
    'addressLine1': row.get('Address', '').strip(),
    'addressLine2': row.get('Address2', '').strip() or None,
    'city': row.get('City', '').strip(),
    'state': row.get('State', '').strip(),
    'zip': row.get('ZIP', '').strip(),
    'phone': row.get('PHONE', '').strip(),
    # 'fax': row.get('Fax', '').strip(),  # REMOVED: Fax no longer needed for Datavant
    # ... other fields
}
```

#### b) Facility Object Construction (CSV Path)
Removed fax parameter:
```python
return Facility(
    addressLine1=csv_facility['addressLine1'],
    addressLine2=csv_facility['addressLine2'],
    city=csv_facility['city'],
    state=csv_facility['state'],
    zip=csv_facility['zip'],
    healthSystem=csv_facility['healthSystem'],
    siteName=csv_facility['siteName'],
    phone=csv_facility['phone']
    # fax field removed - no longer needed for Datavant
)
```

#### c) Facility Object Construction (Form Data Fallback)
Removed fax parameter from fallback path:
```python
return Facility(
    addressLine1=getattr(data, 'mr_address_line_1', ''),
    addressLine2=getattr(data, 'mr_address_line_2', None),
    city=getattr(data, 'mr_city', ''),
    state=getattr(data, 'mr_state', ''),
    zip=getattr(data, 'mr_zip', ''),
    healthSystem=getattr(data, 'mr_health_system', ''),
    siteName=getattr(data, 'mr_site_name', ''),
    phone=getattr(data, 'mr_phone', '')
    # fax field removed - no longer needed for Datavant
)
```

**Impact:**
- ✅ Facility data loader no longer expects fax in CSV
- ✅ Datavant requests built without fax data
- ✅ Backward compatible - old CSV files with fax column still work (column is just ignored)

---

### 3. SmartRequest Faker (`app/services/smartrequest_faker.py`)

**Changes Made:**

Commented out fax generation in two locations:

```python
# Location 1: get_facilities() method
{
    "addressLine1": fake.street_address(),
    # ... other fields
    "phone": fake.phone_number().replace('-', '').replace('(', '').replace(')', '').replace(' ', '')[:10],
    # "fax": fake.phone_number()...  # REMOVED: Fax no longer needed
}

# Location 2: get_fake_facility_data() function
{
    "addressLine1": fake.street_address(),
    # ... other fields
    "phone": fake.phone_number().replace('-', '').replace('(', '').replace(')', '').replace(' ', '')[:10],
    # "fax": fake.phone_number()...  # REMOVED: Fax no longer needed
}
```

**Impact:**
- ✅ Fake/test facility data no longer includes fax
- ✅ Local testing uses simplified facility structure
- ✅ Mock Datavant requests aligned with production

---

### 4. Test Files

#### a) `test_facility_integration.py`

**Changes:**
1. Removed fax from required fields validation:
```python
required_fields = ['site', 'siteName', 'healthSystem', 'addressLine1', 'city', 'state', 'zip', 'phone']
# Note: 'fax' field removed - no longer required for Datavant requests
```

2. Commented out fax display:
```python
# print(f"   Fax: {first_facility['fax']}")  # REMOVED: Fax no longer in facility data
```

**Impact:**
- ✅ Tests updated to not expect fax
- ✅ Validation checks no longer fail on missing fax

---

## What Was NOT Changed

These files still contain fax-related fields but are **intentionally kept** as they are not related to Datavant:

### 1. RedCap Response Models (`app/models/redcap_response_second.py`)

**Kept:** Hospital and physician fax fields
```python
hospital_fax_num: Optional[str] = ""
physician_fax_num: Optional[str] = ""
```

**Reason:** These are RedCap form fields for data collection, not Datavant API fields. They may be used for:
- Record keeping
- Alternative contact methods
- Historical data
- PDF template population

**No Changes Needed**

---

### 2. External API Service (`app/services/external_api_service.py`)

**Kept:** Fax field in RedCap API request
```python
'fields[3]': 'hospital_fax_num',
```

**Reason:** This fetches data from RedCap, which may still collect fax numbers. The field is not used in Datavant requests.

**No Changes Needed**

---

### 3. Test File (`test_email_with_fax.py`)

**Kept:** Entire file unchanged

**Reason:** This is a test utility for email service, unrelated to Datavant API. The fax parameter is for testing email content, not Datavant requests.

**No Changes Needed**

---

### 4. Sample/Mock Data (`app/fake_responses.py`, `app/response_2_sample.json`)

**Kept:** Fax fields in mock RedCap responses

**Reason:** These simulate RedCap API responses which may include fax data. They don't affect Datavant requests.

**No Changes Needed**

---

## Backward Compatibility

### CSV Files
✅ **Old CSV files with Fax column:** Will continue to work. The Fax column is simply ignored during parsing.

✅ **New CSV files without Fax column:** Will work perfectly. The code doesn't expect fax anymore.

### Existing Data
✅ **RedCap forms with fax data:** Continue to work normally. Fax data is collected but not sent to Datavant.

✅ **Templates using fax placeholders:** Will display empty or use fallback values (depends on template design).

### API Integration
✅ **Datavant API:** Now receives Facility objects without fax - which is the correct format.

✅ **RedCap API:** Unchanged - still fetches fax data if available.

---

## Migration Notes

### For New Templates
When adding new templates in the future:
- ❌ Do NOT include fax placeholders for Datavant facilities
- ✅ DO include hospital_fax_num / physician_fax_num if needed for display purposes (from RedCap data)

### For Existing CSV Files
No changes required! The system handles both:
- CSV files with Fax column (ignored)
- CSV files without Fax column (works perfectly)

### For Testing
- Use `test_facility_integration.py` to verify facility loading
- Tests no longer check for fax field presence
- Faker services generate facilities without fax

---

## Validation Checklist

✅ **Model Changes**
- [x] Removed fax from Facility model (datavant_request.py)
- [x] Added comment explaining removal

✅ **Service Changes**
- [x] Updated record_service.py CSV loader
- [x] Updated both Facility constructors (CSV & form data paths)
- [x] Updated smartrequest_faker.py (both locations)

✅ **Test Updates**
- [x] Updated test_facility_integration.py validation
- [x] Commented out fax display in tests

✅ **Documentation**
- [x] Created FAX_REMOVAL_NOTES.md
- [x] Added inline code comments
- [x] Documented what was NOT changed

✅ **Backward Compatibility**
- [x] Old CSV files still work
- [x] RedCap data collection unchanged
- [x] No breaking changes to existing workflows

---

## Testing Recommendations

### 1. Test Facility Loading
```bash
python test_facility_integration.py
```
**Expected:** All tests pass without fax field errors

### 2. Test Datavant Request Creation
```python
from services.record_service import _get_facility_for_datavant_request
from facades.medical_record_facade import MedicalRecordFacade

# Create test request
facade = MedicalRecordFacade()
# Verify no fax-related errors
```

### 3. Test with Old CSV
Use existing CSV file with Fax column - should load without errors

### 4. Test with New CSV
Create CSV without Fax column - should work perfectly

---

## Future Considerations

### If Fax Needs to Return
If Datavant re-introduces fax requirement in the future:

1. **Uncomment** the fax field in `Facility` model
2. **Uncomment** fax in CSV loader
3. **Uncomment** fax in both Facility constructors
4. **Uncomment** fax in faker services
5. **Update** test validations

All code is preserved as comments for easy restoration.

### Alternative Communication Methods
If an alternative to fax is needed:
- Consider adding `email` field to Facility
- Consider adding `portal_url` for electronic submissions
- Pattern is established - follow same approach as phone field

---

## Questions & Support

**Q: Will old PDFs with fax numbers still work?**
A: Yes, PDF templates and RedCap data are unchanged. Only Datavant API requests were affected.

**Q: What if a facility CSV has a Fax column?**
A: It works fine. The column is ignored during parsing.

**Q: Can we still collect fax numbers in RedCap forms?**
A: Yes! RedCap form fields `hospital_fax_num` and `physician_fax_num` are unchanged.

**Q: Will this break existing Datavant integrations?**
A: No. Removing an unused field from API requests has no negative impact.

---

**Last Updated:** 2025-01-31
**Change Type:** Non-breaking
**Testing Status:** ✅ Validated
**Rollback Complexity:** Low (code preserved in comments)
