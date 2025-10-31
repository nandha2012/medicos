#!/usr/bin/env python
"""
Validation script to ensure our implementation matches the provided Datavant record type arrays.
"""

from app.services.smartrequest_service import SmartRequestService

# Expected record types from the user's specification
EXPECTED_INFANT_TYPES = [
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

EXPECTED_MOM_TYPES = [
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

def validate_record_types():
    """Validate that our implementation matches the expected record types."""
    
    print("🔍 Validating Datavant Record Types Implementation")
    print("=" * 60)
    
    service = SmartRequestService()
    
    # Get actual types from our implementation
    actual_infant_types = service.get_infant_record_types()
    actual_mom_types = service.get_mom_record_types()
    
    print(f"\n📊 COUNTS")
    print(f"Expected infant types: {len(EXPECTED_INFANT_TYPES)}")
    print(f"Actual infant types:   {len(actual_infant_types)}")
    print(f"Expected mom types:    {len(EXPECTED_MOM_TYPES)}")
    print(f"Actual mom types:      {len(actual_mom_types)}")
    
    # Validate infant types
    print(f"\n👶 INFANT TYPES VALIDATION")
    print("-" * 30)
    
    expected_set = set(EXPECTED_INFANT_TYPES)
    actual_set = set(actual_infant_types)
    
    missing_from_actual = expected_set - actual_set
    extra_in_actual = actual_set - expected_set
    
    if missing_from_actual:
        print("❌ Missing from implementation:")
        for item in sorted(missing_from_actual):
            print(f"   - {item}")
    
    if extra_in_actual:
        print("⚠️ Extra in implementation:")
        for item in sorted(extra_in_actual):
            print(f"   - {item}")
    
    if not missing_from_actual and not extra_in_actual:
        print("✅ Infant types match perfectly!")
    
    # Validate mom types  
    print(f"\n👩 MOM TYPES VALIDATION")
    print("-" * 25)
    
    expected_set = set(EXPECTED_MOM_TYPES)
    actual_set = set(actual_mom_types)
    
    missing_from_actual = expected_set - actual_set
    extra_in_actual = actual_set - expected_set
    
    if missing_from_actual:
        print("❌ Missing from implementation:")
        for item in sorted(missing_from_actual):
            print(f"   - {item}")
    
    if extra_in_actual:
        print("⚠️ Extra in implementation:")
        for item in sorted(extra_in_actual):
            print(f"   - {item}")
    
    if not missing_from_actual and not extra_in_actual:
        print("✅ Mom types match perfectly!")
    
    # Summary
    print(f"\n📋 SUMMARY")
    print("-" * 10)
    infant_match = len(missing_from_actual) == 0 and len(extra_in_actual) == 0
    
    expected_set = set(EXPECTED_MOM_TYPES)
    actual_set = set(actual_mom_types)
    missing_from_actual = expected_set - actual_set
    extra_in_actual = actual_set - expected_set
    mom_match = len(missing_from_actual) == 0 and len(extra_in_actual) == 0
    
    if infant_match and mom_match:
        print("🎉 All record types implemented correctly!")
        print("✅ Ready for Datavant API integration")
    else:
        print("⚠️ Some discrepancies found - review above details")
    
    print(f"\n💡 USAGE")
    print("-" * 8)
    print("# For infant requests:")
    print("service = SmartRequestService()")
    print("infant_types = service.get_infant_record_types()")
    print("request_data['requestCriteria'][0]['recordTypes'] = infant_types[:5]  # Select specific types")
    print()
    print("# For mom requests:")
    print("mom_types = service.get_mom_record_types()")
    print("request_data['requestCriteria'][0]['recordTypes'] = mom_types[:3]  # Select specific types")

if __name__ == "__main__":
    validate_record_types()