#!/usr/bin/env python
"""
Dashboard Data Tracker
Enhanced tracking service for PDF generation and SmartRequest monitoring
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional, Any, List
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class ProcessingRecord:
    """Complete record of a processing event"""
    record_id: str
    timestamp: str
    
    # Patient and facility info
    patient_name: Optional[str] = None
    facility_name: Optional[str] = None
    
    # PDF generation info
    pdf_status: str = "pending"  # pending, success, error
    pdf_path: Optional[str] = None
    pdf_error: Optional[str] = None
    request_type: str = "unknown"  # first_request, second_request_complete, second_request_partial
    
    # SmartRequest info
    smartrequest_sent: bool = False
    smartrequest_id: Optional[str] = None
    smartrequest_status: str = "not_sent"  # not_sent, sent, success, error
    smartrequest_error: Optional[str] = None
    smartrequest_payload: Optional[Dict[str, Any]] = None
    
    # Additional metadata
    username: Optional[str] = None
    template_used: Optional[str] = None
    processing_duration: Optional[float] = None
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ProcessingRecord':
        return cls(**data)


class DashboardTracker:
    """Enhanced tracker for dashboard data"""
    
    def __init__(self, storage_file: str = "logs/dashboard_tracking.json"):
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
            print(f"⚠️ Error loading dashboard tracking data: {e}")
            return {}
    
    def _save_records(self, records: Dict[str, dict]):
        """Save records to storage"""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(records, f, indent=2, default=str)
        except IOError as e:
            print(f"❌ Error saving dashboard tracking data: {e}")
    
    def start_processing(self, record_id: str, request_type: str, patient_name: Optional[str] = None, 
                        facility_name: Optional[str] = None, username: Optional[str] = None) -> bool:
        """Start tracking a new processing record"""
        try:
            records = self._load_records()
            
            # Create unique key for this processing instance
            instance_key = f"{record_id}_{request_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            record = ProcessingRecord(
                record_id=record_id,
                timestamp=datetime.now().isoformat(),
                patient_name=patient_name,
                facility_name=facility_name,
                request_type=request_type,
                username=username,
                pdf_status="pending",
                smartrequest_status="not_sent"
            )
            
            records[instance_key] = record.to_dict()
            self._save_records(records)
            
            print(f"📊 Started tracking: {instance_key}")
            return True
            
        except Exception as e:
            print(f"❌ Error starting processing tracking: {e}")
            return False
    
    def update_pdf_status(self, record_id: str, status: str, pdf_path: Optional[str] = None, 
                         error: Optional[str] = None, template_used: Optional[str] = None) -> bool:
        """Update PDF generation status"""
        try:
            records = self._load_records()
            
            # Find the most recent record for this record_id
            matching_key = self._find_recent_record(records, record_id)
            if not matching_key:
                print(f"⚠️ No tracking record found for {record_id}")
                return False
            
            records[matching_key]['pdf_status'] = status
            records[matching_key]['pdf_path'] = pdf_path
            records[matching_key]['pdf_error'] = error
            records[matching_key]['template_used'] = template_used
            
            self._save_records(records)
            
            print(f"📊 Updated PDF status for {record_id}: {status}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating PDF status: {e}")
            return False
    
    def update_smartrequest_status(self, record_id: str, status: str, request_id: Optional[str] = None, 
                                  error: Optional[str] = None, payload: Optional[Dict[str, Any]] = None) -> bool:
        """Update SmartRequest status"""
        try:
            records = self._load_records()
            
            # Find the most recent record for this record_id
            matching_key = self._find_recent_record(records, record_id)
            if not matching_key:
                print(f"⚠️ No tracking record found for {record_id}")
                return False
            
            records[matching_key]['smartrequest_sent'] = status in ['sent', 'success']
            records[matching_key]['smartrequest_id'] = request_id
            records[matching_key]['smartrequest_status'] = status
            records[matching_key]['smartrequest_error'] = error
            
            # Store sanitized payload (remove authorization forms)
            if payload:
                sanitized_payload = payload.copy()
                if 'authorizationForms' in sanitized_payload:
                    sanitized_payload['authorizationForms'] = f"[{len(payload.get('authorizationForms', []))} files]"
                records[matching_key]['smartrequest_payload'] = sanitized_payload
            
            self._save_records(records)
            
            print(f"📊 Updated SmartRequest status for {record_id}: {status}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating SmartRequest status: {e}")
            return False
    
    def complete_processing(self, record_id: str, duration: Optional[float] = None) -> bool:
        """Mark processing as complete"""
        try:
            records = self._load_records()
            
            # Find the most recent record for this record_id
            matching_key = self._find_recent_record(records, record_id)
            if not matching_key:
                print(f"⚠️ No tracking record found for {record_id}")
                return False
            
            records[matching_key]['processing_duration'] = duration
            
            self._save_records(records)
            
            print(f"📊 Completed processing for {record_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error completing processing tracking: {e}")
            return False
    
    def _find_recent_record(self, records: Dict[str, dict], record_id: str) -> Optional[str]:
        """Find the most recent tracking record for a record_id"""
        matching_records = []
        
        for key, record in records.items():
            if record.get('record_id') == record_id:
                matching_records.append((key, record.get('timestamp', '')))
        
        if not matching_records:
            return None
        
        # Sort by timestamp and return the most recent
        matching_records.sort(key=lambda x: x[1], reverse=True)
        return matching_records[0][0]
    
    def get_all_records(self) -> List[ProcessingRecord]:
        """Get all tracking records"""
        try:
            records = self._load_records()
            return [ProcessingRecord.from_dict(data) for data in records.values()]
        except Exception as e:
            print(f"❌ Error getting all records: {e}")
            return []
    
    def get_records_by_status(self, pdf_status: Optional[str] = None, 
                             smartrequest_status: Optional[str] = None) -> List[ProcessingRecord]:
        """Get records filtered by status"""
        try:
            all_records = self.get_all_records()
            filtered_records = []
            
            for record in all_records:
                if pdf_status and record.pdf_status != pdf_status:
                    continue
                if smartrequest_status and record.smartrequest_status != smartrequest_status:
                    continue
                filtered_records.append(record)
            
            return filtered_records
        except Exception as e:
            print(f"❌ Error filtering records: {e}")
            return []
    
    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get summary statistics for dashboard"""
        try:
            records = self.get_all_records()
            
            summary = {
                "total_records": len(records),
                "pdf_success": len([r for r in records if r.pdf_status == "success"]),
                "pdf_errors": len([r for r in records if r.pdf_status == "error"]),
                "pdf_pending": len([r for r in records if r.pdf_status == "pending"]),
                "smartrequest_sent": len([r for r in records if r.smartrequest_sent]),
                "smartrequest_success": len([r for r in records if r.smartrequest_status == "success"]),
                "smartrequest_errors": len([r for r in records if r.smartrequest_status == "error"]),
                "request_types": {},
                "recent_activity": []
            }
            
            # Count by request types
            for record in records:
                req_type = record.request_type
                summary["request_types"][req_type] = summary["request_types"].get(req_type, 0) + 1
            
            # Get recent activity (last 10 records)
            sorted_records = sorted(records, key=lambda x: x.timestamp, reverse=True)
            summary["recent_activity"] = [r.to_dict() for r in sorted_records[:10]]
            
            return summary
            
        except Exception as e:
            print(f"❌ Error getting dashboard summary: {e}")
            return {}


