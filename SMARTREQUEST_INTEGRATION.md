# SmartRequest API Integration

This document describes the SmartRequest (Datavant) API integration implemented in the medicos application.

## Overview

The application now automatically creates SmartRequest API calls when processing document creation workflows. This integration allows for seamless medical records requests to be submitted to the Datavant SmartRequest system during the document generation process.

## Files Added/Modified

### New Files
- `app/services/smartrequest_service.py` - Core SmartRequest API service
- `app/utils/smartrequest_helper.py` - Helper utilities and CLI tools
- `app/utils/request_tracker.py` - Request ID tracking system
- `.env.template` - Environment configuration template
- `SMARTREQUEST_INTEGRATION.md` - This documentation file

### Modified Files
- `app/models/datavant_request.py` - Enhanced with optional fields and validation
- `app/services/external_api_service.py` - Updated to use new SmartRequest service
- `app/services/record_service.py` - Integrated request creation and tracking

## Configuration

### Environment Variables

Copy `.env.template` to `.env` and configure the following variables:

```bash
# Application Environment - set to 'local' for automatic faker mode
ENV=local

# SmartRequest API Configuration
SMARTREQUEST_BASE_URL=https://sandbox-api.datavant.com/v1  # or production URL
SMARTREQUEST_CLIENT_ID=your_client_id_here
SMARTREQUEST_CLIENT_SECRET=your_client_secret_here

# SmartRequest Faker Configuration
USE_SMARTREQUEST_FAKER=false  # Set to 'true' to force faker mode
```

### Faker Mode (Local Testing)

The integration includes a comprehensive faker system that simulates SmartRequest API responses for local testing. Faker mode is automatically enabled when:

- `ENV=local` is set, OR
- SmartRequest credentials are missing/empty, OR  
- `USE_SMARTREQUEST_FAKER=true` is set

**Faker Features:**
- ✅ Realistic authentication responses
- ✅ Dynamic facility data generation with filtering
- ✅ Comprehensive record types and request reasons
- ✅ Request creation with proper ID generation
- ✅ Status tracking simulation
- ✅ Download URL generation
- ✅ Request cancellation simulation

### API Environments

- **Sandbox**: `https://sandbox-api.datavant.com/v1`
- **Production**: `https://requester-api.datavant.com/v1`

**Important**: Sandbox and production credentials are separate and environment-specific.

## Usage

### Automatic Integration

The SmartRequest integration is automatically triggered during document creation workflows:

1. **First Request Processing** (`process_first_request`)
2. **Complete Second Request Processing** (`process_complete_second_request`) 
3. **Partial Second Request Processing** (`process_partial_second_request`)

Each workflow now:
1. Creates the SmartRequest payload from RedCap data
2. Submits the request to SmartRequest API
3. Tracks the returned request ID for future reference
4. Continues with PDF generation as before

### Manual Testing

#### Test API Connection (Faker Mode)
```bash
python -m app.utils.smartrequest_helper test
```

#### Test Full Integration
```bash
python test_fake_smartrequest.py
```

#### List Available Record Types
```bash
python -m app.utils.smartrequest_helper record-types
```

#### Search Facilities
```bash
python -m app.utils.smartrequest_helper facilities
python -m app.utils.smartrequest_helper facilities TX  # Filter by state
```

#### Get Request Reasons
```bash
python -m app.utils.smartrequest_helper reasons 1234567  # Replace with your company ID
```

### Request Tracking

#### View All Tracked Requests
```bash
python -m app.utils.request_tracker list
```

#### Get Request Status
```bash
python -m app.utils.request_tracker status Created
python -m app.utils.smartrequest_helper status <request_id>
```

#### Update Request Status
```bash
python -m app.utils.request_tracker update <request_id> "In Process"
```

## API Workflow

### 1. Authentication
The system automatically handles authentication by:
- Storing client credentials from environment variables
- Requesting access tokens using Basic Auth
- Managing token expiration and renewal
- Using Bearer tokens for API calls

### 2. Request Creation Flow

```python
# 1. Convert RedCap data to SmartRequest format
datavant_request_data = get_datavant_request_data(redcap_data)

# 2. Submit to SmartRequest API
api_response = submit_datavant_request(datavant_request_data)

# 3. Track request ID if successful
if api_response and api_response.get('requestId'):
    track_smartrequest(
        request_id=api_response['requestId'],
        record_id=redcap_data.record,
        document_type="first_request",
        patient_name="Patient Name",
        facility_name="Facility Name"
    )
```

### 3. Request Payload Structure

The system maps RedCap data to SmartRequest format:

```json
{
  "facility": {
    "addressLine1": "123 Main St",
    "city": "Townsville", 
    "state": "ME",
    "zip": "12345",
    "healthSystem": "City Health System",
    "siteName": "City Hospital",
    "phone": "1234567890",
    "fax": "0987654321"
  },
  "requesterInfo": {
    "companyId": 1234567,
    "companyName": "Smith and Smith",
    "name": "Bob Loblaw",
    "email": "bob@example.com"
  },
  "patient": {
    "firstName": "John",
    "lastName": "Smith", 
    "dateOfBirth": "1950-08-19",
    "ssn": "111223333",
    "customId": "RECORD123"
  },
  "reason": {
    "businessType": "ATTY",
    "apiCode": "STATE_ATTY_OFFICE"
  },
  "requestCriteria": [
    {
      "recordTypes": ["Abstract", "Toxicology reports"],
      "startDate": "2024-01-01",
      "endDate": "2024-01-05"
    }
  ],
  "certificationRequired": false,
  "authorizationForms": ["base64_encoded_pdf_content"],
  "callbackDetails": {
    "method": "POST",
    "url": "https://your-callback-url.com",
    "headers": {
      "Authorization": "Bearer token123"
    }
  }
}
```

