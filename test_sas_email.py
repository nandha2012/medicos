#!/usr/bin/env python3
"""
Test script for SAS Email Service
This script tests the SAS-configured email functionality
"""

import os
import sys
from datetime import datetime

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.sas_email_service import SASEmailService


def test_sas_config_loading():
    """Test SAS configuration loading"""
    print("Testing SAS Email Service Configuration...")
    
    sas_email = SASEmailService()
    smtp_settings = sas_email.get_smtp_settings()
    
    print("\nSAS Email Configuration:")
    print("=" * 30)
    for key, value in smtp_settings.items():
        print(f"{key.capitalize()}: {value}")
    
    print(f"\nSAS Config Path: {sas_email.sas_config_path}")
    
    return sas_email


def test_notification_email(sas_email):
    """Test notification email creation"""
    print("\n📧 Testing MR_DV Notification Email...")
    
    test_record_id = "TEST_RECORD_001_0"
    test_patient_name = "Jane Doe"
    test_facility_name = "Test Hospital"
    
    # Create email body without sending
    body = sas_email._create_email_body(
        record_id=test_record_id,
        patient_name=test_patient_name,
        facility_name=test_facility_name
    )
    
    print("Generated Email Body:")
    print("-" * 40)
    print(body)
    print("-" * 40)
    
    return True


def test_smtp_connection(sas_email):
    """Test SMTP connection"""
    print("\n📋 Testing SMTP Connection...")
    
    success = sas_email.test_connection()
    
    if success:
        print("✅ SMTP connection test passed")
    else:
        print("⚠️ SMTP connection test failed")
    
    return success


def test_record_service_integration():
    """Test integration with record service"""
    print("\n🔗 Testing Record Service Integration...")
    
    try:
        import services.record_service
        print("✅ Record service imports successfully with SAS email service")
        return True
    except Exception as e:
        print(f"❌ Record service import failed: {e}")
        return False


def test_send_notification_demo(sas_email):
    """Demo test for sending notification (with user confirmation)"""
    print("\n✉️ Testing Email Sending...")
    
    # Ask user if they want to send a test email
    test_email = os.getenv('TEST_EMAIL')
    if test_email:
        response = input(f"Send test notification to {test_email}? (y/n): ").lower().strip()
        
        if response == 'y' or response == 'yes':
            success = sas_email.send_mr_dv_notification(
                record_id="TEST_RECORD_001_0",
                patient_name="Jane Test",
                facility_name="Test Facility",
                to_email=test_email
            )
            
            if success:
                print("✅ Test notification sent successfully!")
            else:
                print("❌ Test notification failed to send")
            
            return success
        else:
            print("Test email cancelled by user")
    else:
        print("⚠️ No TEST_EMAIL environment variable set for testing")
        print("Set TEST_EMAIL=your@email.com to test actual email sending")
    
    return True


def main():
    print("SAS Email Service Test")
    print("=" * 25)
    
    try:
        # Test configuration loading
        sas_email = test_sas_config_loading()
        
        # Test notification email generation
        test_notification_email(sas_email)
        
        # Test SMTP connection
        test_smtp_connection(sas_email)
        
        # Test record service integration
        test_record_service_integration()
        
        # Test actual email sending (optional)
        test_send_notification_demo(sas_email)
        
        print("\n✅ All SAS email service tests completed!")
        print("\nConfiguration Summary:")
        print("- Uses SAS sasv9.cfg for SMTP settings")
        print("- Sends notifications when mr_dv != 1")
        print("- Compatible with existing record processing workflow")
        
        print("\nTo customize configuration, set environment variables:")
        print("- SMTP_SERVER (fallback if SAS config not found)")
        print("- SMTP_PORT (fallback if SAS config not found)")
        print("- FROM_EMAIL (fallback if SAS config not found)")
        print("- NOTIFICATION_EMAIL (recipient for alerts)")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()