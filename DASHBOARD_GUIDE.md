# 📊 Medicos Dashboard Guide

This guide explains how to use the Medicos Dashboard to view PDF generation status and track SmartRequest (Datavant) API calls.

## 🎯 Overview

The Medicos Dashboard provides a web-based interface to monitor:
- ✅ PDF generation status and file paths
- 📤 SmartRequest API calls and success/failure status
- 📊 Real-time statistics and processing summaries
- 🔍 Detailed tracking of each record processed

## 🚀 Getting Started

### Prerequisites
- Flask (will be automatically available if you have all requirements)
- Python 3.7+
- Your medicos application properly configured

### Starting the Dashboard

1. **Start the dashboard server:**
   ```bash
   python app/dashboard_server.py
   ```

2. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

3. **The dashboard will automatically display:**
   - Real-time processing statistics
   - List of all processed records
   - PDF and SmartRequest status for each record

## 📋 Dashboard Features

### Statistics Cards
- **Total PDFs Generated**: Count of successfully generated PDF files
- **SmartRequests Sent**: Number of SmartRequest API calls made
- **PDF Errors**: Count of PDF generation failures
- **Request Failures**: Number of failed SmartRequest API calls

### Filter Options
- **Date Range**: Filter by Today, Last 7 days, Last 30 days, or All time
- **Status**: Filter by Success, Error, or Pending status
- **Request Type**: Filter by First Request, Second Complete, or Second Partial

### Records Table
Each record shows:
- **Record ID**: Unique identifier for the medical record
- **Patient Name**: Patient's name (if available)
- **Facility**: Medical facility name
- **PDF Status**: Success/Error/Pending with status badge
- **PDF Path**: Clickable link to view generated PDF
- **SmartRequest Status**: API call status with badge
- **Request ID**: SmartRequest API request ID
- **Request Type**: Type of processing (first_request, etc.)
- **Timestamp**: When the processing occurred

## 🔗 API Endpoints

The dashboard provides several API endpoints for integration:

### Get Dashboard Data
```
GET /api/dashboard-data
```
Returns complete dashboard data including records and statistics.

**Query Parameters:**
- `date`: Date filter (today, week, month, all)
- `status`: Status filter (success, error, pending, all)
- `type`: Request type filter (first_request, second_request_complete, etc.)

**Example Response:**
```json
{
  "records": [
    {
      "recordId": "TNSC023087781",
      "patientName": "John Doe",
      "facilityName": "City Medical Center",
      "pdfStatus": "success",
      "pdfPath": "output/2025_08_15/TNSC023087781_0.pdf",
      "requestStatus": "success",
      "requestId": "1001",
      "requestType": "first_request",
      "timestamp": "2025-08-15T10:30:00Z"
    }
  ],
  "stats": {
    "totalPdfs": 12,
    "totalRequests": 8,
    "pdfErrors": 2,
    "requestFailures": 1
  }
}
```

### View PDF Files
```
GET /pdf/<filepath>
```
Serves PDF files for viewing in the browser.

### Get Record Details
```
GET /api/records/<record_id>
```
Returns detailed information about a specific record.

### Get SmartRequest Status
```
GET /api/smartrequest/<request_id>/status
```
Gets the current status of a SmartRequest from the API.

## 🔧 Integration with Your Workflow

The dashboard automatically tracks your existing workflow. No changes needed to your main processing logic!

### Automatic Tracking
When you run your normal PDF generation:
```bash
python app/main.py
```

The system automatically:
1. **Tracks Processing Start**: Records when processing begins
2. **Monitors PDF Generation**: Success/failure status and file paths
3. **Tracks SmartRequest Calls**: API calls and response status
4. **Updates Dashboard**: Real-time updates visible in web interface

### Manual Tracking (Advanced)
You can also manually track events in your custom code:

```python
from app.utils.dashboard_tracker import (
    track_processing_start, track_pdf_success, track_pdf_error,
    track_smartrequest_sent, track_smartrequest_success
)

# Start tracking a new record
track_processing_start("RECORD123", "first_request", "John Doe", "City Hospital")

# Track PDF generation
track_pdf_success("RECORD123", "output/RECORD123.pdf", "mother_template")

# Track SmartRequest
track_smartrequest_sent("RECORD123", "SR123456")
track_smartrequest_success("RECORD123", "SR123456")
```

