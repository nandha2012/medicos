#!/usr/bin/env python
"""
Test script to verify the Datavant facility CSV integration.
"""

from app.services.record_service import load_datavant_facilities, get_facility_by_site, get_first_facility

def test_facility_loading():
    """Test facility CSV loading functionality"""
    
    print("🏥 Testing Datavant Facility CSV Integration")
    print("=" * 50)
    
    # Test 1: Load all facilities
    print("\n1️⃣ Testing CSV Loading")
    print("-" * 25)
    
    facilities = load_datavant_facilities()
    print(f"   Loaded {len(facilities)} facilities from CSV")
    
    if facilities:
        print("   ✅ CSV loading successful")
        
        # Show first few facilities
        print("\n   Sample facilities:")
        for i, facility in enumerate(facilities[:3]):
            print(f"   {i+1}. Site: {facility['site']}, Name: {facility['siteName']}")
            print(f"      Address: {facility['addressLine1']}, {facility['city']}, {facility['state']}")
    else:
        print("   ❌ CSV loading failed")
        return
    
    # Test 2: Get first facility
    print("\n2️⃣ Testing First Facility Lookup")
    print("-" * 35)
    
    first_facility = get_first_facility()
    if first_facility:
        print("   ✅ First facility lookup successful")
        print(f"   Site: {first_facility['site']}")
        print(f"   Name: {first_facility['siteName']}")
        print(f"   Health System: {first_facility['healthSystem']}")
        print(f"   Address: {first_facility['addressLine1']}")
        if first_facility['addressLine2']:
            print(f"            {first_facility['addressLine2']}")
        print(f"            {first_facility['city']}, {first_facility['state']} {first_facility['zip']}")
        print(f"   Phone: {first_facility['phone']}")
        print(f"   Fax: {first_facility['fax']}")
    else:
        print("   ❌ First facility lookup failed")
    
    # Test 3: Lookup by site number
    print("\n3️⃣ Testing Site Number Lookup")
    print("-" * 33)
    
    # Test with the first facility's site number
    if first_facility:
        test_site = first_facility['site']
        found_facility = get_facility_by_site(test_site)
        
        if found_facility and found_facility['site'] == test_site:
            print(f"   ✅ Site lookup successful for {test_site}")
            print(f"   Found: {found_facility['siteName']}")
        else:
            print(f"   ❌ Site lookup failed for {test_site}")
    
    # Test with a non-existent site
    fake_site = "99999"
    not_found = get_facility_by_site(fake_site)
    if not_found is None:
        print(f"   ✅ Correctly returned None for non-existent site {fake_site}")
    else:
        print(f"   ❌ Should have returned None for non-existent site {fake_site}")
    
    # Test 4: Data format validation
    print("\n4️⃣ Testing Data Format")
    print("-" * 24)
    
    if first_facility:
        required_fields = ['site', 'siteName', 'healthSystem', 'addressLine1', 'city', 'state', 'zip', 'phone', 'fax']
        missing_fields = []
        
        for field in required_fields:
            if field not in first_facility:
                missing_fields.append(field)
        
        if not missing_fields:
            print("   ✅ All required fields present")
        else:
            print(f"   ❌ Missing fields: {missing_fields}")
        
        # Check for empty critical fields
        critical_fields = ['site', 'siteName', 'city', 'state']
        empty_fields = []
        
        for field in critical_fields:
            if not first_facility.get(field, '').strip():
                empty_fields.append(field)
        
        if not empty_fields:
            print("   ✅ All critical fields have values")
        else:
            print(f"   ⚠️ Empty critical fields: {empty_fields}")
    
    print("\n📊 SUMMARY")
    print("-" * 12)
    
    if facilities and first_facility:
        print("✅ Facility CSV integration working correctly!")
        print(f"✅ Ready to use {len(facilities)} facilities from Datavant CSV")
        print("✅ First facility will be used as default for Datavant requests")
        print(f"✅ Default facility: {first_facility['siteName']} (Site: {first_facility['site']})")
    else:
        print("❌ Facility integration has issues - review above errors")

if __name__ == "__main__":
    test_facility_loading()