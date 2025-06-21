#!/usr/bin/env python
import requests
data = {
    'token': 'E2CAE892A6D129154430EF07AE11EFE7',
    'content': 'record',
    'action': 'export',
    'format': 'json',
    'type': 'flat',
    'csvDelimiter': '',
    'records[0]': 'TNSC023022842',
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
    'rawOrLabel': 'raw',
    'rawOrLabelHeaders': 'raw',
    'exportCheckboxLabel': 'false',
    'exportSurveyFields': 'false',
    'exportDataAccessGroups': 'false',
    'returnFormat': 'json'
}
r = requests.post('https://fdfs.health.tn.gcom/sample',data=data)
print('HTTP Status: ' + str(r.status_code))
print(r.json())
