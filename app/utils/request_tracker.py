#!/usr/bin/env python
"""
SmartRequest ID Tracker
Provides functionality to track and manage SmartRequest IDs
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict


@dataclass
class RequestRecord:
    """Data class for tracking SmartRequest records"""
    request_id: str
    record_id: str
    document_type: str
    status: str
    created_at: str
    updated_at: str
    patient_name: Optional[str] = None
    facility_name: Optional[str] = None
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'RequestRecord':
        return cls(**data)


class SmartRequestTracker:
    """Manager class for tracking SmartRequest IDs"""
    
    def __init__(self, storage_file: str = "logs/smartrequest_tracker.json"):
        self.storage_file = storage_file
        self._ensure_storage_dir()
        
    def _ensure_storage_dir(self):
        """Ensure the storage directory exists"""
        os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
    
    def _load_records(self) -> Dict[str, dict]:
        """Load existing records from storage"""
        if not os.path.exists(self.storage_file):
            return {}
        
        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️ Error loading request tracker data: {e}")
            return {}
    
    def _save_records(self, records: Dict[str, dict]):
        """Save records to storage"""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(records, f, indent=2, default=str)
        except IOError as e:
            print(f"❌ Error saving request tracker data: {e}")
    
    def add_request(
        self, 
        request_id: str, 
        record_id: str, 
        document_type: str = "medical_record",
        patient_name: Optional[str] = None,
        facility_name: Optional[str] = None
    ) -> bool:
        """
        Add a new SmartRequest to tracking
        
        Args:
            request_id: SmartRequest API request ID
            record_id: Internal record/document ID
            document_type: Type of document being requested
            patient_name: Optional patient name
            facility_name: Optional facility name
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            records = self._load_records()
            timestamp = datetime.now().isoformat()
            
            record = RequestRecord(
                request_id=request_id,
                record_id=record_id,
                document_type=document_type,
                status="Created",
                created_at=timestamp,
                updated_at=timestamp,
                patient_name=patient_name,
                facility_name=facility_name
            )
            
            records[request_id] = record.to_dict()
            self._save_records(records)
            
            print(f"📝 Added request tracking: {request_id} -> {record_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error adding request to tracker: {e}")
            return False
    
    def update_request_status(self, request_id: str, status: str) -> bool:
        """
        Update the status of a tracked request
        
        Args:
            request_id: SmartRequest API request ID
            status: New status
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            records = self._load_records()
            
            if request_id not in records:
                print(f"⚠️ Request ID {request_id} not found in tracker")
                return False
            
            records[request_id]['status'] = status
            records[request_id]['updated_at'] = datetime.now().isoformat()
            
            self._save_records(records)
            
            print(f"📝 Updated request {request_id} status to: {status}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating request status: {e}")
            return False
    
    def get_request(self, request_id: str) -> Optional[RequestRecord]:
        """
        Get a tracked request by ID
        
        Args:
            request_id: SmartRequest API request ID
            
        Returns:
            RequestRecord or None if not found
        """
        try:
            records = self._load_records()
            
            if request_id not in records:
                return None
            
            return RequestRecord.from_dict(records[request_id])
            
        except Exception as e:
            print(f"❌ Error getting request: {e}")
            return None
    
    def get_requests_by_record_id(self, record_id: str) -> List[RequestRecord]:
        """
        Get all requests for a specific record ID
        
        Args:
            record_id: Internal record/document ID
            
        Returns:
            List of RequestRecord objects
        """
        try:
            records = self._load_records()
            matches = []
            
            for request_data in records.values():
                if request_data.get('record_id') == record_id:
                    matches.append(RequestRecord.from_dict(request_data))
            
            return matches
            
        except Exception as e:
            print(f"❌ Error getting requests by record ID: {e}")
            return []
    
    def list_all_requests(self) -> List[RequestRecord]:
        """
        Get all tracked requests
        
        Returns:
            List of all RequestRecord objects
        """
        try:
            records = self._load_records()
            return [RequestRecord.from_dict(data) for data in records.values()]
            
        except Exception as e:
            print(f"❌ Error listing all requests: {e}")
            return []
    
    def get_requests_by_status(self, status: str) -> List[RequestRecord]:
        """
        Get all requests with a specific status
        
        Args:
            status: Status to filter by
            
        Returns:
            List of RequestRecord objects
        """
        try:
            records = self._load_records()
            matches = []
            
            for request_data in records.values():
                if request_data.get('status') == status:
                    matches.append(RequestRecord.from_dict(request_data))
            
            return matches
            
        except Exception as e:
            print(f"❌ Error getting requests by status: {e}")
            return []
    
    def remove_request(self, request_id: str) -> bool:
        """
        Remove a request from tracking
        
        Args:
            request_id: SmartRequest API request ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            records = self._load_records()
            
            if request_id in records:
                del records[request_id]
                self._save_records(records)
                print(f"🗑️ Removed request tracking: {request_id}")
                return True
            else:
                print(f"⚠️ Request ID {request_id} not found in tracker")
                return False
                
        except Exception as e:
            print(f"❌ Error removing request: {e}")
            return False


