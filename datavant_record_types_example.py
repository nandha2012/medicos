#!/usr/bin/env python
"""
Example script showing how to use the updated Datavant record types for mom and infant requests.

This script demonstrates how to:
1. Get available record types for mom and infant requests
2. Create sample request payloads using the correct record types
3. Show the difference between mom and infant record types
"""

from app.services.smartrequest_service import SmartRequestService

def main():
    print("🏥 Datavant Record Types for Mom & Infant Requests")
    print("=" * 60)
    
    # Initialize the service
    service = SmartRequestService()
    
    print("\n📋 INFANT RECORD TYPES")
    print("-" * 30)
    infant_types = service.get_infant_record_types()
    print(f"Available record types for infant requests: {len(infant_types)}")
    for i, record_type in enumerate(infant_types, 1):
        print(f"{i:2d}. {record_type}")
    
    print("\n👩 MOM RECORD TYPES")  
    print("-" * 20)
    mom_types = service.get_mom_record_types()
    print(f"Available record types for mom requests: {len(mom_types)}")
    for i, record_type in enumerate(mom_types, 1):
        print(f"{i:2d}. {record_type}")
    
    print("\n🔍 COMPARISON")
    print("-" * 15)
    infant_only = set(infant_types) - set(mom_types)
    mom_only = set(mom_types) - set(infant_types)
    common = set(infant_types) & set(mom_types)
    
    print(f"Record types only for infants ({len(infant_only)}):")
    for record_type in sorted(infant_only):
        print(f"  • {record_type}")
    
    print(f"\nRecord types only for moms ({len(mom_only)}):")
    for record_type in sorted(mom_only):
        print(f"  • {record_type}")
    
    print(f"\nCommon record types ({len(common)}):")
    for record_type in sorted(list(common)[:5]):  # Show first 5
        print(f"  • {record_type}")
    if len(common) > 5:
        print(f"  ... and {len(common) - 5} more")
    
    print("\n📝 EXAMPLE REQUEST PAYLOADS")
    print("-" * 30)
    
    # Example infant request
    print("\nExample infant request recordTypes:")
    example_infant_types = ["Cardiology Reports", "Audiology Report", "Speech Therapy", "Nursing Notes"]
    print(f'  "recordTypes": {example_infant_types}')
    
    # Example mom request  
    print("\nExample mom request recordTypes:")
    example_mom_types = ["Labor and Delivery Records", "ED Records", "Prenatal Care", "Nursing Notes"]
    print(f'  "recordTypes": {example_mom_types}')
    
    print("\n💡 USAGE TIPS")
    print("-" * 15)
    print("• Use service.get_infant_record_types() for infant medical record requests")
    print("• Use service.get_mom_record_types() for mom medical record requests") 
    print("• Always validate record types against the specific facility's capabilities")
    print("• The PDF documentation recommends requesting specific records vs. entire record")
    print("• Record types are case-sensitive and must match Datavant's exact naming")

if __name__ == "__main__":
    main()