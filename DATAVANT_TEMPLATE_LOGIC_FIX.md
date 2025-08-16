# Datavant Template Logic Fix

## Problem Identified

The original `get_template_path(request_for)` function correctly selected templates based on the request type:
- **"1"** → Mother template (`mother_template.docx`)
- **"2"** → Infant template (`infant_template.docx`) 
- **Other** → Combined template (`combined_template.docx`)

However, the Datavant request creation logic in `get_datavant_request_data()` was **not connected** to this template selection. It was using generic record types instead of the appropriate mom/infant-specific record types.

## Root Cause

```python
# BEFORE: Template selection worked correctly
def get_template_path(request_for):
    if request_for == "1":
        return "mother_template.docx"  # ✅ Correct template selected
    elif request_for == "2": 
        return "infant_template.docx"  # ✅ Correct template selected

# BUT: Datavant record types were NOT connected to template choice
def get_datavant_request_data(data):
    recordTypes = getattr(data, 'mr_record_types', ['Abstract'])  # ❌ Generic types
```

This created a **logic gap** where the template choice didn't influence the Datavant API request.

## Solution Implemented

### 1. Created Record Type Selection Logic

```python
def get_record_types_for_request(request_for) -> List[str]:
    """Get appropriate Datavant record types based on request type"""
    service = SmartRequestService()
    
    if request_for == "1":
        print("🔍 Using Mom record types for Datavant request")
        return service.get_mom_record_types()  # 28 types
    elif request_for == "2":
        print("🔍 Using Infant record types for Datavant request") 
        return service.get_infant_record_types()  # 33 types
    else:
        print("🔍 Using Combined record types for Datavant request")
        # Combine and deduplicate mom + infant types
        return sorted(list(set(mom_types + infant_types)))  # 34 types
```

### 2. Updated Datavant Request Creation

```python
# BEFORE
def get_datavant_request_data(data: RedcapResponseFirst) -> DatavantRequest:

# AFTER  
def get_datavant_request_data(data: RedcapResponseFirst, request_for: str = None) -> DatavantRequest:
    # Now uses request_for to select appropriate record types
```

### 3. Created Smart Record Type Selection

```python
def _get_record_types_for_datavant_request(data, request_for=None) -> List[str]:
    """Priority-based record type selection"""
    
    # Priority 1: Use request_for if provided (template-based selection)
    if request_for is not None:
        return get_record_types_for_request(request_for)
    
    # Priority 2: Use manual record types if specified
    manual_types = getattr(data, 'mr_record_types', None)
    if manual_types:
        return manual_types if isinstance(manual_types, list) else [manual_types]
    
    # Priority 3: Fallback to combined (safest option)
    return get_record_types_for_request("combined")
```

### 4. Updated All Call Sites

```python
# BEFORE
handle_datavant_request(item, j, "first_request")

# AFTER  
request_for = getattr(data, 'mr_req_for', None)
handle_datavant_request(item, j, "first_request", request_for)
```

## Now The Logic Works Correctly

### Template Selection → Record Type Selection

| Template Choice | `request_for` | Record Types Used | Count |
|---|---|---|---|
| **Mother** | "1" | Mom-specific types (includes ED Records) | 28 |
| **Infant** | "2" | Infant-specific types (includes Cardiology, Speech Therapy) | 33 |
| **Combined** | Other | All available types (mom + infant) | 34 |

### Validation Results

✅ **Mother requests (request_for="1")**:
- Uses 28 mom-specific record types
- Includes "ED Records" (mom-only)
- Excludes infant-only types like "Cardiology Reports"

✅ **Infant requests (request_for="2")**:
- Uses 33 infant-specific record types  
- Includes "Cardiology Reports", "Speech Therapy" (infant-only)
- Excludes mom-only types like "ED Records"

✅ **Combined requests (other)**:
- Uses all 34 available record types
- Includes both mom and infant specific types
- Safe fallback for undefined request types

## Flow Diagram

```
User Form Data (mr_req_for)
        ↓
Template Selection Logic
        ↓
┌─────────────────────────────────────┐
│ request_for = "1" → Mother Template │
│ request_for = "2" → Infant Template │  
│ request_for = other → Combined      │
└─────────────────────────────────────┘
        ↓
Record Type Selection (NEW!)
        ↓
┌─────────────────────────────────────┐
│ "1" → Mom Record Types (28)         │
│ "2" → Infant Record Types (33)      │
│ other → Combined Types (34)         │  
└─────────────────────────────────────┘
        ↓
Datavant API Request with Correct Record Types
```

## Benefits

1. **Consistent Logic**: Template selection now properly drives Datavant record type selection
2. **Appropriate Records**: Requests get relevant record types based on patient type (mom vs infant)
3. **Fallback Safety**: Multiple fallback levels prevent errors
4. **Maintainable**: Clear separation of concerns and documented logic
5. **Testable**: All logic paths have been tested and validated

## Files Modified

- `app/services/record_service.py`: Core logic updates
- `app/services/smartrequest_service.py`: Added mom/infant record type methods (previous update)
- `app/services/smartrequest_faker.py`: Updated with correct record types (previous update)

## Testing

All three request types have been tested and work correctly:
- Mother template → Mom record types ✅
- Infant template → Infant record types ✅  
- Combined template → All record types ✅

The logic gap has been **completely resolved**.