## 📁 Data Storage

Dashboard data is stored in:
- **Main tracking**: `app/logs/dashboard_tracking.json`
- **SmartRequest IDs**: `app/logs/smartrequest_tracker.json`
- **Processing logs**: `app/logs/` (various CSV files)

## 🔄 Real-time Updates

The dashboard automatically refreshes every 30 seconds to show the latest data. You can also manually refresh using the "🔄 Refresh" button.

## 🎨 Dashboard Interface

### Status Badges
- 🟢 **Success**: Green badge for successful operations
- 🔴 **Error**: Red badge for failed operations  
- 🟡 **Pending**: Yellow badge for operations in progress
- 🔵 **Info**: Blue badge for informational status

### PDF Links
- 📄 **View PDF**: Click to open PDF files in a new tab
- **N/A**: Displayed when PDF generation failed or path not available

### Request IDs
- Monospace font display for easy copying
- Clickable to get detailed SmartRequest status

## 🛠️ Troubleshooting

### Dashboard Won't Start
```bash
# Check if Flask is installed
pip list | grep -i flask

# Install missing dependencies
pip install flask python-dateutil
```

### No Data Showing
1. **Run some processing first:**
   ```bash
   python app/main.py
   ```

2. **Check tracking files exist:**
   ```bash
   ls app/logs/dashboard_tracking.json
   ```

3. **Test tracking manually:**
   ```bash
   python test_dashboard_integration.py
   ```

### PDF Links Not Working
- Ensure PDF files exist in the `output/` directory
- Check file permissions
- Verify the PDF path is correct in the tracking data

### SmartRequest Status Not Updating
- Check your SmartRequest API configuration
- Verify faker mode is working: Look for "🎭 SmartRequest: Using faker mode" messages
- Check network connectivity for production API calls

## 📊 Monitoring Multiple Runs

The dashboard accumulates data from multiple processing runs. Each time you run the main application, new records are added to the dashboard.

### Viewing Historical Data
- Use date filters to see specific time periods
- All processing history is preserved in JSON files
- Export data using the API endpoints for external analysis

### Clearing Old Data
To reset the dashboard data:
```bash
# Backup current data (optional)
cp app/logs/dashboard_tracking.json app/logs/dashboard_tracking_backup.json

# Clear tracking data
rm app/logs/dashboard_tracking.json

# Restart processing to generate new data
```

## 🔐 Security Considerations

### Local Access Only
The dashboard runs on localhost (127.0.0.1) by default and is only accessible from your local machine.

### Sensitive Data
- Patient information is stored locally only
- SmartRequest authorization forms are not stored in tracking data
- API credentials are handled separately through environment variables

### Production Deployment
For production use:
1. Use a proper WSGI server (not Flask's development server)
2. Configure proper authentication
3. Use HTTPS
4. Set up proper access controls

## 🎯 Use Cases

### Development and Testing
- Monitor PDF generation during development
- Test SmartRequest integration with faker mode
- Debug processing issues by viewing detailed status

### Production Monitoring  
- Track daily processing statistics
- Monitor for PDF generation failures
- Ensure SmartRequest API calls are successful
- Generate reports on processing volumes

### Quality Assurance
- Verify all records are processed correctly
- Check that SmartRequest calls match PDF generation
- Review error patterns and frequencies

## 🚀 Advanced Features

### Custom Filtering
Combine multiple filters to find specific records:
- Date + Status: Find all errors from last week
- Type + Status: Find all successful first requests
- Custom API calls: Use the API directly for complex queries

### Batch Operations
View processing statistics for batch operations:
- Track multiple records processed together
- Monitor batch completion rates
- Identify batch processing bottlenecks

### Integration with External Systems
Use the API endpoints to:
- Export data to external monitoring systems
- Create custom reporting dashboards
- Integrate with alerting systems

---

## 🆘 Support

If you encounter issues with the dashboard:

1. **Check the console output** for error messages
2. **Review the log files** in `app/logs/`
3. **Test with the integration script**: `python test_dashboard_integration.py`
4. **Verify your environment configuration** matches the requirements

The dashboard is designed to enhance your workflow visibility without disrupting existing operations. Happy monitoring! 📊✨