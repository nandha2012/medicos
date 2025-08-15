import time
import os
import sys
from typing import List, Optional
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

pdf_logger = PandasCSVLogger(f"logs/pdfs/logs_{datetime.now().strftime('%Y%m%d')}.csv", ["record", "timestamp", "username", "request_type","process_type", "status", "details"])
extended_record_logger = PandasCSVLogger(f"logs/extended_records/logs_{datetime.now().strftime('%Y%m%d')}.csv", ["record", "timestamp", "username", "request_type","process_type", "status", "details"])
logger = PandasCSVLogger(f"logs/logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", ["record", "timestamp", "username", "status", "details"])

PATIENT_AUTH_ENCODED = "PATIENT_AUTH_ENCODED"
REPRESENTATION_LETTER_ENCODED = "REPRESENTATION_LETTER_ENCODED"

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
                handle_datavant_request(item, j, "first_request")
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
            handle_datavant_request(item, j, "second_request_complete")
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
        handle_datavant_request(item, j, "second_request_partial")



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

def get_datavant_request_data(data: RedcapResponseFirst) -> DatavantRequest:
    """
    Convert RedCap response data to SmartRequest format
    
    Args:
        data: RedcapResponseFirst object containing form data
        
    Returns:
        DatavantRequest: Properly formatted request object
    """
    try:
        return DatavantRequest(
            facility=Facility(
                addressLine1=getattr(data, 'mr_address_line_1', ''),
                addressLine2=getattr(data, 'mr_address_line_2', None),
                city=getattr(data, 'mr_city', ''),
                state=getattr(data, 'mr_state', ''),
                zip=getattr(data, 'mr_zip', ''),
                healthSystem=getattr(data, 'mr_health_system', ''),
                siteName=getattr(data, 'mr_site_name', ''),     
                phone=getattr(data, 'mr_phone', ''),
                fax=getattr(data, 'mr_fax', '')
            ),
            requesterInfo=RequesterInfo(
                companyId="1792190",
                companyName="TN DEPT OF HEALTH",
                name="Bhanu Gaddam",
                email="bhanu.prathap.gaddam@tn.gov"
            ),
            patient=Patient(
                firstName=getattr(data, 'mr_first_name', ''),
                lastName=getattr(data, 'mr_last_name', ''),
                dateOfBirth=getattr(data, 'mr_date_of_birth', ''),
                ssn=getattr(data, 'mr_ssn', ''),
                customId=getattr(data, 'mr_custom_id', data.mg_idpreg)
            ),
            reason=Reason(
                businessType=getattr(data, 'mr_business_type', 'ATTY'),
                apiCode=getattr(data, 'mr_api_code', 'STATE_ATTY_OFFICE')
            ),
            requestCriteria=[RequestCriteria(
                recordTypes=getattr(data, 'mr_record_types', ['Abstract']) if isinstance(getattr(data, 'mr_record_types', []), list) 
                           else [getattr(data, 'mr_record_types', 'Abstract')],
                startDate=getattr(data, 'mr_start_date', ''),
                endDate=getattr(data, 'mr_end_date', '')
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

def handle_datavant_request(item, j: int, document_type: str):
    """
    Handle datavant request submission with error tracking
    
    Args:
        item: Data item to process
        j: Item index
        document_type: Type of document request (first_request, second_request_complete, etc.)
    """
    try:
        datavant_request_data = get_datavant_request_data(item)
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