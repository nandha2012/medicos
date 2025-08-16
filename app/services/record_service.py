import time
import os
import sys
import csv
from typing import List, Optional, Dict, Any
from dataclasses import replace 
from datetime import datetime

# Add current directory to path for relative imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from models.datavant_request import DatavantRequest, Facility, RequesterInfo, Patient, Reason, RequestCriteria, CallbackDetails, CallbackHeaders
from services.external_api_service import get_log_detail_data_from_api, submit_datavant_request
from utils.filters import filter_records
from models.redcap_response_second import RedcapResponseSecond
from services.template_service import TemplateService
from services.pdf_service import PDFService
from models.redcap_response_first import RedcapResponseFirst
from utils.counter import Counter
from utils.logger import PandasCSVLogger
from utils.request_tracker import track_smartrequest
from utils.dashboard_tracker import (
    track_processing_start, track_pdf_success, track_pdf_error,
    track_smartrequest_sent, track_smartrequest_success, track_smartrequest_error
)
from utils.dates import get_datavant_date_range

pdf_logger = PandasCSVLogger(f"logs/pdfs/logs_{datetime.now().strftime('%Y%m%d')}.csv", ["record", "timestamp", "username", "request_type","process_type", "status", "details"])
extended_record_logger = PandasCSVLogger(f"logs/extended_records/logs_{datetime.now().strftime('%Y%m%d')}.csv", ["record", "timestamp", "username", "request_type","process_type", "status", "details"])
logger = PandasCSVLogger(f"logs/logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", ["record", "timestamp", "username", "status", "details"])

PATIENT_AUTH_ENCODED = "PATIENT_AUTH_ENCODED"
REPRESENTATION_LETTER_ENCODED = "REPRESENTATION_LETTER_ENCODED"

# Facility data cache
_facility_cache = None

def load_datavant_facilities() -> List[Dict[str, Any]]:
    """
    Load facility data from Datavant facility CSV file
    
    Returns:
        List of facility dictionaries with standardized field names
    """
    global _facility_cache
    
    if _facility_cache is not None:
        return _facility_cache
    
    facilities = []
    csv_path = os.path.join(os.getcwd(), "Datavant_ Facility_List.csv")
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Standardize the facility data to match Datavant API format
                facility = {
                    'site': row.get('SITE', '').strip(),
                    'healthSystem': row.get('Health System ', '').strip(),  # Note the space after "System"
                    'siteName': row.get('SiteName', '').strip(),
                    'addressLine1': row.get('Address', '').strip(),
                    'addressLine2': row.get('Address2', '').strip() or None,
                    'city': row.get('City', '').strip(),
                    'state': row.get('State', '').strip(),
                    'zip': row.get('ZIP', '').strip(),
                    'phone': row.get('PHONE', '').strip(),
                    'fax': row.get('Fax', '').strip(),
                    # Additional fields for reference
                    'itemizedBills': row.get('ITEMIZED BILLS', '').strip(),
                    'records': row.get('RECORDS', '').strip(),
                    'radiology': row.get('RADIOLOGY', '').strip(),
                    'subpoena': row.get('SUBPOENA', '').strip()
                }
                facilities.append(facility)
        
        _facility_cache = facilities
        print(f"✅ Loaded {len(facilities)} facilities from Datavant CSV")
        return facilities
        
    except Exception as e:
        print(f"❌ Error loading Datavant facilities CSV: {e}")
        return []

def get_facility_by_site(site_number: str) -> Optional[Dict[str, Any]]:
    """
    Get facility data by site number
    
    Args:
        site_number: Site number to lookup (e.g., "00101")
        
    Returns:
        Facility dictionary or None if not found
    """
    facilities = load_datavant_facilities()
    
    for facility in facilities:
        if facility['site'] == site_number.strip():
            return facility
    
    print(f"⚠️ Facility with site number '{site_number}' not found in CSV")
    return None

def get_first_facility() -> Optional[Dict[str, Any]]:
    """
    Get the first facility from the CSV (for default use)
    
    Returns:
        First facility dictionary or None if CSV is empty
    """
    facilities = load_datavant_facilities()
    
    if facilities:
        first_facility = facilities[0]
        print(f"🔍 Using first facility: {first_facility['siteName']} (Site: {first_facility['site']})")
        return first_facility
    
    print("❌ No facilities found in CSV")
    return None

