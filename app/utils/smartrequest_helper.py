#!/usr/bin/env python
"""
SmartRequest Helper Utilities
Provides helper functions for managing SmartRequest operations
"""

import os
import sys
from typing import Optional, List, Dict, Any

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from services.smartrequest_service import SmartRequestService
from services.external_api_service import get_smartrequest_status, get_smartrequest_download_url, cancel_smartrequest


def validate_smartrequest_config() -> bool:
    """
    Validate that all required SmartRequest configuration is present
    
    Returns:
        bool: True if configuration is valid, False otherwise
    """
    required_vars = [
        'SMARTREQUEST_BASE_URL',
        'SMARTREQUEST_CLIENT_ID',
        'SMARTREQUEST_CLIENT_SECRET'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print(f"📝 Please check your .env file or set these environment variables")
        return False
    
    return True


def test_smartrequest_connection() -> bool:
    """
    Test connection to SmartRequest API
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    if not validate_smartrequest_config():
        return False
    
    try:
        service = SmartRequestService()
        success = service.authenticate()
        
        if success:
            print("✅ SmartRequest API connection successful")
            
            # Test fetching record types as a quick health check
            record_types = service.get_record_types()
            if record_types:
                print(f"📋 Found {len(record_types)} available record types")
            
        return success
        
    except Exception as e:
        print(f"❌ SmartRequest connection test failed: {e}")
        return False


def list_available_record_types() -> List[Dict[str, Any]]:
    """
    Get and display available record types from SmartRequest API
    
    Returns:
        List of record types
    """
    if not validate_smartrequest_config():
        return []
    
    try:
        service = SmartRequestService()
        if not service.authenticate():
            return []
            
        record_types = service.get_record_types()
        
        if record_types:
            print("📋 Available Record Types:")
            for record_type in record_types:
                name = record_type.get('name', 'Unknown')
                digital = record_type.get('digitalFulfillment', False)
                print(f"   - {name} {'(Digital)' if digital else '(Physical)'}")
        else:
            print("⚠️ No record types found")
            
        return record_types
        
    except Exception as e:
        print(f"❌ Error fetching record types: {e}")
        return []


def search_facilities(filters: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
    """
    Search facilities with optional filters
    
    Args:
        filters: Optional dictionary of search filters
        
    Returns:
        List of facilities
    """
    if not validate_smartrequest_config():
        return []
    
    try:
        service = SmartRequestService()
        if not service.authenticate():
            return []
            
        facilities = service.get_facilities(filters)
        
        if facilities:
            print(f"🏥 Found {len(facilities)} facilities")
            if len(facilities) <= 5:  # Show details for small results
                for facility in facilities:
                    site_name = facility.get('siteName', 'Unknown')
                    city = facility.get('city', '')
                    state = facility.get('state', '')
                    print(f"   - {site_name} ({city}, {state})")
        else:
            print("⚠️ No facilities found")
            
        return facilities
        
    except Exception as e:
        print(f"❌ Error searching facilities: {e}")
        return []


def get_request_reasons_for_company(company_id: int) -> List[Dict[str, Any]]:
    """
    Get available request reasons for a company
    
    Args:
        company_id: Company ID to get reasons for
        
    Returns:
        List of request reasons
    """
    if not validate_smartrequest_config():
        return []
    
    try:
        service = SmartRequestService()
        if not service.authenticate():
            return []
            
        reasons = service.get_request_reasons(company_id)
        
        if reasons:
            print(f"📋 Available Request Reasons for Company {company_id}:")
            for reason in reasons:
                name = reason.get('name', 'Unknown')
                business_type = reason.get('businessType', '')
                api_code = reason.get('apiCode', '')
                states = reason.get('facilityStates', [])
                
                print(f"   - {name} ({business_type})")
                print(f"     API Code: {api_code}")
                print(f"     States: {', '.join(states) if states != ['ALL'] else 'All States'}")
        else:
            print("⚠️ No request reasons found")
            
        return reasons
        
    except Exception as e:
        print(f"❌ Error fetching request reasons: {e}")
        return []


if __name__ == "__main__":
    """Command line interface for SmartRequest utilities"""
    if len(sys.argv) < 2:
        print("Usage: python smartrequest_helper.py <command> [args...]")
        print("Commands:")
        print("  test                    - Test SmartRequest API connection")
        print("  record-types           - List available record types")
        print("  facilities [state]     - Search facilities, optionally by state")
        print("  reasons <company_id>   - Get request reasons for company")
        print("  status <request_id>    - Get status of a request")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "test":
        success = test_smartrequest_connection()
        sys.exit(0 if success else 1)
        
    elif command == "record-types":
        list_available_record_types()
        
    elif command == "facilities":
        filters = {}
        if len(sys.argv) > 2:
            filters['state'] = sys.argv[2].upper()
        search_facilities(filters)
        
    elif command == "reasons":
        if len(sys.argv) < 3:
            print("❌ Company ID required")
            sys.exit(1)
        try:
            company_id = int(sys.argv[2])
            get_request_reasons_for_company(company_id)
        except ValueError:
            print("❌ Invalid company ID")
            sys.exit(1)
            
    elif command == "status":
        if len(sys.argv) < 3:
            print("❌ Request ID required")
            sys.exit(1)
        request_id = sys.argv[2]
        status = get_smartrequest_status(request_id)
        if status:
            print(f"📋 Request {request_id} Status:")
            print(f"   Status: {status.get('status', 'Unknown')}")
            print(f"   Modified: {status.get('modifiedDate', 'Unknown')}")
        else:
            print(f"❌ Could not get status for request {request_id}")
            
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)