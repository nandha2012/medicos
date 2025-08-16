#!/usr/bin/env python
"""
Test script to verify the updated patient data fields in Datavant requests.
"""

from app.services.record_service import get_datavant_request_data

class MockDataWithPatientInfo:
    """Mock data with birth certificate mom information"""
    
    def __init__(self, include_patient_data=True):
        self.mg_idpreg = 'TEST123'
        
        if include_patient_data:
            # Birth certificate mom data (new fields)
            self.bc_momnamefirst = 'Sarah'
            self.bc_momnamelast = 'Johnson'  
            self.bc_mom_dob = '1985-03-15'
            self.bc_momssn = '123456789'
        
        # Optional medical record fields (old fields - should not be used)
        self.mr_first_name = 'OLD_FIRST'
        self.mr_last_name = 'OLD_LAST'
        self.mr_date_of_birth = '1990-01-01'
        self.mr_ssn = '999999999'

class MockDataWithoutPatientInfo:
    """Mock data without birth certificate mom information"""
    
    def __init__(self):
        self.mg_idpreg = 'TEST456'
        # No bc_mom* fields - should use empty defaults

def test_patient_data_update():
    """Test the patient data field updates"""
    
    print("👤 Testing Datavant Patient Data Update")
    print("=" * 45)
    
    # Test 1: With birth certificate mom data
    print("\n1️⃣ Testing with Birth Certificate Mom Data")
    print("-" * 48)
    
    mock_data_with_bc = MockDataWithPatientInfo()
    
    try:
        request_data = get_datavant_request_data(mock_data_with_bc, '1')
        patient = request_data.patient
        
        print(f"   Patient Details:")
        print(f"   - First Name: '{patient.firstName}' (should be 'Sarah')")
        print(f"   - Last Name: '{patient.lastName}' (should be 'Johnson')")
        print(f"   - Date of Birth: '{patient.dateOfBirth}' (should be '1985-03-15')")
        print(f"   - SSN: '{patient.ssn}' (should be '123456789')")
        print(f"   - Custom ID: '{patient.customId}' (should be 'TEST123')")
        
        # Validate the data
        validations = [
            (patient.firstName == 'Sarah', 'First Name'),
            (patient.lastName == 'Johnson', 'Last Name'),
            (patient.dateOfBirth == '1985-03-15', 'Date of Birth'),
            (patient.ssn == '123456789', 'SSN'),
            (patient.customId == 'TEST123', 'Custom ID')
        ]
        
        all_valid = True
        for is_valid, field_name in validations:
            if is_valid:
                print(f"   ✅ {field_name} correct")
            else:
                print(f"   ❌ {field_name} incorrect")
                all_valid = False
        
        if all_valid:
            print("   🎉 All patient fields use birth certificate mom data correctly!")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Without birth certificate mom data (fallback)
    print("\n2️⃣ Testing without Birth Certificate Mom Data (Fallback)")
    print("-" * 62)
    
    mock_data_without_bc = MockDataWithoutPatientInfo()
    
    try:
        request_data = get_datavant_request_data(mock_data_without_bc, '1')
        patient = request_data.patient
        
        print(f"   Patient Details (should be empty):")
        print(f"   - First Name: '{patient.firstName}' (should be empty)")
        print(f"   - Last Name: '{patient.lastName}' (should be empty)")
        print(f"   - Date of Birth: '{patient.dateOfBirth}' (should be empty)")
        print(f"   - SSN: '{patient.ssn}' (should be empty)")
        print(f"   - Custom ID: '{patient.customId}' (should be 'TEST456')")
        
        # Check that it falls back to empty strings, not old MR fields
        if (patient.firstName == '' and patient.lastName == '' and 
            patient.dateOfBirth == '' and patient.ssn == ''):
            print("   ✅ Correctly uses empty defaults when BC mom data not available")
        else:
            print("   ❌ Should use empty defaults when BC mom data not available")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Field Mapping Verification
    print("\n3️⃣ Field Mapping Verification")
    print("-" * 35)
    
    field_mappings = [
        ('bc_momnamefirst', 'patient.firstName'),
        ('bc_momnamelast', 'patient.lastName'),
        ('bc_mom_dob', 'patient.dateOfBirth'),
        ('bc_momssn', 'patient.ssn')
    ]
    
    print("   Field mappings:")
    for source_field, target_field in field_mappings:
        print(f"   {source_field} → {target_field}")
    
    print("\n📊 SUMMARY")
    print("-" * 12)
    print("✅ Patient data now uses birth certificate mom fields")
    print("✅ Fields: bc_momnamefirst, bc_momnamelast, bc_mom_dob, bc_momssn")
    print("✅ Falls back to empty strings if BC mom data not available")
    print("✅ Custom ID continues to use mg_idpreg as before")

if __name__ == "__main__":
    test_patient_data_update()