def _get_facility_for_datavant_request(data: RedcapResponseFirst) -> Facility:
    """
    Get facility data for Datavant request, prioritizing CSV lookup over form data
    
    Args:
        data: RedcapResponseFirst object containing form data
        
    Returns:
        Facility object with appropriate data
    """
    # TODO: In future, match facility number from redcap detail response with CSV SITE
    # Example usage when facility matching is implemented:
    # facility_number = getattr(data, 'facility_number', None) or getattr(data, 'site_id', None)
    # if facility_number:
    #     csv_facility = get_facility_by_site(str(facility_number).zfill(5))  # Pad to 5 digits like 00101
    #     if csv_facility:
    #         return create_facility_from_csv_data(csv_facility)
    
    # For now, use the first facility from CSV as requested
    
    csv_facility = get_first_facility()
    
    if csv_facility:
        print(f"🔍 Using CSV facility: {csv_facility['siteName']} (Site: {csv_facility['site']})")
        return Facility(
            addressLine1=csv_facility['addressLine1'],
            addressLine2=csv_facility['addressLine2'],
            city=csv_facility['city'],
            state=csv_facility['state'],
            zip=csv_facility['zip'],
            healthSystem=csv_facility['healthSystem'],
            siteName=csv_facility['siteName'],
            phone=csv_facility['phone'],
            fax=csv_facility['fax']
        )
    else:
        # Fallback to form data if CSV loading fails
        print("⚠️ CSV facility not available, falling back to form data")
        return Facility(
            addressLine1=getattr(data, 'mr_address_line_1', ''),
            addressLine2=getattr(data, 'mr_address_line_2', None),
            city=getattr(data, 'mr_city', ''),
            state=getattr(data, 'mr_state', ''),
            zip=getattr(data, 'mr_zip', ''),
            healthSystem=getattr(data, 'mr_health_system', ''),
            siteName=getattr(data, 'mr_site_name', ''),     
            phone=getattr(data, 'mr_phone', ''),
            fax=getattr(data, 'mr_fax', '')
        )

def process_first_request(data:RedcapResponseFirst,counter:Counter):
    print(f"Processing first request for {data.record}")
    try:
        data_to_process = get_log_detail_data_from_api(data)
        if len(data_to_process) == 0:
            print(f"❌ No data to process for {data.record}")
            return
        
        
        for j, item in enumerate(data_to_process):
            print(f"📄 Processing {j+1} of {item.mg_idpreg}")
            item.mr_rec_needs___1 = "1"
            item.mr_rec_needs___2 = "1"
            item.mr_rec_needs___3 = "1"
            item.mr_rec_needs___4 = "1"
            item.mr_rec_needs___6 = "1"
            item.mr_rec_needs___7 = "1"
            item.mr_rec_needs___8 = "1"
            item.mr_rec_needs___9 = "1"
            item.mr_rec_needs___10 = "1"
            item.mr_rec_needs___11 = "1"
            item.mr_rec_needs___12 = "1"
            item.mr_rec_needs___13 = "1"
            item.mr_rec_needs___14 = "1"
            item.mr_rec_needs___15 = "1"
            item.mr_rec_needs_inf___1 = "1"
            item.mr_rec_needs_inf___2 = "1"
            item.mr_rec_needs_inf___3 = "1"
            item.mr_rec_needs_inf___4 = "1"
            item.mr_rec_needs_inf___5 = "1"
            item.mr_rec_needs_inf___6 = "1"
            item.mr_rec_needs_inf___7 = "1"
            item.mr_rec_needs_inf___8 = "1"
            item.mr_rec_needs_inf___9 = "1"
            item.mr_rec_needs_inf___10 = "1"
            item.mr_rec_needs_inf___11 = "1"
            item.mr_rec_needs_inf___12 = "1"
            item.mr_rec_needs_inf___13 = "1"
            item = replace(item)
            handle_pdf_generation(item,"first_request",data,j)
            if(item.mr_dv == "1"):
                request_for = getattr(data, 'mr_req_for', None)
                handle_datavant_request(item, j, "first_request", request_for)
            else:
                print(f"🔄 skipping datavant request for {item.mg_idpreg}_{j}")
            counter.inc()
    except Exception as e:
        logger.log({
            "record": data.record,
            "timestamp": data.timestamp,
            "username": data.username,
            "status": "error",
            "details": f"Error processing {data.record}: {e}"
        })
        print(f"❌ Error processing {data.record}: {e}")
        return

