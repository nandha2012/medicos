#!/usr/bin/env python
import requests
from dotenv import load_dotenv
import os
from models.redcap_response_first import RedcapResponseFirst
from models.redcap_response_second import RedcapResponseSecond
from models.datavant_request import DatavantRequest
from utils.filters import filter_records, get_latest_records, merge_records
from utils.dates import get_current_time_str, get_one_hour_before_str, get_start_of_today_str, subtract_time_from_str
from fake_responses import generate_fake_detail_record
from services.smartrequest_service import SmartRequestService
from typing import List, Literal, Optional

import json
import sys

def parse_arg(flag_name: str, default_value: str):
    for arg in sys.argv:
        if arg.startswith(f"--{flag_name}="):
            return arg.split("=", 1)[1]
    return default_value

time_delta = parse_arg("time_delta", "1")
time_delta_period = parse_arg("time_delta_period", "hours")
load_dotenv()
end_point = os.getenv("EXTERNAL_API_END_POINT") or "https://localhost/redcap/api/"
token = os.getenv("EXTERNAL_API_TOKEN") or "E*************7"
env = os.getenv("ENV") or 'local'

# Initialize SmartRequest service
smartrequest_service = SmartRequestService()

details_data = {
    'token': token,
    'content': 'record',
    'action': 'export',
    'format': 'json',
    'type': 'flat',
    'csvDelimiter': '',
    'fields[0]': 'mg_idpreg',
    'fields[1]': 'hos_name',
    'fields[2]': 'hospital_phone_num',
    'fields[3]': 'hospital_fax_num',
    'fields[4]': 'bc_momnamefirst',
    'fields[5]': 'bc_momnamelast',
    'fields[6]': 'bc_mom_dob',
    'fields[7]': 'bc_momssn',
    'fields[8]': 'dob_inf',
    'fields[9]': 'mr_request_dt',
    'fields[10]': 'bc_childnamefirst',
    'fields[11]': 'bc_childnamelast',
    'fields[12]': 'bc_childssn',
    'fields[13]': 'bc_momnamemaidenlast',
    'fields[14]': 'mr_req_for',
    'fields[15]': 'mr_request_days',
    'fields[16]': 'inf_dob_mom_tr',
    'fields[17]': 'mr_rec_needs',
    'fields[18]': 'mr_rec_needs_inf',
    'fields[19]': 'mr_needs_oth',
    'fields[20]': 'mr_needs_oth_inf',
    'fields[21]': 'mr_dv',
    'rawOrLabel': 'raw',
    'rawOrLabelHeaders': 'raw',
    'exportCheckboxLabel': 'false',
    'exportSurveyFields': 'false',
    'exportDataAccessGroups': 'false',
    'returnFormat': 'json'
}

def get_log_data_from_api():
    data = {
        'token': token,
        'content': 'log',
        'logtype': 'record',
        'user': '',
        'record': '',
        'beginTime': subtract_time_from_str(get_current_time_str(), int(time_delta), time_delta_period),
        'endTime': get_current_time_str(),
        'format': 'json',
        'returnFormat': 'json'
    }
    print(f'🔍 Begin Time: {data}')
    try:
        if env == 'local':
            print(f'logs fetching from local...')
            # Try different possible paths for the sample file
            sample_paths = [
                'app/response_1_sample.json',  # When run from project root
                'response_1_sample.json',      # When run from app directory
                '../app/response_1_sample.json'  # When run from subdirectory
            ]
            
            for path in sample_paths:
                if os.path.exists(path):
                    return json.load(open(path))
            
            print(f"⚠️ Sample data file not found in any of: {sample_paths}")
            return []
        print(f"Hitting logs api....")
        response = requests.post(f'{end_point}',data=data,timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print(f'❌ api timeout...')
        return []
    except Exception as e:
        print(f"❌ Error getting log data from API: {e}")
        return []

def get_log_detail_data_from_api(record:RedcapResponseFirst):
        data = get_record_data_from_api(record)
        data = merge_records(data)
        print(f'details response {data}')
        if len(data) == 0:
            print(f"❌ no record data found for {record.record}")
            return []
        data = filter_records([data], RedcapResponseSecond)
        # data = generate_fake_detail_record(record.record,1)
        if data is None:
            print(f"❌ no record data found for {record.record}")
            return []
        return data


def get_record_data_from_api(record:RedcapResponseFirst):
    data = details_data.copy()
    data[f'records[{0}]'] = record.record
    print(f"data {data}")
    try:
        if env == 'local':
            # Try different possible paths for the sample file
            sample_paths = [
                'app/response_2_sample.json',  # When run from project root
                'response_2_sample.json',      # When run from app directory
                '../app/response_2_sample.json'  # When run from subdirectory
            ]
            
            for path in sample_paths:
                if os.path.exists(path):
                    json_data = json.load(open(path))
                    print(f'details fetching from local...')
                    result = [x for x in json_data if x['mg_idpreg'] == record.record]
                    return result
            
            print(f"⚠️ Sample data file response_2_sample.json not found in any of: {sample_paths}")
            return []
        response = requests.post(end_point,data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print(f'❌ api timeout...')
        return []
    except Exception as e:
        print(f"❌ Error getting log detail data from API: {e}")
        return []


def submit_datavant_request(request_data: DatavantRequest) -> Optional[dict]:
    """
    Submit a medical records request to SmartRequest API
    
    Args:
        request_data: DatavantRequest object containing all required fields
    
    Returns:
        dict: API response or None on error
    """
    try:
        # Convert Pydantic model to dict for API submission
        request_dict = request_data.model_dump(exclude_none=True)
        
        # Submit request using SmartRequest service
        result = smartrequest_service.create_request(request_dict)
        
        if result:
            request_id = result.get("requestId")
            print(f"✅ SmartRequest submitted successfully with ID: {request_id}")
            
            # Log the request ID for tracking
            if request_id:
                print(f"📝 Track this request with ID: {request_id}")
        
        return result
        
    except Exception as e:
        print(f"❌ Unexpected error submitting SmartRequest: {e}")
        return None


def get_smartrequest_status(request_id: str) -> Optional[dict]:
    """
    Get status of a SmartRequest
    
    Args:
        request_id: ID of the request to check
        
    Returns:
        Status dictionary or None on error
    """
    return smartrequest_service.get_request_status(request_id)


def get_smartrequest_download_url(request_id: str, document_type: str = "ALL") -> Optional[str]:
    """
    Get download URL for SmartRequest documents
    
    Args:
        request_id: ID of the request
        document_type: Type of document (REQUEST_LETTER, INVOICE, MEDICAL_RECORD, CORRESPONDENCE, ALL)
        
    Returns:
        Download URL or None on error
    """
    return smartrequest_service.get_download_url(request_id, document_type)


def cancel_smartrequest(request_id: str, reason: str) -> bool:
    """
    Cancel a SmartRequest
    
    Args:
        request_id: ID of the request to cancel
        reason: Reason for cancellation
        
    Returns:
        True if successful, False otherwise
    """
    return smartrequest_service.cancel_request(request_id, reason)
    