## Data Mapping

### RedCap to SmartRequest Field Mapping

| RedCap Field | SmartRequest Field | Required | Default |
|--------------|-------------------|----------|---------|
| `mr_address_line_1` | `facility.addressLine1` | Yes | '' |
| `mr_city` | `facility.city` | Yes | '' |
| `mr_state` | `facility.state` | Yes | '' |
| `mr_zip` | `facility.zip` | Yes | '' |
| `mr_health_system` | `facility.healthSystem` | Yes | '' |
| `mr_site_name` | `facility.siteName` | Yes | '' |
| `mr_phone` | `facility.phone` | Yes | '' |
| `mr_fax` | `facility.fax` | Yes | '' |
| `mr_company_id` | `requesterInfo.companyId` | Yes | 0 |
| `mr_company_name` | `requesterInfo.companyName` | Yes | '' |
| `mr_name` | `requesterInfo.name` | Yes | '' |
| `mr_email` | `requesterInfo.email` | Yes | '' |
| `mr_first_name` | `patient.firstName` | Yes | '' |
| `mr_last_name` | `patient.lastName` | Yes | '' |
| `mr_date_of_birth` | `patient.dateOfBirth` | Yes | '' |
| `mr_ssn` | `patient.ssn` | Yes | '' |
| `mr_custom_id` | `patient.customId` | No | record_id |
| `mr_business_type` | `reason.businessType` | No | 'ATTY' |
| `mr_api_code` | `reason.apiCode` | No | 'STATE_ATTY_OFFICE' |
| `mr_record_types` | `requestCriteria[0].recordTypes` | No | ['Abstract'] |
| `mr_start_date` | `requestCriteria[0].startDate` | Yes | '' |
| `mr_end_date` | `requestCriteria[0].endDate` | Yes | '' |
| `mr_certification_required` | `certificationRequired` | No | false |
| `mr_authorization_forms` | `authorizationForms` | No | [] |
| `mr_callback_url` | `callbackDetails.url` | No | null |
| `mr_callback_method` | `callbackDetails.method` | No | 'POST' |
| `mr_callback_authorization` | `callbackDetails.headers.Authorization` | No | '' |

## Error Handling

### Configuration Errors
- Missing environment variables are detected at startup
- Invalid credentials result in authentication failures
- Network timeouts are handled gracefully

### API Errors
- HTTP errors are caught and logged
- Request failures don't stop PDF generation
- Retry logic for temporary failures

### Request Tracking Errors
- JSON storage failures are logged but don't affect main workflow
- Missing request IDs are handled gracefully
- File permission issues are reported

## Request Status Values

SmartRequest API returns these status values:

- **Created**: Request created successfully and queued
- **In Process - Pending Fulfillment**: Queued at facility
- **In Process - Fulfillment**: Being actively worked on
- **In Process - Quality Assurance**: Under quality review
- **In Process - Pending Approval**: Waiting for approval
- **In Process - Preparing Invoice**: Being invoiced
- **In Process - Certification**: Being certified
- **Canceled**: Canceled by requester
- **Canceled by Fulfillment**: Canceled by fulfillment team
- **Correspondence Sent**: Issue occurred, correspondence available
- **Requires Payment**: Payment required before download
- **Preparing Record for Delivery**: Being prepared for download
- **Record Available**: Ready for download

## Document Types Available

- **REQUEST_LETTER**: Original request letter and authorization forms
- **INVOICE**: Payment/billing information
- **MEDICAL_RECORD**: Retrieved medical records
- **CORRESPONDENCE**: Correspondence letters if records not found
- **ALL**: All documents bundled into one PDF

## Monitoring and Logging

### Request Tracking Storage
- Location: `logs/smartrequest_tracker.json`
- Format: JSON with request metadata
- Includes: Request ID, record ID, timestamps, patient/facility info

### Log Files
- SmartRequest operations are logged to console
- PDF generation logs include request tracking info
- API errors are logged with full context

## Security Considerations

### Credentials Management
- Environment variables used for sensitive data
- No credentials stored in code or logs
- Separate sandbox/production environments

### Data Handling
- Patient data handled according to HIPAA requirements
- Authorization forms base64 encoded for transmission
- No sensitive data in tracking files

### Network Security
- HTTPS required for all API endpoints
- Bearer token authentication
- Request timeouts prevent hanging connections

## Troubleshooting

### Common Issues

1. **Authentication Failures**
   - Check client ID/secret in .env file
   - Verify correct environment (sandbox vs production)
   - Ensure credentials match environment

2. **Network Timeouts**
   - Check internet connectivity
   - Verify firewall settings
   - Check SmartRequest service status

3. **Request Creation Failures**
   - Validate all required fields are present
   - Check field data formats (dates, phone numbers)
   - Verify facility information is correct

4. **Missing Request IDs**
   - Check API response structure
   - Verify successful authentication
   - Review error logs for API failures

### Debug Mode

Enable debug logging by setting:
```bash
export DEBUG=1
```

### Support

For SmartRequest API issues:
- Check the official documentation at https://requester-api.datavant.com/redoc
- Contact Datavant support with request IDs
- Review request tracker logs for troubleshooting

## Future Enhancements

### Planned Features
1. Callback endpoint implementation for status updates
2. Automated status polling for active requests
3. Download automation for completed requests
4. Enhanced error recovery and retry logic
5. Request cancellation management
6. Bulk request operations

### Integration Opportunities
1. RedCap webhook integration for real-time updates
2. Dashboard for request status monitoring  
3. Automated authorization form processing
4. Integration with document management systems