def process_complete_second_request(data:RedcapResponseFirst,counter:Counter):
    print(f"Processing complete second request for {data.record}")
    try:
        data_to_process = get_log_detail_data_from_api(data)
        if len(data_to_process) == 0:
            print(f"❌ No data to process for {data.record}")
            return

        
        for j, item in enumerate(data_to_process):
            print(f"📄 Processing {j+1} of {item.mg_idpreg}")
            item.mr_rec_needs___1 = "0"
            item.mr_rec_needs___2 = "0"
            item.mr_rec_needs___3 = "0"
            item.mr_rec_needs___4 = "0"
            item.mr_rec_needs___6 = "1"
            item.mr_rec_needs___7 = "1"
            item.mr_rec_needs___8 = "1"
            item.mr_rec_needs___9 = "1"
            item.mr_rec_needs___10 = "1"
            item.mr_rec_needs___11 = "1"
            item.mr_rec_needs___12 = "1"
            item.mr_rec_needs___13 = "1"
            item.mr_rec_needs___14 = "1"
            item.mr_rec_needs___15 = "1"
            item.mr_rec_needs_inf___1 = "1"
            item.mr_rec_needs_inf___2 = "1"
            item.mr_rec_needs_inf___3 = "1"
            item.mr_rec_needs_inf___4 = "1"
            item.mr_rec_needs_inf___5 = "1"
            item.mr_rec_needs_inf___6 = "1"
            item.mr_rec_needs_inf___7 = "1"
            item.mr_rec_needs_inf___8 = "1"
            item.mr_rec_needs_inf___9 = "1"
            item.mr_rec_needs_inf___10 = "1"
            item.mr_rec_needs_inf___11 = "1"
            item.mr_rec_needs_inf___12 = "1"
            item.mr_rec_needs_inf___13 = "1"
            item = replace(item)
            handle_pdf_generation(item,"second_request",data,j)
            counter.inc()
            request_for = getattr(data, 'mr_req_for', None)
            handle_datavant_request(item, j, "second_request_complete", request_for)
    except Exception as e:
        print(f"❌ Error processing {data.record}: {e}")
        return


def process_partial_second_request(data:RedcapResponseFirst,counter:Counter):
    print(f"Processing partial second request for {data.record}")
    data_to_process = get_log_detail_data_from_api(data)
    if len(data_to_process) == 0:
        print(f"❌ No data to process for {data.record}")
        return

    
    for j, item in enumerate(data_to_process):
        print(f"📄 Processing {j+1} of {item.mg_idpreg}")
        handle_pdf_generation(item,"second_request",data,j)
        counter.inc()
        request_for = getattr(data, 'mr_req_for', None)
        handle_datavant_request(item, j, "second_request_partial", request_for)



def handle_pdf_generation(data,request_type,first_data,j):
    try:
        request_for = data.mr_req_for
        mg_idpreg = data.mg_idpreg
        print(f"📄 Generating PDF for {mg_idpreg}_{j}")
        
        # Start dashboard tracking
        patient_name = f"{getattr(data, 'bc_momnamefirst', '')} {getattr(data, 'bc_momnamelast', '')}".strip()
        facility_name = getattr(data, 'hos_name', '')
        username = getattr(first_data, 'username', '')
        
        track_processing_start(
            f"{mg_idpreg}_{j}", 
            request_type, 
            patient_name if patient_name else None,
            facility_name if facility_name else None,
            username if username else None
        )
        
        template_path = get_template_path(request_for)
        template_service = TemplateService(template_path)
        docx_path = template_service.fill_template(request_type,data.to_dict(),j)  
        print(f"📄 Docx path test: {docx_path}")
        pdf_service = PDFService()
        pdf_path = pdf_service.convert_to_pdf(docx_path,request_type, f"{mg_idpreg}_{j}")      
        print(f"✅ PDF generated for {mg_idpreg}_{j}")
        
        # Track PDF success
        template_name = request_for_to_template_name(request_for)
        track_pdf_success(f"{mg_idpreg}_{j}", pdf_path or "", template_name)
        if data.mr_request_days and data.mr_request_days.isdigit() and int(data.mr_request_days) > 50:
            extended_record_logger.log({
            "record": mg_idpreg,
            "timestamp": first_data.timestamp,
            "username": first_data.username,
            "request_type": request_for_to_template_name(request_for),
            "process_type": request_type,
            "status": "generated",
            "details": ", ".join(f"{key} = {value}" for key, value in first_data.details.items())
            })
        pdf_logger.log({
            "record": mg_idpreg,
            "timestamp": first_data.timestamp,
            "username": first_data.username,
            "request_type": request_for_to_template_name(request_for),
            "process_type": request_type,
            "status": "generated",
            "details": ", ".join(f"{key} = {value}" for key, value in first_data.details.items())
        })
        time.sleep(2)
    except Exception as e:
        # Track PDF error
        track_pdf_error(f"{mg_idpreg}_{j}", str(e))
        
        logger.log({
            "record": mg_idpreg,
            "timestamp": first_data.timestamp,
            "username": first_data.username,
            "status": "error",
            "details": f"Error generating PDF for {mg_idpreg}_{j}: {e}"
        })
        print(f"❌ Error generating PDF for {mg_idpreg}_{j}: {e}")
        return


