#!/usr/bin/env python3
"""
Test script for the email service functionality
This script tests the mr_dv email notification feature
"""

import os
import sys
from datetime import datetime

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.email_service import EmailService


def test_email_service():
    """Test the email service with mock data"""
    print("Testing Email Service for MR_DV notifications...")
    
    # Create email service instance
    email_service = EmailService()
    
    # Test data
    test_record_id = "TEST_RECORD_001_0"
    test_patient_name = "Jane Doe"
    test_facility_name = "Test Hospital"
    
    # You can set a test email here or use environment variable
    test_email = os.getenv('TEST_EMAIL')  # Set this in your environment
    
    if not test_email:
        print("⚠️ No TEST_EMAIL environment variable set. Will use NOTIFICATION_EMAIL if configured.")
        print("To test with a specific email, run: TEST_EMAIL=your@email.com python test_email_service.py")
    
    print(f"\nTest Parameters:")
    print(f"Record ID: {test_record_id}")
    print(f"Patient Name: {test_patient_name}")
    print(f"Facility Name: {test_facility_name}")
    print(f"Target Email: {test_email or 'From NOTIFICATION_EMAIL env var'}")
    
    # Send test email
    success = email_service.send_mr_dv_notification(
        record_id=test_record_id,
        patient_name=test_patient_name,
        facility_name=test_facility_name,
        to_email=test_email
    )
    
    if success:
        print("✅ Test email sent successfully!")
        print("Check the recipient's inbox for the MR_DV notification email.")
    else:
        print("❌ Test email failed to send.")
        print("Check your email configuration in environment variables.")
        print("\nRequired environment variables:")
        print("- SMTP_SERVER (e.g., smtp.gmail.com)")
        print("- SMTP_PORT (e.g., 587)")
        print("- SMTP_USERNAME (your email)")
        print("- SMTP_PASSWORD (your app password)")
        print("- FROM_EMAIL (sender email)")
        print("- NOTIFICATION_EMAIL (recipient email)")
    
    return success


def show_config_status():
    """Show the current email configuration status"""
    print("Current Email Configuration Status:")
    print("=" * 40)
    
    # Create EmailService to check configuration
    email_service = EmailService()
    
    print(f"✅ Sender Email: {email_service.from_email}")
    print(f"✅ Notification Email: {email_service.notification_email or 'Not configured'}")
    print(f"✅ Email Subject: {email_service.email_subject}")
    print(f"✅ Use Outlook: {email_service.use_outlook}")
    print(f"✅ Template Length: {len(email_service.email_template)} characters")
    
    if email_service.use_outlook:
        print("✅ Email Method: Outlook (local application)")
    else:
        print("⚠️ Email Method: SMTP fallback")
        print(f"  SMTP Server: {email_service.smtp_server}")
        print(f"  SMTP Port: {email_service.smtp_port}")
    
    print("\nConfiguration loaded from:")
    print("- SASS file: config/email_config.sass")
    print("- HSB template: templates/email_body.hsb")


if __name__ == "__main__":
    print("MR_DV Email Notification Test")
    print("=" * 30)
    
    # Show current configuration
    show_config_status()
    print()
    
    # Ask user if they want to proceed with the test
    user_input = input("Do you want to proceed with the email test? (y/n): ").lower().strip()
    
    if user_input == 'y' or user_input == 'yes':
        success = test_email_service()
        sys.exit(0 if success else 1)
    else:
        print("Test cancelled by user.")
        sys.exit(0)