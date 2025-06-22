#!/usr/bin/env python
import requests
from dotenv import load_dotenv
import os
from models.redcap_response_first import RedcapResponseFirst
from models.redcap_response_second import RedcapResponseSecond
from utils.filters import filter_records, get_latest_records, merge_records
from utils.dates import get_current_time_str, get_one_hour_before_str
from fake_responses import generate_fake_detail_record
from typing import List
import json

load_dotenv()
end_point = os.getenv("EXTERNAL_API_END_POINT") or "https://localhost/redcap/api/"
token = os.getenv("EXTERNAL_API_TOKEN") or "E*************7"
env = os.getenv("ENV") or 'local'

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
    'fields[14]': 'bc_momnamemaidenlast',
    'fields[15]': 'mr_req_for',
    'fields[16]': 'mr_emr_needs_inf___1',
    'fields[17]': 'mr_emr_needs_inf___2',
    'fields[18]': 'mr_emr_needs_inf___3',
    'fields[19]': 'mr_emr_needs_inf___4',
    'fields[20]': 'mr_emr_needs_inf___5',
    'fields[21]': 'mr_emr_needs_inf___6',
    'fields[22]': 'mr_emr_needs_inf___7',
    'fields[23]': 'mr_emr_needs_inf___8',
    'fields[24]': 'mr_emr_needs_inf___9',
    'fields[25]': 'mr_emr_needs_inf___10',
    'fields[26]': 'mr_emr_needs_inf___11',
    'fields[27]': 'mr_emr_needs_inf___12',
    'fields[28]': 'mr_emr_needs_inf___13',
    'fields[29]': 'mr_emr_needs_inf___88',
    'fields[30]': 'mr_rec_needs___1',
    'fields[31]': 'mr_rec_needs___2',
    'fields[32]': 'mr_rec_needs___3',
    'fields[33]': 'mr_rec_needs___4',
    'fields[34]': 'mr_rec_needs___6',
    'fields[35]': 'mr_rec_needs___7',
    'fields[36]': 'mr_rec_needs___8',
    'fields[37]': 'mr_rec_needs___9',
    'fields[38]': 'mr_rec_needs___10',
    'fields[39]': 'mr_rec_needs___11',
    'fields[40]': 'mr_rec_needs___12',
    'fields[41]': 'mr_rec_needs___13',
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
        if env == 'local':
            return json.load(open('app/response_1_sample.json'))
        response = requests.post(f'{end_point}',data=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error getting log data from API: {e}")
        return []

def get_log_detail_data_from_api(record:RedcapResponseFirst):
        data = get_record_data_from_api(record)
        data = merge_records(data)
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
    try:
        if env == 'local':
            json_data = json.load(open('app/response_2_sample.json'))
            result = [x for x in json_data if x['mg_idpreg'] == record.record]
            print(f"🔍 Result: {result}")
            return result
        response = requests.post(end_point,data=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error getting log detail data from API: {e}")
        return []
    