def get_template_path(request_for):
    if request_for == "1":
        print("🔍 Using Mother template")
        return os.path.join(os.getcwd(), "assets/templates/mother_template.docx")
    elif request_for == "2":
        print("🔍 Using Infant template")
        return os.path.join(os.getcwd(), "assets/templates/infant_template.docx")
    else:
        print("🔍 Using Combined template")
        return os.path.join(os.getcwd(), "assets/templates/combined_template.docx")

def request_for_to_template_name(request_for):
    if request_for == "1":
        return "mother"
    elif request_for == "2":
        return "infant"
    else:
        return "combined"

def get_record_types_for_request(request_for) -> List[str]:
    """
    Get appropriate Datavant record types based on request type
    
    Args:
        request_for: Request type ("1" for mother, "2" for infant, other for combined)
        
    Returns:
        List of record type names appropriate for the request type
    """
    from .smartrequest_service import SmartRequestService
    
    service = SmartRequestService()
    
    if request_for == "1":
        print("🔍 Using Mom record types for Datavant request")
        return service.get_mom_record_types()
    elif request_for == "2":
        print("🔍 Using Infant record types for Datavant request")
        return service.get_infant_record_types()
    else:
        print("🔍 Using Combined record types for Datavant request")
        # For combined requests, use all available record types
        mom_types = service.get_mom_record_types()
        infant_types = service.get_infant_record_types()
        # Combine and deduplicate
        combined_types = list(set(mom_types + infant_types))
        return sorted(combined_types)

def _get_record_types_for_datavant_request(data: RedcapResponseFirst, request_for: str = None) -> List[str]:
    """
    Get record types for Datavant request, prioritizing request_for logic over manual selection
    
    Args:
        data: RedcapResponseFirst object containing form data
        request_for: Request type ("1" for mother, "2" for infant, other for combined)
        
    Returns:
        List of appropriate record type names
    """
    # If request_for is provided, use it to determine record types
    if request_for is not None:
        return get_record_types_for_request(request_for)
    
    # Fallback to manual record types if specified in the data
    manual_types = getattr(data, 'mr_record_types', None)
    if manual_types:
        if isinstance(manual_types, list):
            return manual_types
        else:
            return [manual_types]
    
    # Final fallback: use combined record types (safest option)
    print("⚠️ No request_for or manual record types specified, using combined record types")
    return get_record_types_for_request("combined")

