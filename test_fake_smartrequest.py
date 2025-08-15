#!/usr/bin/env python
"""
Test script to verify SmartRequest faker integration with the main workflow
"""

import os
import sys
from dotenv import load_dotenv

# Add app directory to path
sys.path.append('app')

# Load environment variables
load_dotenv()

# Ensure we're in faker mode
os.environ['ENV'] = 'local'

from app.services.external_api_service import submit_datavant_request
from app.services.smartrequest_faker import create_fake_smartrequest_payload
from app.models.datavant_request import DatavantRequest

def test_smartrequest_integration():
    """Test the full SmartRequest integration with faker"""
    print("🚀 Testing SmartRequest Integration with Faker")
    print("=" * 50)
    
    # Create a fake SmartRequest payload
    print("📝 Creating fake SmartRequest payload...")
    fake_payload = create_fake_smartrequest_payload()
    
    print(f"   Patient: {fake_payload['patient']['firstName']} {fake_payload['patient']['lastName']}")
    print(f"   Facility: {fake_payload['facility']['siteName']}")
    print(f"   Record Types: {', '.join(fake_payload['requestCriteria'][0]['recordTypes'])}")
    
    # Convert to DatavantRequest model
    print("\n🔧 Converting to DatavantRequest model...")
    try:
        datavant_request = DatavantRequest(**fake_payload)
        print("   ✅ Model validation successful")
    except Exception as e:
        print(f"   ❌ Model validation failed: {e}")
        return False
    
    # Submit the request using the external API service
    print("\n🚀 Submitting SmartRequest...")
    try:
        response = submit_datavant_request(datavant_request)
        
        if response:
            request_id = response.get('requestId')
            print(f"   ✅ Request created successfully!")
            print(f"   📝 Request ID: {request_id}")
            print(f"   👤 Patient: {response.get('patient', {}).get('firstName')} {response.get('patient', {}).get('lastName')}")
            print(f"   🏥 Facility: {response.get('facility', {}).get('siteName')}")
            return True
        else:
            print("   ❌ Request creation failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Request submission failed: {e}")
        return False

def test_request_tracking():
    """Test the request tracking functionality"""
    print("\n📋 Testing Request Tracking...")
    
    from app.utils.request_tracker import track_smartrequest, request_tracker
    
    # Add a fake tracked request
    fake_request_id = "FAKE_12345"
    fake_record_id = "TEST_RECORD_001"
    
    success = track_smartrequest(
        request_id=fake_request_id,
        record_id=fake_record_id,
        document_type="test_request",
        patient_name="John Doe",
        facility_name="Test Medical Center"
    )
    
    if success:
        print("   ✅ Request tracking successful")
        
        # Retrieve the tracked request
        tracked_request = request_tracker.get_request(fake_request_id)
        if tracked_request:
            print(f"   📝 Retrieved: {tracked_request.request_id} -> {tracked_request.record_id}")
            print(f"   👤 Patient: {tracked_request.patient_name}")
            print(f"   🏥 Facility: {tracked_request.facility_name}")
            return True
        else:
            print("   ❌ Failed to retrieve tracked request")
            return False
    else:
        print("   ❌ Request tracking failed")
        return False

def main():
    """Main test function"""
    all_tests_passed = True
    
    # Test SmartRequest integration
    if not test_smartrequest_integration():
        all_tests_passed = False
    
    # Test request tracking
    if not test_request_tracking():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All tests passed! SmartRequest faker integration is working correctly.")
        print("\nYou can now:")
        print("  • Run your normal document workflows with SmartRequest integration")
        print("  • Use ENV=local to automatically use faker mode")
        print("  • Set USE_SMARTREQUEST_FAKER=true to force faker mode")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)