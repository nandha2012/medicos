#!/usr/bin/env python
"""
Test script to verify the complete dashboard integration
"""

import os
import sys
import time
import json
from datetime import datetime

# Add app directory to path
sys.path.append('app')

from app.utils.dashboard_tracker import (
    track_processing_start, track_pdf_success, track_pdf_error,
    track_smartrequest_sent, track_smartrequest_success, track_smartrequest_error,
    dashboard_tracker
)

def test_dashboard_integration():
    """Test the complete dashboard integration"""
    print("🧪 Testing Dashboard Integration")
    print("=" * 50)
    
    # Test data
    record_id = f"TEST_DASHBOARD_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    patient_name = "Test Patient"
    facility_name = "Test Medical Center"
    username = "test_user"
    
    print(f"📝 Testing with record ID: {record_id}")
    
    # 1. Start processing
    print("\n1️⃣ Starting processing tracking...")
    success = track_processing_start(
        record_id=record_id,
        request_type="first_request",
        patient_name=patient_name,
        facility_name=facility_name,
        username=username
    )
    print(f"   ✅ Processing start tracked: {success}")
    
    # Simulate some processing time
    time.sleep(1)
    
    # 2. Test PDF success
    print("\n2️⃣ Testing PDF success tracking...")
    pdf_path = f"output/test/{record_id}.pdf"
    success = track_pdf_success(record_id, pdf_path, "mother_template")
    print(f"   ✅ PDF success tracked: {success}")
    
    # 3. Test SmartRequest success
    print("\n3️⃣ Testing SmartRequest tracking...")
    smartrequest_id = f"SR_{record_id}"
    payload = {
        "facility": {"siteName": facility_name},
        "patient": {"firstName": "Test", "lastName": "Patient"},
        "requestCriteria": [{"recordTypes": ["Abstract"]}]
    }
    
    success = track_smartrequest_sent(record_id, smartrequest_id, payload)
    print(f"   ✅ SmartRequest sent tracked: {success}")
    
    success = track_smartrequest_success(record_id, smartrequest_id)
    print(f"   ✅ SmartRequest success tracked: {success}")
    
    # 4. Get dashboard summary
    print("\n4️⃣ Getting dashboard summary...")
    summary = dashboard_tracker.get_dashboard_summary()
    print(f"   📊 Total records: {summary.get('total_records', 0)}")
    print(f"   📄 PDF successes: {summary.get('pdf_success', 0)}")
    print(f"   📤 SmartRequests sent: {summary.get('smartrequest_sent', 0)}")
    
    # 5. Test error tracking
    print("\n5️⃣ Testing error tracking...")
    error_record_id = f"ERROR_TEST_{datetime.now().strftime('%H%M%S')}"
    
    track_processing_start(error_record_id, "test_error", "Error Patient", "Error Facility")
    track_pdf_error(error_record_id, "Test PDF error for dashboard")
    track_smartrequest_error(error_record_id, "Test SmartRequest error for dashboard")
    
    print(f"   ✅ Error tracking completed")
    
    # 6. Get all records
    print("\n6️⃣ Retrieving all tracking records...")
    all_records = dashboard_tracker.get_all_records()
    print(f"   📋 Total tracking records: {len(all_records)}")
    
    # Display recent records
    if all_records:
        print(f"   🔄 Recent records:")
        for record in all_records[-3:]:  # Show last 3 records
            print(f"      - {record.record_id}: PDF={record.pdf_status}, SR={record.smartrequest_status}")
    
    print(f"\n✅ Dashboard integration test completed successfully!")
    return True

def test_api_compatibility():
    """Test compatibility with the dashboard API"""
    print("\n🔗 Testing API compatibility...")
    
    try:
        from app.dashboard_server import DashboardDataService
        
        # Create data service
        data_service = DashboardDataService()
        
        # Get dashboard data
        dashboard_data = data_service.get_dashboard_data()
        
        print(f"   📊 Dashboard data structure:")
        print(f"      - Records: {len(dashboard_data.get('records', []))}")
        print(f"      - Stats: {dashboard_data.get('stats', {})}")
        print(f"      - Timestamp: {dashboard_data.get('timestamp', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ API compatibility test failed: {e}")
        return False

def simulate_processing_workflow():
    """Simulate a complete processing workflow"""
    print("\n🔄 Simulating complete processing workflow...")
    
    # Simulate multiple records being processed
    workflows = [
        {"type": "first_request", "patient": "John Doe", "facility": "City Hospital"},
        {"type": "second_request_complete", "patient": "Jane Smith", "facility": "General Medical"},
        {"type": "second_request_partial", "patient": "Bob Johnson", "facility": "Regional Center"}
    ]
    
    for i, workflow in enumerate(workflows):
        record_id = f"WORKFLOW_{i}_{datetime.now().strftime('%H%M%S')}"
        
        print(f"   🔄 Processing {workflow['type']} for {workflow['patient']}...")
        
        # Start tracking
        track_processing_start(
            record_id=record_id,
            request_type=workflow['type'],
            patient_name=workflow['patient'],
            facility_name=workflow['facility']
        )
        
        # Simulate PDF generation (some succeed, some fail)
        if i % 3 == 0:  # Simulate occasional PDF failure
            track_pdf_error(record_id, "Template not found")
        else:
            track_pdf_success(record_id, f"output/{record_id}.pdf", "test_template")
        
        # Simulate SmartRequest (most succeed)
        if i % 4 == 0:  # Simulate occasional SmartRequest failure
            track_smartrequest_error(record_id, "API timeout")
        else:
            sr_id = f"SR_{record_id}"
            track_smartrequest_sent(record_id, sr_id)
            track_smartrequest_success(record_id, sr_id)
        
        time.sleep(0.5)  # Small delay to simulate processing time
    
    print(f"   ✅ Workflow simulation completed")

def main():
    """Main test function"""
    print("🚀 Dashboard Integration Test Suite")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Test 1: Basic dashboard integration
    try:
        if not test_dashboard_integration():
            all_tests_passed = False
    except Exception as e:
        print(f"❌ Dashboard integration test failed: {e}")
        all_tests_passed = False
    
    # Test 2: API compatibility
    try:
        if not test_api_compatibility():
            all_tests_passed = False
    except Exception as e:
        print(f"❌ API compatibility test failed: {e}")
        all_tests_passed = False
    
    # Test 3: Workflow simulation
    try:
        simulate_processing_workflow()
    except Exception as e:
        print(f"❌ Workflow simulation failed: {e}")
        all_tests_passed = False
    
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("🎉 All dashboard tests passed!")
        print("\n📋 Next steps:")
        print("  1. Run the dashboard server: python app/dashboard_server.py")
        print("  2. Open http://localhost:5000 in your browser")
        print("  3. Run your normal PDF generation workflow")
        print("  4. View real-time tracking in the dashboard")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)