# Global tracker instance
request_tracker = SmartRequestTracker()


def track_smartrequest(
    request_id: str, 
    record_id: str, 
    document_type: str = "medical_record",
    patient_name: Optional[str] = None,
    facility_name: Optional[str] = None
) -> bool:
    """
    Convenience function to track a SmartRequest
    
    Args:
        request_id: SmartRequest API request ID
        record_id: Internal record/document ID
        document_type: Type of document being requested
        patient_name: Optional patient name
        facility_name: Optional facility name
        
    Returns:
        bool: True if successful, False otherwise
    """
    return request_tracker.add_request(
        request_id, record_id, document_type, patient_name, facility_name
    )


def update_smartrequest_status(request_id: str, status: str) -> bool:
    """
    Convenience function to update SmartRequest status
    
    Args:
        request_id: SmartRequest API request ID
        status: New status
        
    Returns:
        bool: True if successful, False otherwise
    """
    return request_tracker.update_request_status(request_id, status)


if __name__ == "__main__":
    """Command line interface for request tracking"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python request_tracker.py <command> [args...]")
        print("Commands:")
        print("  list                           - List all tracked requests")
        print("  get <request_id>              - Get specific request details")
        print("  status <status>               - Get requests by status")
        print("  record <record_id>            - Get requests by record ID")
        print("  update <request_id> <status>  - Update request status")
        print("  remove <request_id>           - Remove request from tracking")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    tracker = SmartRequestTracker()
    
    if command == "list":
        requests = tracker.list_all_requests()
        if requests:
            print(f"📋 Found {len(requests)} tracked requests:")
            for req in requests:
                print(f"   {req.request_id}: {req.record_id} ({req.status}) - {req.created_at}")
        else:
            print("📋 No tracked requests found")
    
    elif command == "get":
        if len(sys.argv) < 3:
            print("❌ Request ID required")
            sys.exit(1)
        request_id = sys.argv[2]
        request = tracker.get_request(request_id)
        if request:
            print(f"📋 Request {request_id}:")
            for key, value in request.to_dict().items():
                print(f"   {key}: {value}")
        else:
            print(f"❌ Request {request_id} not found")
    
    elif command == "status":
        if len(sys.argv) < 3:
            print("❌ Status required")
            sys.exit(1)
        status = sys.argv[2]
        requests = tracker.get_requests_by_status(status)
        if requests:
            print(f"📋 Found {len(requests)} requests with status '{status}':")
            for req in requests:
                print(f"   {req.request_id}: {req.record_id} - {req.updated_at}")
        else:
            print(f"📋 No requests found with status '{status}'")
    
    elif command == "record":
        if len(sys.argv) < 3:
            print("❌ Record ID required")
            sys.exit(1)
        record_id = sys.argv[2]
        requests = tracker.get_requests_by_record_id(record_id)
        if requests:
            print(f"📋 Found {len(requests)} requests for record '{record_id}':")
            for req in requests:
                print(f"   {req.request_id}: {req.status} - {req.created_at}")
        else:
            print(f"📋 No requests found for record '{record_id}'")
    
    elif command == "update":
        if len(sys.argv) < 4:
            print("❌ Request ID and status required")
            sys.exit(1)
        request_id = sys.argv[2]
        status = sys.argv[3]
        success = tracker.update_request_status(request_id, status)
        sys.exit(0 if success else 1)
    
    elif command == "remove":
        if len(sys.argv) < 3:
            print("❌ Request ID required")
            sys.exit(1)
        request_id = sys.argv[2]
        success = tracker.remove_request(request_id)
        sys.exit(0 if success else 1)
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)