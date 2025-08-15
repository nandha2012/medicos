#!/usr/bin/env python
"""
SmartRequest Integration Setup Verification Script
Run this to verify your SmartRequest integration is properly configured
"""

import os
import sys
from dotenv import load_dotenv

def check_environment():
    """Check if environment variables are properly set"""
    print("🔍 Checking environment configuration...")
    
    load_dotenv()
    
    required_vars = [
        'SMARTREQUEST_BASE_URL',
        'SMARTREQUEST_CLIENT_ID', 
        'SMARTREQUEST_CLIENT_SECRET'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            # Mask sensitive values for display
            if 'SECRET' in var or 'TOKEN' in var:
                display_value = f"{value[:8]}..." if len(value) > 8 else "***"
            else:
                display_value = value
            print(f"  ✅ {var} = {display_value}")
    
    if missing_vars:
        print(f"\n❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n📝 Please check your .env file or set these environment variables")
        return False
    
    print("\n✅ Environment configuration looks good!")
    return True

def check_imports():
    """Check if all required modules can be imported"""
    print("\n🔍 Checking module imports...")
    
    try:
        from app.services.smartrequest_service import SmartRequestService
        print("  ✅ SmartRequestService import successful")
    except ImportError as e:
        print(f"  ❌ SmartRequestService import failed: {e}")
        return False
    
    try:
        from app.utils.request_tracker import SmartRequestTracker
        print("  ✅ SmartRequestTracker import successful")
    except ImportError as e:
        print(f"  ❌ SmartRequestTracker import failed: {e}")
        return False
    
    try:
        from app.models.datavant_request import DatavantRequest
        print("  ✅ DatavantRequest model import successful")
    except ImportError as e:
        print(f"  ❌ DatavantRequest model import failed: {e}")
        return False
    
    print("\n✅ All module imports successful!")
    return True

def test_api_connection():
    """Test connection to SmartRequest API"""
    print("\n🔍 Testing SmartRequest API connection...")
    
    try:
        from app.services.smartrequest_service import SmartRequestService
        
        service = SmartRequestService()
        success = service.authenticate()
        
        if success:
            print("  ✅ SmartRequest API authentication successful!")
            
            # Test a simple API call
            try:
                record_types = service.get_record_types()
                if record_types:
                    print(f"  ✅ API functionality test passed - found {len(record_types)} record types")
                else:
                    print("  ⚠️ API authentication successful but no record types returned")
            except Exception as e:
                print(f"  ⚠️ API authentication successful but test call failed: {e}")
                
            return True
        else:
            print("  ❌ SmartRequest API authentication failed")
            print("     Please check your credentials and network connection")
            return False
            
    except Exception as e:
        print(f"  ❌ SmartRequest API test failed: {e}")
        return False

def check_file_structure():
    """Check if all required files are present"""
    print("\n🔍 Checking file structure...")
    
    required_files = [
        'app/services/smartrequest_service.py',
        'app/services/__init__.py',
        'app/utils/smartrequest_helper.py',
        'app/utils/request_tracker.py',
        'app/models/datavant_request.py',
        '.env.template',
        'SMARTREQUEST_INTEGRATION.md'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"  ❌ {file_path}")
    
    if missing_files:
        print(f"\n⚠️ Some files are missing, but integration may still work")
        return False
    
    print("\n✅ All required files present!")
    return True

def main():
    """Main verification function"""
    print("🚀 SmartRequest Integration Setup Verification")
    print("=" * 50)
    
    all_good = True
    
    # Check file structure
    if not check_file_structure():
        all_good = False
    
    # Check imports
    if not check_imports():
        all_good = False
        print("\n❌ Cannot proceed with API testing due to import failures")
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        all_good = False
        print("\n⚠️ Skipping API test due to missing configuration")
    else:
        # Test API connection
        if not test_api_connection():
            all_good = False
    
    print("\n" + "=" * 50)
    
    if all_good:
        print("🎉 Setup verification completed successfully!")
        print("\nYou can now:")
        print("  • Run your normal document workflows - SmartRequest calls will be automatic")
        print("  • Use CLI tools: python -m app.utils.smartrequest_helper test")
        print("  • Track requests: python -m app.utils.request_tracker list")
    else:
        print("⚠️ Setup verification completed with some issues")
        print("\nPlease address the issues above before proceeding")
        print("Refer to SMARTREQUEST_INTEGRATION.md for detailed setup instructions")
    
    return all_good

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)