# Global dashboard tracker instance
dashboard_tracker = DashboardTracker()


# Convenience functions
def track_processing_start(record_id: str, request_type: str, patient_name: Optional[str] = None, 
                          facility_name: Optional[str] = None, username: Optional[str] = None) -> bool:
    """Convenience function to start tracking"""
    return dashboard_tracker.start_processing(record_id, request_type, patient_name, facility_name, username)


def track_pdf_success(record_id: str, pdf_path: str, template_used: Optional[str] = None) -> bool:
    """Convenience function to track PDF success"""
    return dashboard_tracker.update_pdf_status(record_id, "success", pdf_path, None, template_used)


def track_pdf_error(record_id: str, error: str) -> bool:
    """Convenience function to track PDF error"""
    return dashboard_tracker.update_pdf_status(record_id, "error", None, error)


def track_smartrequest_sent(record_id: str, request_id: str, payload: Optional[Dict[str, Any]] = None) -> bool:
    """Convenience function to track SmartRequest sent"""
    return dashboard_tracker.update_smartrequest_status(record_id, "sent", request_id, None, payload)


def track_smartrequest_success(record_id: str, request_id: str) -> bool:
    """Convenience function to track SmartRequest success"""
    return dashboard_tracker.update_smartrequest_status(record_id, "success", request_id)


def track_smartrequest_error(record_id: str, error: str) -> bool:
    """Convenience function to track SmartRequest error"""
    return dashboard_tracker.update_smartrequest_status(record_id, "error", None, error)


if __name__ == "__main__":
    """Test the dashboard tracker"""
    print("🧪 Testing Dashboard Tracker...")
    
    # Test creating a record
    tracker = DashboardTracker()
    
    record_id = "TEST123"
    
    # Start tracking
    tracker.start_processing(record_id, "first_request", "John Doe", "Test Hospital", "testuser")
    
    # Update PDF status
    tracker.update_pdf_status(record_id, "success", "output/test.pdf", None, "mother_template")
    
    # Update SmartRequest status
    tracker.update_smartrequest_status(record_id, "sent", "REQ123", None, {"test": "payload"})
    
    # Complete processing
    tracker.complete_processing(record_id, 5.2)
    
    # Get summary
    summary = tracker.get_dashboard_summary()
    print(f"📊 Summary: {json.dumps(summary, indent=2)}")
    
    print("✅ Dashboard tracker test completed!")