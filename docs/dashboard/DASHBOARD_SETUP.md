# 🚀 Dashboard Setup Guide

This guide will help you set up and run the Medicos Dashboard to monitor PDF generation and SmartRequest API calls.

## 🎯 Quick Start (3 Options)

### Option 1: Automatic Setup (Recommended)
```bash
python run_dashboard.py
```
This script will:
- Detect if Flask is installed
- Offer to install Flask automatically
- Run the appropriate dashboard version

### Option 2: Simple Dashboard (No Installation Required)
```bash
python app/simple_dashboard.py
```
- Uses Python's built-in HTTP server
- No additional dependencies needed
- Basic functionality
- Access at: http://localhost:8000

### Option 3: Full Flask Dashboard (Advanced Features)
```bash
# Install Flask first
pip install flask python-dateutil

# Then run the full dashboard
python app/dashboard_server.py
```
- Full-featured web interface
- Advanced filtering and real-time updates
- Access at: http://localhost:5000

## 📋 What You'll See

Both dashboard versions show:
- ✅ **PDF Generation Status**: Success/error for each document
- 📤 **SmartRequest Tracking**: API calls and their status
- 📊 **Statistics**: Real-time counts and success rates
- 👤 **Patient Information**: Names and facility details
- 📁 **PDF Links**: Click to view generated PDF files

## 🔧 Installation Details

### Requirements
- Python 3.7+
- Your existing medicos application
- Optional: Flask for advanced features

### Flask Installation
If you want the full-featured dashboard:
```bash
pip install flask python-dateutil
```

### Verifying Installation
```bash
# Check if Flask is available
python -c "import flask; print('Flask available')"

# Test dashboard tracking
python test_dashboard_integration.py
```

## 🎮 Using the Dashboard

### 1. Start the Dashboard
Choose one of the three options above to start the dashboard server.

### 2. Run Your Normal Workflow
In another terminal, run your PDF generation:
```bash
python app/main.py
```

### 3. View Results
Open your browser to:
- **Simple Dashboard**: http://localhost:8000
- **Flask Dashboard**: http://localhost:5000

### 4. Monitor in Real-time
- Watch PDFs being generated
- See SmartRequest API calls
- Track success/failure rates
- Click PDF links to view files

## 📊 Dashboard Features

### Simple Dashboard (No Flask)
- ✅ Real-time statistics
- ✅ Records table with PDF links
- ✅ SmartRequest status tracking
- ✅ Basic filtering
- ✅ No dependencies required

### Full Flask Dashboard (With Flask)
- ✅ All simple dashboard features
- ✅ Advanced filtering (date, status, type)
- ✅ Auto-refresh every 30 seconds
- ✅ REST API endpoints
- ✅ Detailed record views
- ✅ Mobile-responsive design

## 🛠️ Troubleshooting

### Dashboard Won't Start
1. **Check Python version**:
   ```bash
   python --version  # Should be 3.7+
   ```

2. **Try the simple dashboard**:
   ```bash
   python app/simple_dashboard.py
   ```

3. **Check port availability**:
   ```bash
   # Kill any process using the port
   lsof -ti:8000 | xargs kill -9  # For simple dashboard
   lsof -ti:5000 | xargs kill -9  # For Flask dashboard
   ```

### No Data Showing
1. **Run some processing first**:
   ```bash
   python app/main.py
   ```

2. **Check tracking files**:
   ```bash
   ls app/logs/dashboard_tracking.json
   ```

3. **Test manually**:
   ```bash
   python test_dashboard_integration.py
   ```

### Flask Installation Issues
1. **Try upgrading pip**:
   ```bash
   python -m pip install --upgrade pip
   ```

2. **Use simple dashboard instead**:
   ```bash
   python app/simple_dashboard.py
   ```

3. **Check virtual environment**:
   ```bash
   # If using venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

### PDF Links Not Working
1. **Check PDF files exist**:
   ```bash
   ls output/
   ```

2. **Verify file permissions**:
   ```bash
   chmod 644 output/*.pdf
   ```

3. **Check output directory structure**:
   ```bash
   find output -name "*.pdf" -type f
   ```

## 🔐 Security Notes

### Local Access Only
Both dashboard versions run on localhost by default and are only accessible from your local machine.

### Data Privacy
- Patient information stays on your local machine
- No data is sent to external servers
- SmartRequest credentials handled separately

### Production Use
For production deployment:
- Use a proper web server (nginx, Apache)
- Configure proper authentication
- Use HTTPS
- Set up access controls

## 📈 Data Storage

Dashboard data is stored in:
- **Main tracking**: `app/logs/dashboard_tracking.json`
- **SmartRequest IDs**: `app/logs/smartrequest_tracker.json`
- **Processing logs**: `app/logs/*.csv`

### Backing Up Data
```bash
# Backup all dashboard data
cp -r app/logs app/logs_backup_$(date +%Y%m%d)
```

### Clearing Old Data
```bash
# Clear dashboard tracking (keeps backups)
mv app/logs/dashboard_tracking.json app/logs/dashboard_tracking_backup.json
```

## 🎯 Use Cases

### Development
- Monitor PDF generation during development
- Debug processing issues
- Test SmartRequest integration

### Production Monitoring
- Track daily processing volumes
- Monitor error rates
- Ensure API calls succeed

### Quality Assurance
- Verify all records processed correctly
- Review error patterns
- Generate processing reports

## 🆘 Getting Help

If you encounter issues:

1. **Check this guide** for common solutions
2. **Test with the integration script**: 
   ```bash
   python test_dashboard_integration.py
   ```
3. **Try the simple dashboard** if Flask has issues
4. **Check the console output** for error messages
5. **Review log files** in `app/logs/`

## 🎉 Success!

Once your dashboard is running:
- Navigate to the dashboard URL in your browser
- Run your PDF generation workflow
- Watch real-time updates of processing status
- Click PDF links to view generated files
- Monitor SmartRequest API success rates

The dashboard enhances your workflow visibility without changing your existing operations. Happy monitoring! 📊✨