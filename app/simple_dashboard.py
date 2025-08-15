#!/usr/bin/env python
"""
Simple Dashboard Server for Medicos (No Flask Required)
Uses Python's built-in HTTP server to provide dashboard functionality
"""

import os
import sys
import json
import html
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import mimetypes

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from utils.request_tracker import SmartRequestTracker
from utils.dashboard_tracker import dashboard_tracker

class DashboardHTTPHandler(BaseHTTPRequestHandler):
    """HTTP handler for the dashboard server"""
    
    def __init__(self, *args, **kwargs):
        self.dashboard_data_service = DashboardDataService()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)
        
        try:
            if path == '/' or path == '/dashboard':
                self.serve_dashboard()
            elif path == '/api/dashboard-data':
                self.serve_dashboard_data(query_params)
            elif path.startswith('/pdf/'):
                self.serve_pdf_file(path[5:])  # Remove '/pdf/' prefix
            elif path.startswith('/api/records/'):
                record_id = path.split('/')[-1]
                self.serve_record_detail(record_id)
            else:
                self.send_error(404, "Not Found")
        except Exception as e:
            print(f"❌ Error handling request {path}: {e}")
            self.send_error(500, f"Internal Server Error: {e}")
    
    def serve_dashboard(self):
        """Serve the main dashboard HTML page"""
        try:
            dashboard_html = self.generate_dashboard_html()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(dashboard_html.encode('utf-8'))))
            self.end_headers()
            self.wfile.write(dashboard_html.encode('utf-8'))
        except Exception as e:
            print(f"❌ Error serving dashboard: {e}")
            self.send_error(500, f"Error generating dashboard: {e}")
    
    def serve_dashboard_data(self, query_params):
        """Serve dashboard data as JSON"""
        try:
            date_filter = query_params.get('date', ['all'])[0]
            status_filter = query_params.get('status', ['all'])[0]
            type_filter = query_params.get('type', ['all'])[0]
            
            data = self.dashboard_data_service.get_dashboard_data(date_filter, status_filter, type_filter)
            json_data = json.dumps(data, indent=2, default=str)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(json_data.encode('utf-8'))))
            self.end_headers()
            self.wfile.write(json_data.encode('utf-8'))
        except Exception as e:
            print(f"❌ Error serving dashboard data: {e}")
            error_data = json.dumps({"error": str(e), "records": [], "stats": {}})
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(error_data.encode('utf-8'))
    
    def serve_pdf_file(self, filename):
        """Serve PDF files"""
        try:
            from urllib.parse import unquote
            
            # URL decode the filename to handle encoded slashes
            decoded_filename = unquote(filename)
            
            # Clean the path - remove trailing backslashes and normalize
            cleaned_filename = decoded_filename.rstrip('\\').rstrip('/')
            print(f"🔍 Serving PDF: {cleaned_filename}")
            
            # Security: ensure the file is within allowed directories
            if not cleaned_filename.startswith('output/'):
                print(f"❌ Access denied - path outside output directory: {cleaned_filename}")
                self.send_error(403, "Access denied")
                return
            
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
            if pdf_path.exists() and pdf_path.suffix.lower() == '.pdf':
                print(f"✅ Found PDF file: {pdf_path}")
                with open(pdf_path, 'rb') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/pdf')
                self.send_header('Content-Length', str(len(content)))
                self.send_header('Content-Disposition', f'inline; filename="{pdf_path.name}"')
                self.end_headers()
                self.wfile.write(content)
            else:
                print(f"❌ PDF not found: {pdf_path}")
                # List what files are actually in that directory for debugging
                if pdf_path.parent.exists():
                    files = list(pdf_path.parent.glob("*"))
                    print(f"🔍 Files in {pdf_path.parent}: {files}")
                self.send_error(404, "PDF not found")
        except Exception as e:
            print(f"❌ Error serving PDF {filename}: {e}")
            import traceback
            traceback.print_exc()
            self.send_error(500, f"Error serving PDF: {e}")
    
    def serve_record_detail(self, record_id):
        """Serve detailed record information"""
        try:
            detail = {"recordId": record_id, "message": "Feature available in full Flask version"}
            json_data = json.dumps(detail, indent=2)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json_data.encode('utf-8'))
        except Exception as e:
            print(f"❌ Error serving record detail: {e}")
            self.send_error(500, f"Error getting record detail: {e}")
    
    def generate_dashboard_html(self):
        """Generate the dashboard HTML dynamically"""
        # Get current data for the dashboard
        data = self.dashboard_data_service.get_dashboard_data()
        stats = data.get('stats', {})
        records = data.get('records', [])
        
        # Generate records table HTML
        records_html = ""
        if records:
            for record in records[:50]:  # Limit to 50 records for performance
                records_html += f"""
                    <tr>
                        <td><strong>{html.escape(str(record.get('recordId', '')))}</strong></td>
                        <td>{html.escape(str(record.get('patientName', 'N/A')))}</td>
                        <td>{html.escape(str(record.get('facilityName', 'N/A')))}</td>
                        <td>
                            <span class="status-badge status-{record.get('pdfStatus', 'unknown')}">
                                {html.escape(str(record.get('pdfStatus', 'unknown')))}
                            </span>
                        </td>
                        <td>
                            {f'<a href="/pdf/{html.escape(str(record.get("pdfPath", "")))}" class="pdf-link" target="_blank">📄 View PDF</a>' 
                             if record.get('pdfPath') else 'N/A'}
                        </td>
                        <td>
                            <span class="status-badge status-{record.get('requestStatus', 'unknown')}">
                                {html.escape(str(record.get('requestStatus', 'unknown')))}
                            </span>
                        </td>
                        <td>
                            {f'<span class="request-id">{html.escape(str(record.get("requestId", "")))}</span>' 
                             if record.get('requestId') else 'N/A'}
                        </td>
                        <td>{html.escape(str(record.get('requestType', 'N/A')))}</td>
                        <td>{html.escape(str(record.get('timestamp', 'N/A'))[:19])}</td>
                    </tr>
                """
        else:
            records_html = """
                <tr>
                    <td colspan="9" class="empty-state">
                        <h3>No records found</h3>
                        <p>Run your PDF generation workflow to see data here</p>
                    </td>
                </tr>
            """
        
        # Generate complete HTML
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Medicos - PDF & SmartRequest Dashboard</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f7fa; color: #333; line-height: 1.6; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem 2rem; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header h1 {{ font-size: 2rem; margin-bottom: 0.5rem; }}
                .header p {{ opacity: 0.9; font-size: 1.1rem; }}
                .container {{ max-width: 1400px; margin: 0 auto; padding: 2rem; }}
                .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }}
                .stat-card {{ background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .stat-card h3 {{ color: #666; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem; }}
                .stat-card .number {{ font-size: 2.5rem; font-weight: bold; color: #4a5568; }}
                .stat-card.success .number {{ color: #48bb78; }}
                .stat-card.warning .number {{ color: #ed8936; }}
                .stat-card.error .number {{ color: #f56565; }}
                .stat-card.info .number {{ color: #4299e1; }}
                .controls {{ background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 2rem; text-align: center; }}
                .btn {{ padding: 0.5rem 1rem; background: #667eea; color: white; border: none; border-radius: 6px; cursor: pointer; margin: 0.5rem; text-decoration: none; display: inline-block; }}
                .btn:hover {{ background: #5a67d8; }}
                .btn.refresh {{ background: #48bb78; }}
                .data-table {{ background: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); overflow: hidden; }}
                .table-header {{ background: #f7fafc; padding: 1rem 1.5rem; border-bottom: 1px solid #e2e8f0; }}
                .table-wrapper {{ overflow-x: auto; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ text-align: left; padding: 1rem; border-bottom: 1px solid #e2e8f0; }}
                th {{ background: #f7fafc; font-weight: 600; color: #4a5568; font-size: 0.85rem; text-transform: uppercase; }}
                tr:hover {{ background: #f7fafc; }}
                .status-badge {{ display: inline-block; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; }}
                .status-success {{ background: #c6f6d5; color: #22543d; }}
                .status-error {{ background: #fed7d7; color: #742a2a; }}
                .status-pending {{ background: #bee3f8; color: #2a4365; }}
                .status-unknown {{ background: #e2e8f0; color: #4a5568; }}
                .pdf-link {{ color: #667eea; text-decoration: none; font-weight: 500; }}
                .pdf-link:hover {{ text-decoration: underline; }}
                .request-id {{ font-family: 'Courier New', monospace; background: #f7fafc; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem; }}
                .empty-state {{ text-align: center; padding: 3rem; color: #666; }}
                .footer {{ text-align: center; padding: 2rem; color: #666; font-size: 0.9rem; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📋 Medicos Dashboard</h1>
                <p>PDF Generation & SmartRequest Tracking (Simple Version)</p>
            </div>

            <div class="container">
                <!-- Statistics Cards -->
                <div class="stats-grid">
                    <div class="stat-card success">
                        <h3>Total PDFs Generated</h3>
                        <div class="number">{stats.get('totalPdfs', 0)}</div>
                    </div>
                    <div class="stat-card info">
                        <h3>SmartRequests Sent</h3>
                        <div class="number">{stats.get('totalRequests', 0)}</div>
                    </div>
                    <div class="stat-card warning">
                        <h3>PDF Errors</h3>
                        <div class="number">{stats.get('pdfErrors', 0)}</div>
                    </div>
                    <div class="stat-card error">
                        <h3>Request Failures</h3>
                        <div class="number">{stats.get('requestFailures', 0)}</div>
                    </div>
                </div>

                <!-- Controls -->
                <div class="controls">
                    <a href="/" class="btn refresh">🔄 Refresh Dashboard</a>
                    <a href="/api/dashboard-data" class="btn" target="_blank">📊 View Raw Data</a>
                    <span style="margin-left: 1rem; color: #666;">
                        Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    </span>
                </div>

                <!-- Data Table -->
                <div class="data-table">
                    <div class="table-header">
                        <h2>Processing Records (Latest {len(records)} records)</h2>
                    </div>
                    <div class="table-wrapper">
                        <table>
                            <thead>
                                <tr>
                                    <th>Record ID</th>
                                    <th>Patient Name</th>
                                    <th>Facility</th>
                                    <th>PDF Status</th>
                                    <th>PDF Path</th>
                                    <th>SmartRequest Status</th>
                                    <th>Request ID</th>
                                    <th>Request Type</th>
                                    <th>Timestamp</th>
                                </tr>
                            </thead>
                            <tbody>
                                {records_html}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            
            <div class="footer">
                <p>🎯 <strong>Simple Dashboard Mode</strong> - For full features, install Flask: <code>pip install flask python-dateutil</code></p>
                <p>📁 Data stored in: <code>app/logs/dashboard_tracking.json</code></p>
            </div>
        </body>
        </html>
        """
        
        return html_content


class DashboardDataService:
    """Service to collect and aggregate dashboard data (simplified version)"""
    
    def __init__(self):
        self.request_tracker = SmartRequestTracker()
        self.output_dir = Path("output")
        self.logs_dir = Path("logs")
        
    def get_dashboard_data(self, date_filter: str = "all", status_filter: str = "all", type_filter: str = "all") -> Dict[str, Any]:
        """Collect dashboard data from tracking files"""
        try:
            # Get dashboard tracker data
            summary = dashboard_tracker.get_dashboard_summary()
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
            
            # Apply basic filtering
            if date_filter == "today":
                today = datetime.now().strftime('%Y-%m-%d')
                record_dicts = [r for r in record_dicts if today in str(r.get('timestamp', ''))]
            
            # Calculate stats
            stats = {
                "totalPdfs": len([r for r in record_dicts if r.get('pdfStatus') == 'success']),
                "totalRequests": len([r for r in record_dicts if r.get('requestId')]),
                "pdfErrors": len([r for r in record_dicts if r.get('pdfStatus') == 'error']),
                "requestFailures": len([r for r in record_dicts if r.get('requestStatus') == 'error'])
            }
            
            return {
                "records": record_dicts[-50:],  # Show latest 50 records
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


def main():
    """Main function to run the simple dashboard server"""
    print("🌐 Starting Simple Medicos Dashboard Server...")
    print("📊 Dashboard will be available at: http://localhost:8000")
    print("🔗 API endpoint: http://localhost:8000/api/dashboard-data")
    print("💡 This is a simplified version using Python's built-in HTTP server")
    print("   For full features, install Flask: pip install flask python-dateutil")
    print()
    
    try:
        # Create HTTP server
        server = HTTPServer(('localhost', 8000), DashboardHTTPHandler)
        print("✅ Server started successfully!")
        print("🔄 Press Ctrl+C to stop the server")
        print()
        
        # Start serving
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("\n💡 Troubleshooting:")
        print("   - Make sure port 8000 is not in use")
        print("   - Try running from the app directory")
        print("   - Check file permissions")


if __name__ == "__main__":
    main()