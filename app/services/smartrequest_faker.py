#!/usr/bin/env python
"""
SmartRequest API Faker
Provides fake responses for SmartRequest API when testing locally
"""

import random
import string
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from faker import Faker

fake = Faker()

class SmartRequestFaker:
    """Generates fake SmartRequest API responses for local testing"""
    
    def __init__(self):
        self.access_token = self._generate_fake_token()
        self.request_counter = 1000
        
    def _generate_fake_token(self) -> str:
        """Generate a fake JWT-like token"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=64))
    
    def _generate_request_id(self) -> str:
        """Generate a fake request ID"""
        self.request_counter += 1
        return str(self.request_counter)
    
    def authenticate(self) -> Dict[str, Any]:
        """Fake authentication response"""
        return {
            "accessToken": self.access_token,
            "tokenType": "Bearer",
            "expiresIn": 3600
        }
    
    def get_facilities(self, filters: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Generate fake facilities response"""
        facilities = []
        
        # Generate 5-20 fake facilities
        num_facilities = random.randint(5, 20)
        
        for i in range(num_facilities):
            state = filters.get('state') if filters and 'state' in filters else fake.state_abbr()
            city = filters.get('city') if filters and 'city' in filters else fake.city()
            
            facility = {
                "siteName": f"{fake.company()} Medical Center",
                "healthSystem": f"{fake.company()} Health System",
                "address": f"{fake.street_address()}",
                "addressLine1": fake.street_address(),
                "addressLine2": fake.secondary_address() if random.choice([True, False]) else None,
                "city": city,
                "state": state,
                "zip": fake.zipcode(),
                "stdZip": fake.zipcode(),
                "phone": fake.phone_number().replace('-', '').replace('(', '').replace(')', '').replace(' ', '')[:10],
                "fax": fake.phone_number().replace('-', '').replace('(', '').replace(')', '').replace(' ', '')[:10]
            }
            
            # Apply city filter if specified
            if filters and 'city' in filters:
                if filters['city'].lower() not in facility['city'].lower():
                    continue
                    
            facilities.append(facility)
        
        return {
            "totalRows": len(facilities),
            "facilities": facilities,
            "nextToken": fake.uuid4() if len(facilities) > 10 else None
        }
    
    def get_request_reasons(self, company_id: int) -> Dict[str, Any]:
        """Generate fake request reasons response"""
        business_types = ["ATTY", "COPY_SERVICE", "LIFE_INS", "DISABILITY", "WORKERS_COMP"]
        
        reasons = []
        for business_type in business_types:
            for i in range(random.randint(2, 5)):
                api_code = f"{business_type}_{fake.word().upper()}_{i+1}"
                name = f"{business_type.replace('_', ' ').title()} - {fake.bs().title()}"
                
                reason = {
                    "name": name,
                    "businessType": business_type,
                    "apiCode": api_code,
                    "facilityStates": ["ALL"] if random.choice([True, False]) else random.sample(
                        ["CA", "TX", "NY", "FL", "IL", "PA", "OH", "GA", "NC", "MI"], 
                        random.randint(1, 3)
                    )
                }
                reasons.append(reason)
        
        return {
            "reasons": reasons
        }
    
    def get_record_types(self) -> Dict[str, Any]:
        """Generate fake record types response"""
        record_types = [
            {"name": "Abstract", "digitalFulfillment": True},
            {"name": "Admission Records", "digitalFulfillment": True},
            {"name": "Billing Records", "digitalFulfillment": False},
            {"name": "Discharge Summary", "digitalFulfillment": True},
            {"name": "Emergency Department Records", "digitalFulfillment": True},
            {"name": "Imaging Reports", "digitalFulfillment": True},
            {"name": "Laboratory Results", "digitalFulfillment": True},
            {"name": "Medication Records", "digitalFulfillment": True},
            {"name": "Nursing Notes", "digitalFulfillment": False},
            {"name": "Operative Reports", "digitalFulfillment": True},
            {"name": "Pathology Reports", "digitalFulfillment": True},
            {"name": "Physical Therapy Records", "digitalFulfillment": False},
            {"name": "Physician Notes", "digitalFulfillment": True},
            {"name": "Radiology Reports", "digitalFulfillment": True},
            {"name": "Toxicology Reports", "digitalFulfillment": True},
            {"name": "Complete Medical Record", "digitalFulfillment": False}
        ]
        
        # Randomly include some record types
        included_types = random.sample(record_types, random.randint(8, len(record_types)))
        
        return {
            "recordTypes": included_types
        }
    
    def create_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fake request creation response"""
        request_id = self._generate_request_id()
        
        # Echo back the request data with some modifications
        response = request_data.copy()
        
        # Remove authorization forms from response (as per real API)
        if "authorizationForms" in response:
            del response["authorizationForms"]
        
        # Add request ID and any missing fields
        response["requestId"] = request_id
        
        # Ensure facility has address field
        if "facility" in response and "address" not in response["facility"]:
            response["facility"]["address"] = response["facility"].get("addressLine1", "")
        
        print(f"🎭 FAKE: Created SmartRequest with ID: {request_id}")
        return response
    
    def get_request_status(self, request_id: str) -> Dict[str, Any]:
        """Generate fake request status response"""
        statuses = [
            "Created",
            "In Process - Pending Fulfillment", 
            "In Process - Fulfillment",
            "In Process - Quality Assurance",
            "In Process - Pending Approval",
            "In Process - Preparing Invoice",
            "In Process - Certification",
            "Record Available",
            "Requires Payment",
            "Correspondence Sent"
        ]
        
        status = random.choice(statuses)
        modified_date = fake.date_time_between(start_date='-30d', end_date='now').isoformat() + "+00:00"
        
        return {
            "requestId": request_id,
            "status": status,
            "modifiedDate": modified_date
        }
    
    def get_download_url(self, request_id: str, document_type: str) -> Dict[str, str]:
        """Generate fake download URL response"""
        fake_url = f"https://fake-download-server.com/download/{request_id}/{document_type.lower()}/{fake.uuid4()}.pdf"
        
        return {
            "url": fake_url
        }
    
    def cancel_request(self, request_id: str, reason: str) -> bool:
        """Simulate request cancellation"""
        print(f"🎭 FAKE: Cancelled request {request_id} with reason: {reason}")
        return True
    
    def encode_authorization_form(self, file_path: str) -> str:
        """Generate fake base64 encoded content"""
        # Generate fake PDF-like content
        fake_content = f"FAKE_PDF_CONTENT_{fake.uuid4()}"
        import base64
        return base64.b64encode(fake_content.encode()).decode()


# Global faker instance
smartrequest_faker = SmartRequestFaker()


def get_fake_company_id() -> int:
    """Get a fake company ID for testing"""
    return random.randint(1000000, 9999999)


def get_fake_facility_data() -> Dict[str, Any]:
    """Generate fake facility data for testing"""
    return {
        "addressLine1": fake.street_address(),
        "city": fake.city(),
        "state": fake.state_abbr(),
        "zip": fake.zipcode(),
        "healthSystem": f"{fake.company()} Health System",
        "siteName": f"{fake.company()} Medical Center",
        "phone": fake.phone_number().replace('-', '').replace('(', '').replace(')', '').replace(' ', '')[:10],
        "fax": fake.phone_number().replace('-', '').replace('(', '').replace(')', '').replace(' ', '')[:10]
    }


def get_fake_patient_data() -> Dict[str, Any]:
    """Generate fake patient data for testing"""
    return {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "dateOfBirth": fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%Y-%m-%d"),
        "ssn": fake.ssn().replace('-', ''),
        "customId": fake.uuid4()[:8].upper()
    }


def get_fake_requester_data() -> Dict[str, Any]:
    """Generate fake requester data for testing"""
    return {
        "companyId": get_fake_company_id(),
        "companyName": f"{fake.company()} Law Firm",
        "name": fake.name(),
        "email": fake.email()
    }


def create_fake_smartrequest_payload() -> Dict[str, Any]:
    """Create a complete fake SmartRequest payload for testing"""
    return {
        "facility": get_fake_facility_data(),
        "requesterInfo": get_fake_requester_data(),
        "patient": get_fake_patient_data(),
        "reason": {
            "businessType": "ATTY",
            "apiCode": "STATE_ATTY_OFFICE"
        },
        "requestCriteria": [
            {
                "recordTypes": ["Abstract", "Laboratory Results"],
                "startDate": fake.date_between(start_date='-2y', end_date='-1y').strftime("%Y-%m-%d"),
                "endDate": fake.date_between(start_date='-1y', end_date='today').strftime("%Y-%m-%d")
            }
        ],
        "certificationRequired": random.choice([True, False]),
        "authorizationForms": [
            smartrequest_faker.encode_authorization_form("fake_auth_form.pdf")
        ],
        "callbackDetails": {
            "method": "POST",
            "url": f"https://{fake.domain_name()}/webhook/smartrequest",
            "headers": {
                "Authorization": f"Bearer {fake.uuid4()}",
                "Content-Type": "application/json"
            }
        }
    }


if __name__ == "__main__":
    """Test the faker functionality"""
    print("🎭 Testing SmartRequest Faker...")
    
    faker = SmartRequestFaker()
    
    # Test authentication
    print("\n1. Testing authentication...")
    auth_response = faker.authenticate()
    print(f"   Token: {auth_response['accessToken'][:20]}...")
    
    # Test facilities
    print("\n2. Testing facilities...")
    facilities_response = faker.get_facilities()
    print(f"   Found {len(facilities_response['facilities'])} facilities")
    
    # Test record types
    print("\n3. Testing record types...")
    record_types_response = faker.get_record_types()
    print(f"   Found {len(record_types_response['recordTypes'])} record types")
    
    # Test request reasons
    print("\n4. Testing request reasons...")
    reasons_response = faker.get_request_reasons(1234567)
    print(f"   Found {len(reasons_response['reasons'])} request reasons")
    
    # Test request creation
    print("\n5. Testing request creation...")
    fake_payload = create_fake_smartrequest_payload()
    create_response = faker.create_request(fake_payload)
    request_id = create_response['requestId']
    print(f"   Created request: {request_id}")
    
    # Test status check
    print("\n6. Testing status check...")
    status_response = faker.get_request_status(request_id)
    print(f"   Status: {status_response['status']}")
    
    # Test download URL
    print("\n7. Testing download URL...")
    download_response = faker.get_download_url(request_id, "MEDICAL_RECORD")
    print(f"   Download URL: {download_response['url'][:50]}...")
    
    print("\n✅ All faker tests completed successfully!")