#!/usr/bin/env python3
"""
Test script for Email Service with Fax Number
This script tests the email service by passing a fax number as parameter
"""

import os
import sys
import argparse
from datetime import datetime

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.email_service import EmailService


def test_email_with_fax(fax_number: str, test_email: str = None, use_outlook: bool = True):
    """
    Test email service with fax number
    
    Args:
        fax_number: The fax number to include in the test
        test_email: Email address to send test to (optional)
        use_outlook: Whether to use Outlook or SMTP
    """
    print(f"Testing Email Service with Fax Number: {fax_number}")
    print("=" * 50)
    
    try:
        # Initialize email service
        email_service = EmailService(use_outlook=use_outlook)
        
        # Create test data with fax number
        test_record_id = f"FAX_{fax_number}_RECORD_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        test_patient_name = "Test Patient"
        test_facility_name = f"Facility (Fax: {fax_number})"
        
        print(f"\nTest Parameters:")
        print(f"- Record ID: {test_record_id}")
        print(f"- Patient Name: {test_patient_name}")
        print(f"- Facility Name: {test_facility_name}")
        print(f"- Fax Number: {fax_number}")
        print(f"- Email Method: {'Outlook' if use_outlook else 'SMTP'}")
        
        # Test email body generation
        print(f"\n📧 Generating Email Body...")
        body = email_service._create_email_body_from_template(
            record_id=test_record_id,
            patient_name=test_patient_name,
            facility_name=test_facility_name
        )
        
        # Add fax number to email body
        body += f"\nFax Number: {fax_number}"
        
        print("Generated Email Body:")
        print("-" * 40)
        print(body)
        print("-" * 40)
        
        # Test email sending if test email is provided
        if test_email:
            print(f"\n✉️ Sending test email to: {test_email}")
            success = email_service.send_mr_dv_notification(
                record_id=test_record_id,
                patient_name=test_patient_name,
                facility_name=test_facility_name,
                to_email=test_email
            )
            
            if success:
                print("✅ Test email sent successfully!")
                return True
            else:
                print("❌ Test email failed to send")
                return False
        else:
            print("\n⚠️ No test email provided - email body generated but not sent")
            print("Use --email parameter to actually send the test email")
            return True
            
    except Exception as e:
        print(f"❌ Error testing email service: {e}")
        import traceback
        traceback.print_exc()
        return False


def validate_fax_number(fax_number: str) -> bool:
    """
    Validate fax number format
    
    Args:
        fax_number: The fax number to validate
        
    Returns:
        bool: True if valid format
    """
    # Remove common separators
    cleaned = fax_number.replace("-", "").replace("(", "").replace(")", "").replace(" ", "").replace(".", "")
    
    # Check if it's all digits and reasonable length
    if cleaned.isdigit() and 7 <= len(cleaned) <= 15:
        return True
    
    return False


def main():
    parser = argparse.ArgumentParser(description='Test Email Service with Fax Number')
    parser.add_argument('fax_number', help='Fax number to test with')
    parser.add_argument('--email', '-e', help='Test email address to send to')
    parser.add_argument('--smtp', action='store_true', help='Use SMTP instead of Outlook')
    parser.add_argument('--validate', action='store_true', help='Validate fax number format')
    
    args = parser.parse_args()
    
    # Validate fax number if requested
    if args.validate:
        if validate_fax_number(args.fax_number):
            print(f"✅ Fax number '{args.fax_number}' is valid format")
        else:
            print(f"⚠️ Fax number '{args.fax_number}' may not be valid format")
            response = input("Continue anyway? (y/n): ").lower().strip()
            if response not in ['y', 'yes']:
                print("Test cancelled")
                return
    
    # Get test email from environment if not provided
    test_email = args.email or os.getenv('TEST_EMAIL')
    
    if not test_email:
        print("⚠️ No test email provided")
        print("Either use --email parameter or set TEST_EMAIL environment variable")
        print("Email body will be generated but not sent")
    
    # Run the test
    use_outlook = not args.smtp
    success = test_email_with_fax(args.fax_number, test_email, use_outlook)
    
    if success:
        print(f"\n✅ Email service test completed successfully with fax: {args.fax_number}")
    else:
        print(f"\n❌ Email service test failed with fax: {args.fax_number}")
        sys.exit(1)


if __name__ == "__main__":
    main()