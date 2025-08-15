#!/usr/bin/env python
"""
Flask Dashboard Server for Medicos
Provides web interface to view PDF generation and SmartRequest tracking
"""

import os
import sys
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from flask import Flask, render_template, jsonify, send_file, request
from pathlib import Path

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from utils.request_tracker import SmartRequestTracker
from utils.logger import PandasCSVLogger

app = Flask(__name__)

class DashboardDataService:
    """Service to collect and aggregate dashboard data"""
    
    def __init__(self):
        self.request_tracker = SmartRequestTracker()
        self.output_dir = Path("output")
        self.logs_dir = Path("logs")
        
    def get_dashboard_data(self, date_filter: str = "all", status_filter: str = "all", type_filter: str = "all") -> Dict[str, Any]:
        """Collect all dashboard data using dashboard tracker"""
        try:
            # Use dashboard tracker like the simple dashboard does
            from utils.dashboard_tracker import dashboard_tracker
            
            records = dashboard_tracker.get_all_records()
            
            # Convert records to dictionary format
            record_dicts = []
            for record in records:
                record_dict = {
                    "recordId": record.record_id,
                    "patientName": record.patient_name,
                    "facilityName": record.facility_name,
                    "pdfStatus": record.pdf_status,
                    "pdfPath": record.pdf_path,
                    "requestStatus": record.smartrequest_status,
                    "requestId": record.smartrequest_id,
                    "requestType": record.request_type,
                    "timestamp": record.timestamp
                }
                record_dicts.append(record_dict)
            
            # Apply filters
            filtered_records = self._apply_filters(record_dicts, date_filter, status_filter, type_filter)
            
            # Calculate stats
            stats = self._calculate_stats(filtered_records)
            
            return {
                "records": filtered_records,
                "stats": stats,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error getting dashboard data: {e}")
            return {
                "records": [],
                "stats": {"totalPdfs": 0, "totalRequests": 0, "pdfErrors": 0, "requestFailures": 0},
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def _apply_filters(self, records: List[Dict[str, Any]], date_filter: str, status_filter: str, type_filter: str) -> List[Dict[str, Any]]:
        """Apply filtering to records"""
        filtered_records = records.copy()
        
        # Apply date filter
        if date_filter != "all":
            cutoff_date = self._get_cutoff_date(date_filter)
            filtered_records = [r for r in filtered_records if self._parse_timestamp(r.get("timestamp", "")) >= cutoff_date]
        
        # Apply status filter
        if status_filter != "all":
            if status_filter == "success":
                filtered_records = [r for r in filtered_records if r.get("pdfStatus") == "success" or r.get("requestStatus") == "success"]
            elif status_filter == "error":
                filtered_records = [r for r in filtered_records if r.get("pdfStatus") == "error" or r.get("requestStatus") == "error"]
            elif status_filter == "pending":
                filtered_records = [r for r in filtered_records if r.get("pdfStatus") == "pending" or r.get("requestStatus") == "pending"]
        
        # Apply type filter
        if type_filter != "all":
            filtered_records = [r for r in filtered_records if r.get("requestType") == type_filter]
        
        # Sort by timestamp (newest first)
        filtered_records.sort(key=lambda x: self._parse_timestamp(x.get("timestamp", "")), reverse=True)
        
        return filtered_records
    
    def _collect_processing_records(self, date_filter: str, status_filter: str, type_filter: str) -> List[Dict[str, Any]]:
        """Collect records from various sources"""
        records = []
        
        # Get SmartRequest tracking data
        smartrequest_records = self.request_tracker.list_all_requests()
        
        # Get PDF generation logs
        pdf_records = self._get_pdf_logs()
        
        # Merge and enhance records
        record_map = {}
        
        # Process SmartRequest records
        for sr_record in smartrequest_records:
            record_id = sr_record.record_id
            if record_id not in record_map:
                record_map[record_id] = {
                    "recordId": record_id,
                    "patientName": sr_record.patient_name,
                    "facilityName": sr_record.facility_name,
                    "requestStatus": "success",  # Assume success if tracked
                    "requestId": sr_record.request_id,
                    "requestType": sr_record.document_type,
                    "timestamp": sr_record.created_at,
                    "pdfStatus": "unknown",
                    "pdfPath": None
                }
        
        # Process PDF generation logs
        for pdf_record in pdf_records:
            record_id = pdf_record.get("record", "")
            if record_id:
                if record_id not in record_map:
                    record_map[record_id] = {
                        "recordId": record_id,
                        "patientName": None,
                        "facilityName": None,
                        "requestStatus": "unknown",
                        "requestId": None,
                        "requestType": pdf_record.get("request_type", ""),
                        "timestamp": pdf_record.get("timestamp", ""),
                        "pdfStatus": pdf_record.get("status", "unknown"),
                        "pdfPath": self._find_pdf_path(record_id, pdf_record.get("request_type", ""))
                    }
                else:
                    # Update existing record with PDF info
                    record_map[record_id]["pdfStatus"] = pdf_record.get("status", "unknown")
                    record_map[record_id]["pdfPath"] = self._find_pdf_path(record_id, pdf_record.get("request_type", ""))
        
        # Convert to list and apply filters
        records = list(record_map.values())
        
        # Apply date filter
        if date_filter != "all":
            cutoff_date = self._get_cutoff_date(date_filter)
            records = [r for r in records if self._parse_timestamp(r.get("timestamp", "")) >= cutoff_date]
        
        # Apply status filter
        if status_filter != "all":
            if status_filter == "success":
                records = [r for r in records if r.get("pdfStatus") == "success" or r.get("requestStatus") == "success"]
            elif status_filter == "error":
                records = [r for r in records if r.get("pdfStatus") == "error" or r.get("requestStatus") == "error"]
            elif status_filter == "pending":
                records = [r for r in records if r.get("pdfStatus") == "pending" or r.get("requestStatus") == "pending"]
        
        # Apply type filter
        if type_filter != "all":
            records = [r for r in records if r.get("requestType") == type_filter]
        
        # Sort by timestamp (newest first)
        records.sort(key=lambda x: self._parse_timestamp(x.get("timestamp", "")), reverse=True)
        
        return records
    
    def _get_pdf_logs(self) -> List[Dict[str, Any]]:
        """Read PDF generation logs"""
        pdf_logs = []
        
        # Read from PDF logs directory
        pdf_logs_dir = self.logs_dir / "pdfs"
        if pdf_logs_dir.exists():
            for log_file in pdf_logs_dir.glob("logs_*.csv"):
                try:
                    import pandas as pd
                    df = pd.read_csv(log_file)
                    for _, row in df.iterrows():
                        pdf_logs.append(row.to_dict())
                except Exception as e:
                    print(f"⚠️ Error reading log file {log_file}: {e}")
        
        # Also read from main logs directory
        for log_file in self.logs_dir.glob("logs_*.csv"):
            try:
                import pandas as pd
                df = pd.read_csv(log_file)
                for _, row in df.iterrows():
                    if "PDF" in str(row.get("details", "")):
                        pdf_logs.append(row.to_dict())
            except Exception as e:
                print(f"⚠️ Error reading log file {log_file}: {e}")
        
        return pdf_logs
    
    def _find_pdf_path(self, record_id: str, request_type: str) -> Optional[str]:
        """Find the actual PDF file path for a record"""
        if not self.output_dir.exists():
            return None
        
        # Search in output directory structure
        for pdf_file in self.output_dir.rglob("*.pdf"):
            if record_id in pdf_file.name:
                return str(pdf_file.relative_to("."))
        
        return None
    
    def _calculate_stats(self, records: List[Dict[str, Any]]) -> Dict[str, int]:
        """Calculate dashboard statistics"""
        stats = {
            "totalPdfs": 0,
            "totalRequests": 0,
            "pdfErrors": 0,
            "requestFailures": 0
        }
        
        for record in records:
            # Count PDFs
            if record.get("pdfStatus") in ["success", "generated"]:
                stats["totalPdfs"] += 1
            elif record.get("pdfStatus") == "error":
                stats["pdfErrors"] += 1
            
            # Count SmartRequests
            if record.get("requestId"):
                stats["totalRequests"] += 1
                if record.get("requestStatus") == "error":
                    stats["requestFailures"] += 1
        
        return stats
    
    def _get_cutoff_date(self, date_filter: str) -> datetime:
        """Get cutoff date for filtering"""
        now = datetime.now()
        
        if date_filter == "today":
            return now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif date_filter == "week":
            return now - timedelta(days=7)
        elif date_filter == "month":
            return now - timedelta(days=30)
        else:
            return datetime.min
    
    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """Parse timestamp string to datetime object"""
        if not timestamp_str:
            return datetime.min
        
        try:
            # Try different timestamp formats
            formats = [
                "%Y-%m-%dT%H:%M:%S.%f",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d",
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(timestamp_str, fmt)
                except ValueError:
                    continue
            
            # If ISO format with timezone
            if 'T' in timestamp_str and ('+' in timestamp_str or 'Z' in timestamp_str):
                from dateutil import parser
                return parser.parse(timestamp_str).replace(tzinfo=None)
            
            return datetime.min
        except Exception:
            return datetime.min


# Initialize data service
data_service = DashboardDataService()


@app.route('/')
def dashboard():
    """Serve the main dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/dashboard-data')
def api_dashboard_data():
    """API endpoint to get dashboard data"""
    date_filter = request.args.get('date', 'all')
    status_filter = request.args.get('status', 'all')
    type_filter = request.args.get('type', 'all')
    
    try:
        data = data_service.get_dashboard_data(date_filter, status_filter, type_filter)
        return jsonify(data)
    except Exception as e:
        print(f"❌ Error getting dashboard data: {e}")
        return jsonify({
            "error": str(e),
            "records": [],
            "stats": {
                "totalPdfs": 0,
                "totalRequests": 0,
                "pdfErrors": 0,
                "requestFailures": 0
            }
        }), 500


@app.route('/pdf/<path:filename>')
def serve_pdf(filename):
    """Serve PDF files"""
    try:
        from urllib.parse import unquote
        
        # URL decode the filename to handle encoded slashes
        decoded_filename = unquote(filename)
        
        # Clean the path - remove trailing backslashes and normalize
        cleaned_filename = decoded_filename.rstrip('\\').rstrip('/')
        print(f"🔍 Serving PDF: {cleaned_filename}")
        
        # Security: ensure the file is within the output directory
        if not cleaned_filename.startswith('output/'):
            print(f"❌ Access denied - path outside output directory: {cleaned_filename}")
            return "Access denied", 403
        
        # Construct path relative to project root (not app directory)
        # Find project root by looking for the output directory
        current_dir = Path.cwd()
        project_root = current_dir
        
        # If we're in app/ directory, go up one level
        if current_dir.name == 'app':
            project_root = current_dir.parent
        
        # Double-check by looking for output directory
        if not (project_root / 'output').exists():
            # Try going up one more level
            project_root = project_root.parent
        
        pdf_path = project_root / cleaned_filename
        print(f"🔍 Project root: {project_root}")
        print(f"🔍 Final PDF path: {pdf_path}")
        
        # Check if file exists and is a PDF
        if pdf_path.exists() and pdf_path.suffix.lower() == '.pdf':
            print(f"✅ Found PDF file: {pdf_path}")
            return send_file(pdf_path, as_attachment=False)
        else:
            print(f"❌ PDF not found: {pdf_path}")
            # List what files are actually in that directory for debugging
            if pdf_path.parent.exists():
                files = list(pdf_path.parent.glob("*"))
                print(f"🔍 Files in {pdf_path.parent}: {files}")
            return "PDF not found", 404
    except Exception as e:
        print(f"❌ Error serving PDF {filename}: {e}")
        import traceback
        traceback.print_exc()
        return "Error serving PDF", 500


@app.route('/api/records/<record_id>')
def api_record_detail(record_id):
    """Get detailed information about a specific record"""
    try:
        # Get SmartRequest details
        sr_record = data_service.request_tracker.get_request(record_id)
        
        # Get related records by record ID
        related_records = data_service.request_tracker.get_requests_by_record_id(record_id)
        
        record_detail = {
            "recordId": record_id,
            "smartrequestRecord": sr_record.to_dict() if sr_record else None,
            "relatedRecords": [r.to_dict() for r in related_records],
            "pdfPath": data_service._find_pdf_path(record_id, ""),
        }
        
        return jsonify(record_detail)
    except Exception as e:
        print(f"❌ Error getting record detail for {record_id}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/smartrequest/<request_id>/status')
def api_smartrequest_status(request_id):
    """Get SmartRequest status from API"""
    try:
        from services.external_api_service import get_smartrequest_status
        
        status = get_smartrequest_status(request_id)
        if status:
            return jsonify(status)
        else:
            return jsonify({"error": "Request not found"}), 404
    except Exception as e:
        print(f"❌ Error getting SmartRequest status for {request_id}: {e}")
        return jsonify({"error": str(e)}), 500


def main():
    """Main function to run the dashboard server"""
    print("🌐 Starting Medicos Dashboard Server...")
    print(f"📊 Dashboard will be available at: http://localhost:5001")
    print(f"🔗 API endpoint: http://localhost:5001/api/dashboard-data")
    
    # Check templates directory (try multiple possible locations)
    possible_template_paths = [
        Path("templates"),           # When run from app directory
        Path("app/templates"),       # When run from project root
        Path("./app/templates")      # Alternative project root
    ]
    
    template_found = False
    template_dir = None
    
    for template_path in possible_template_paths:
        template_file = template_path / "dashboard.html"
        if template_file.exists():
            template_dir = template_path
            template_found = True
            break
    
    if not template_found:
        print(f"❌ Dashboard template not found in any of these locations:")
        for path in possible_template_paths:
            print(f"   - {path}/dashboard.html")
        print(f"💡 Please ensure dashboard.html exists in one of these locations")
        print(f"🔄 Alternative: Use the simple dashboard (no Flask required):")
        print(f"   python app/simple_dashboard.py")
        return
    else:
        print(f"✅ Template found: {template_dir}/dashboard.html")
        # Configure Flask template folder
        app.template_folder = str(template_dir.absolute())
        print(f"🔧 Flask template folder set to: {app.template_folder}")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5001, debug=True)


if __name__ == "__main__":
    main()