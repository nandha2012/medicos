#!/usr/bin/env python
import requests
from dotenv import load_dotenv
import os
from models.redcap_response_first import RedcapResponseFirst
from models.redcap_response_second import RedcapResponseSecond
from utils.filters import filter_records, get_latest_records
from utils.dates import get_current_time_str, get_one_hour_before_str
from fake_responses import generate_fake_detail_record
from typing import List


load_dotenv()
end_point = os.getenv("EXTERNAL_API_END_POINT") or "https://localhost/redcap/api/"
token = os.getenv("EXTERNAL_API_TOKEN") or "E*************7"

details_data = {
    'token': '',
    'content': 'record',
    'action': 'export',
    'format': 'json',
    'type': 'flat',
    'csvDelimiter': '',
    'fields[0]': 'mg_idpreg',
    'fields[1]': 'bc_momnamefirst',
    'fields[2]': 'bc_momnamelast',
    'fields[3]': 'bc_momssn',
    'fields[4]': 'hos_name_cat_2',
    'fields[5]': 'mr_request_dt',
    'fields[6]': 'ifu_fac_num',
    'fields[7]': 'ifu_fac_phone',
    'fields[8]': 'inf_dob_mom_tr',
    'fields[9]': 'hos_name',
    'fields[10]': 'mr_rec_needs',
    'fields[11]': 'mr_rec_needs_inf',
    'fields[12]': 'hospital_fax_num',
    'fields[13]': 'hospital_phone_num',
    'fields[14]': 'dob_inf',
    'fields[15]': 'bc_mom_dob',
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
        'beginTime': '2025-06-21 08:34',
        'endTime': get_current_time_str(),
        'format': 'json',
        'returnFormat': 'json'
    }
    try:
        response = requests.post(f'{end_point}',data=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error getting log data from API: {e}")
        return []

def get_log_detail_data_from_api(record:RedcapResponseFirst):
        data = get_record_data_from_api(record)
        data = filter_records(data, RedcapResponseSecond)
        # data = generate_fake_detail_record(record.record,1)
        if data is None:
            print(f"❌ no record data found for {record.record}")
            return []
        return data


def get_record_data_from_api(record:RedcapResponseFirst):
    data = details_data.copy()
    data[f'records[{0}]'] = record.record
    try:
        response = requests.post(end_point,data=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error getting log detail data from API: {e}")
        return []
    