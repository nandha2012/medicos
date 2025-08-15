#!/usr/bin/env python
import requests
import base64
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# Import faker for local testing
try:
    from .smartrequest_faker import smartrequest_faker
except ImportError:
    # Handle relative import when running as module
    import sys
    sys.path.append(os.path.dirname(__file__))
    from smartrequest_faker import smartrequest_faker

class SmartRequestService:
    """Service class for interacting with SmartRequest (Datavant) API"""
    
    def __init__(self):
        # Load configuration from environment
        self.base_url = os.getenv("SMARTREQUEST_BASE_URL", "https://sandbox-api.datavant.com/v1")
        self.client_id = os.getenv("SMARTREQUEST_CLIENT_ID", "")
        self.client_secret = os.getenv("SMARTREQUEST_CLIENT_SECRET", "")
        self.access_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None
        
        # Check if we should use fake mode
        self.env = os.getenv("ENV", "production").lower()
        self.use_faker = (self.env == "local" or 
                         not self.client_id or 
                         not self.client_secret or
                         os.getenv("USE_SMARTREQUEST_FAKER", "false").lower() == "true")
        
        if self.use_faker:
            print("🎭 SmartRequest: Using faker mode for local testing")
        
    def _get_basic_auth_header(self) -> str:
        """Generate Basic Auth header for token endpoint"""
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded_credentials}"
    
    def _get_bearer_auth_header(self) -> str:
        """Generate Bearer Auth header for API calls"""
        return f"Bearer {self.access_token}"
    
    def _is_token_expired(self) -> bool:
        """Check if the current token is expired or will expire soon"""
        if not self.access_token or not self.token_expires_at:
            return True
        # Consider token expired if it expires within 5 minutes
        return datetime.now() + timedelta(minutes=5) >= self.token_expires_at
    
    def authenticate(self) -> bool:
        """
        Authenticate with SmartRequest API and get access token
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        if self.use_faker:
            print("🎭 Using fake authentication...")
            auth_data = smartrequest_faker.authenticate()
            self.access_token = auth_data.get("accessToken")
            expires_in = auth_data.get("expiresIn", 3600)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
            print(f"✅ SmartRequest fake authentication successful")
            return True
        
        url = f"{self.base_url}/auth/token"
        headers = {
            "Authorization": self._get_basic_auth_header()
        }
        print(f"🔄 Authenticating with SmartRequest API...")
        
        try:
            response = requests.post(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            self.access_token = data.get("accessToken")
            expires_in = data.get("expiresIn", 3600)  # Default to 1 hour
            
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
            
            print(f"✅ SmartRequest authentication successful")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ SmartRequest authentication failed: {e}")
            return False
    
    def _ensure_authenticated(self) -> bool:
        """Ensure we have a valid access token"""
        if self._is_token_expired():
            return self.authenticate()
        return True
    
    def get_facilities(self, filters: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
        """
        Get list of facilities from SmartRequest API
        
        Args:
            filters: Optional filters to apply to the search
            
        Returns:
            List of facility dictionaries
        """
        if self.use_faker:
            print("🎭 Using fake facilities data...")
            data = smartrequest_faker.get_facilities(filters)
            return data.get("facilities", [])
        
        if not self._ensure_authenticated():
            return []
            
        url = f"{self.base_url}/facilities"
        headers = {
            "Authorization": self._get_bearer_auth_header()
        }
        
        try:
            response = requests.get(url, headers=headers, params=filters or {}, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return data.get("facilities", [])
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching facilities: {e}")
            return []
    
    def get_request_reasons(self, company_id: int) -> List[Dict[str, Any]]:
        """
        Get available request reasons for a company
        
        Args:
            company_id: Company ID to get reasons for
            
        Returns:
            List of reason dictionaries
        """
        if self.use_faker:
            print("🎭 Using fake request reasons data...")
            data = smartrequest_faker.get_request_reasons(company_id)
            return data.get("reasons", [])
        
        if not self._ensure_authenticated():
            return []
            
        url = f"{self.base_url}/request-reasons"
        headers = {
            "Authorization": self._get_bearer_auth_header()
        }
        params = {"companyId": company_id}
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return data.get("reasons", [])
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching request reasons: {e}")
            return []
    
    def get_record_types(self) -> List[Dict[str, Any]]:
        """
        Get available record types
        
        Returns:
            List of record type dictionaries
        """
        if self.use_faker:
            print("🎭 Using fake record types data...")
            data = smartrequest_faker.get_record_types()
            return data.get("recordTypes", [])
        
        if not self._ensure_authenticated():
            return []
            
        url = f"{self.base_url}/record-types"
        headers = {
            "Authorization": self._get_bearer_auth_header()
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return data.get("recordTypes", [])
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching record types: {e}")
            return []
    
    def create_request(self, request_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a medical records request
        
        Args:
            request_data: Dictionary containing request payload
            
        Returns:
            API response dictionary or None on error
        """
        if self.use_faker:
            print("🎭 Creating fake SmartRequest...")
            return smartrequest_faker.create_request(request_data)
        
        if not self._ensure_authenticated():
            return None
            
        url = f"{self.base_url}/request"
        headers = {
            "Authorization": self._get_bearer_auth_header(),
            "Content-Type": "application/json"
        }
        
        try:
            print(f"🔄 Creating SmartRequest...")
            print(f'datavant payload {request_data}')
            response = requests.post(url, json=request_data, headers=headers, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            request_id = result.get("requestId")
            print(f"✅ SmartRequest created successfully with ID: {request_id}")
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error creating SmartRequest: {e}")
            return None
    
    def get_request_status(self, request_id: str) -> Optional[Dict[str, Any]]:
        """
        Get status of a request
        
        Args:
            request_id: ID of the request to check
            
        Returns:
            Status dictionary or None on error
        """
        if self.use_faker:
            print(f"🎭 Getting fake status for request {request_id}...")
            return smartrequest_faker.get_request_status(request_id)
        
        if not self._ensure_authenticated():
            return None
            
        url = f"{self.base_url}/request/{request_id}/status"
        headers = {
            "Authorization": self._get_bearer_auth_header()
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error getting request status: {e}")
            return None
    
    def get_download_url(self, request_id: str, document_type: str) -> Optional[str]:
        """
        Get download URL for request documents
        
        Args:
            request_id: ID of the request
            document_type: Type of document (REQUEST_LETTER, INVOICE, MEDICAL_RECORD, CORRESPONDENCE, ALL)
            
        Returns:
            Download URL or None on error
        """
        if self.use_faker:
            print(f"🎭 Getting fake download URL for {request_id}/{document_type}...")
            data = smartrequest_faker.get_download_url(request_id, document_type)
            return data.get("url")
        
        if not self._ensure_authenticated():
            return None
            
        url = f"{self.base_url}/request/{request_id}/download-url/{document_type}"
        headers = {
            "Authorization": self._get_bearer_auth_header()
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return data.get("url")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error getting download URL: {e}")
            return None
    
    def cancel_request(self, request_id: str, reason: str) -> bool:
        """
        Cancel a request
        
        Args:
            request_id: ID of the request to cancel
            reason: Reason for cancellation
            
        Returns:
            True if successful, False otherwise
        """
        if self.use_faker:
            print(f"🎭 Cancelling fake request {request_id}...")
            return smartrequest_faker.cancel_request(request_id, reason)
        
        if not self._ensure_authenticated():
            return False
            
        url = f"{self.base_url}/request/{request_id}/cancel"
        headers = {
            "Authorization": self._get_bearer_auth_header(),
            "Content-Type": "application/json"
        }
        data = {"reason": reason}
        
        try:
            response = requests.put(url, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            
            print(f"✅ Request {request_id} cancelled successfully")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error cancelling request: {e}")
            return False
    
    def encode_authorization_form(self, file_path: str) -> Optional[str]:
        """
        Base64 encode an authorization form file
        
        Args:
            file_path: Path to the file to encode
            
        Returns:
            Base64 encoded string or None on error
        """
        try:
            with open(file_path, 'rb') as file:
                file_content = file.read()
                encoded = base64.b64encode(file_content).decode('utf-8')
                return encoded
        except Exception as e:
            print(f"❌ Error encoding file {file_path}: {e}")
            return None