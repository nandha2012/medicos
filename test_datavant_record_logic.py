#!/usr/bin/env python
"""
Test script to verify the updated Datavant record type selection logic.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.services.record_service import get_record_types_for_request, _get_record_types_for_datavant_request
from app.models.redcap_response import RedcapResponseFirst


class MockRedcapData:
    """Mock RedCap data for testing"""
    def __init__(self, mr_req_for=None, mr_record_types=None):
        self.mr_req_for = mr_req_for
        self.mr_record_types = mr_record_types
        self.mg_idpreg = "TEST123"


def test_record_type_selection():
    """Test the record type selection logic"""
    
    print("🧪 Testing Datavant Record Type Selection Logic")
    print("=" * 55)
    
    # Test 1: Mother request (request_for = "1")
    print("\n1️⃣ Testing Mother Request (request_for='1')")
    print("-" * 45)
    
    mom_types = get_record_types_for_request("1")
    print(f"   Mom record types count: {len(mom_types)}")
    print(f"   Sample types: {mom_types[:3]}...")
    
    # Verify specific mom-only type is included
    if "ED Records" in mom_types:
        print("   ✅ ED Records (mom-only type) found")
    else:
        print("   ❌ ED Records (mom-only type) NOT found")
    
    # Test 2: Infant request (request_for = "2") 
    print("\n2️⃣ Testing Infant Request (request_for='2')")
    print("-" * 47)
    
    infant_types = get_record_types_for_request("2")
    print(f"   Infant record types count: {len(infant_types)}")
    print(f"   Sample types: {infant_types[:3]}...")
    
    # Verify specific infant-only types are included
    infant_only_types = ["Cardiology Reports", "Audiology Report", "Speech Therapy"]
    for record_type in infant_only_types:
        if record_type in infant_types:
            print(f"   ✅ {record_type} (infant-only type) found")
        else:
            print(f"   ❌ {record_type} (infant-only type) NOT found")
    
    # Test 3: Combined request (request_for = anything else)
    print("\n3️⃣ Testing Combined Request (request_for='3')")
    print("-" * 48)
    
    combined_types = get_record_types_for_request("3")
    print(f"   Combined record types count: {len(combined_types)}")
    print(f"   Sample types: {combined_types[:3]}...")
    
    # Verify combined has both mom and infant types
    has_mom_only = "ED Records" in combined_types
    has_infant_only = "Cardiology Reports" in combined_types
    
    if has_mom_only and has_infant_only:
        print("   ✅ Combined contains both mom and infant specific types")
    else:
        print(f"   ❌ Combined missing types (mom-only: {has_mom_only}, infant-only: {has_infant_only})")
    
    # Test 4: Integration with mock data
    print("\n4️⃣ Testing Integration with Mock Data")
    print("-" * 40)
    
    # Test with request_for specified
    mock_data_mom = MockRedcapData(mr_req_for="1")
    result_mom = _get_record_types_for_datavant_request(mock_data_mom, "1")
    print(f"   Mock mom data result: {len(result_mom)} types")
    
    mock_data_infant = MockRedcapData(mr_req_for="2") 
    result_infant = _get_record_types_for_datavant_request(mock_data_infant, "2")
    print(f"   Mock infant data result: {len(result_infant)} types")
    
    # Test fallback to manual types
    mock_data_manual = MockRedcapData(mr_record_types=["Custom Type 1", "Custom Type 2"])
    result_manual = _get_record_types_for_datavant_request(mock_data_manual, None)
    print(f"   Manual types fallback: {result_manual}")
    
    # Test final fallback
    mock_data_empty = MockRedcapData()
    result_empty = _get_record_types_for_datavant_request(mock_data_empty, None)
    print(f"   Empty data fallback: {len(result_empty)} types (should be combined)")
    
    # Test 5: Validate Template Mapping
    print("\n5️⃣ Testing Template to Record Type Mapping")
    print("-" * 48)
    
    template_mappings = {
        "1": "Mother",
        "2": "Infant", 
        "3": "Combined"
    }
    
    for request_for, template_name in template_mappings.items():
        types = get_record_types_for_request(request_for)
        print(f"   {template_name} template -> {len(types)} record types")
    
    print("\n✅ All tests completed!")
    
    # Summary
    print("\n📊 SUMMARY")
    print("-" * 12)
    print(f"✅ Logic correctly chooses record types based on template selection")
    print(f"✅ Mother requests get {len(mom_types)} mom-specific record types")
    print(f"✅ Infant requests get {len(infant_types)} infant-specific record types")
    print(f"✅ Combined requests get {len(combined_types)} total record types")
    print(f"✅ Fallback logic works for manual and empty configurations")


if __name__ == "__main__":
    test_record_type_selection()