def get_datavant_request_data(data: RedcapResponseFirst, request_for: str = None) -> DatavantRequest:
    """
    Convert RedCap response data to SmartRequest format
    
    Args:
        data: RedcapResponseFirst object containing form data
        request_for: Request type ("1" for mother, "2" for infant, other for combined)
        
    Returns:
        DatavantRequest: Properly formatted request object
    """
    try:
        # Get date range for the request
        date_range = get_datavant_date_range()
        print(f"🗓️ Using Datavant date range: {date_range[0]} to {date_range[1]}")
        
        # Log patient data being used
        patient_name = f"{getattr(data, 'bc_momnamefirst', '')} {getattr(data, 'bc_momnamelast', '')}".strip()
        print(f"👤 Using patient data: {patient_name} (DOB: {getattr(data, 'bc_mom_dob', 'N/A')})")
        
        return DatavantRequest(
            facility=_get_facility_for_datavant_request(data),
            requesterInfo=RequesterInfo(
                companyId="1792190",
                companyName="TN DEPT OF HEALTH",
                name="Bhanu Gaddam",
                email="bhanu.prathap.gaddam@tn.gov",
            ),
            patient=Patient(
                firstName=getattr(data, 'bc_momnamefirst', ''),
                lastName=getattr(data, 'bc_momnamelast', ''),
                dateOfBirth=getattr(data, 'bc_mom_dob', ''),
                ssn=getattr(data, 'bc_momssn', ''),
                customId=getattr(data, 'mr_custom_id', data.mg_idpreg)
            ),
            reason=Reason(
                businessType=getattr(data, 'mr_business_type', 'ATTY'),
                apiCode=getattr(data, 'mr_api_code', 'STATE_ATTY_OFFICE')
            ),
            requestCriteria=[RequestCriteria(
                recordTypes=_get_record_types_for_datavant_request(data, request_for),
                startDate="2025-08-14",
                endDate="2025-08-15"
            )],
            certificationRequired=getattr(data, 'mr_certification_required', False),
            authorizationForms=[
                PATIENT_AUTH_ENCODED,
                REPRESENTATION_LETTER_ENCODED
            ],
            callbackDetails=_create_callback_details(data)
        )
    except Exception as e:
        print(f"❌ Error creating SmartRequest data: {e}")
        raise


def _create_callback_details(data: RedcapResponseFirst) -> Optional[CallbackDetails]:
    """Create callback details if URL is provided"""
    callback_url = getattr(data, 'mr_callback_url', '')
    if not callback_url:
        return None
        
    return CallbackDetails(
        method=getattr(data, 'mr_callback_method', 'POST'),
        url=callback_url,
        headers=CallbackHeaders(
            Authorization=getattr(data, 'mr_callback_authorization', '')
        ) if getattr(data, 'mr_callback_authorization', '') else None
    )

def handle_datavant_request(item, j: int, document_type: str, request_for: str = None):
    """
    Handle datavant request submission with error tracking
    
    Args:
        item: Data item to process
        j: Item index
        document_type: Type of document request (first_request, second_request_complete, etc.)
        request_for: Request type ("1" for mother, "2" for infant, other for combined)
    """
    try:
        datavant_request_data = get_datavant_request_data(item, request_for)
        print(f"🔄 Datavant request data: {datavant_request_data}")
        api_response = submit_datavant_request(datavant_request_data)
        print(f"🔄 SmartRequest API response: {api_response}")
        
        # Track SmartRequest in dashboard
        if api_response and api_response.get('requestId'):
            request_id = api_response['requestId']
            patient_name = f"{getattr(item, 'mr_first_name', '')} {getattr(item, 'mr_last_name', '')}".strip()
            facility_name = getattr(item, 'mr_site_name', '')
            
            # Dashboard tracking - Success case
            track_smartrequest_sent(f"{item.mg_idpreg}_{j}", request_id, datavant_request_data.model_dump() if hasattr(datavant_request_data, 'model_dump') else None)
            track_smartrequest_success(f"{item.mg_idpreg}_{j}", request_id)
            print(f"✅ SmartRequest tracked as successful for {item.mg_idpreg}_{j}")
            
            # Original tracking (for backward compatibility)
            track_smartrequest(
                request_id=request_id,
                record_id=item.mg_idpreg,
                document_type=document_type,
                patient_name=patient_name if patient_name else None,
                facility_name=facility_name if facility_name else None
            )
        else:
            # Dashboard tracking - Failure case
            error_msg = "SmartRequest API call failed or returned no requestId"
            if api_response:
                error_msg += f": {api_response}"
            track_smartrequest_error(f"{item.mg_idpreg}_{j}", error_msg)
            print(f"❌ SmartRequest failed for {item.mg_idpreg}_{j}: {error_msg}")
    except Exception as e:
        # Track unexpected SmartRequest errors
        error_msg = f"Unexpected error during SmartRequest: {str(e)}"
        track_smartrequest_error(f"{item.mg_idpreg}_{j}", error_msg)
        print(f"❌ SmartRequest exception for {item.mg_idpreg}_{j}: {error_msg}")