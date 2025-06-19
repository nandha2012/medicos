import os
import requests
from models.redcap_response_first import RedcapResponseFirst
from models.redcap_response_second import RedcapResponseSecond
from services.template_service import TemplateService
from services.api_instance import api
from utils import get_current_time_str, get_one_hour_before_str
import os

# template_path = os.path.join(os.getcwd(), "assets/templates/invoice_template.docx")
# print(f"📄 Using template: {template_path}")

def get_log_data_from_api():
    data = {
                'token': 'E2CAE892A6D129154430EF07AE11EFE7',
                'content': 'log',
                'logtype': 'record',
                'user': '',
                'record': '',
                'beginTime':'2025-06-19 01:00',
                'endTime': get_current_time_str(),
                'format': 'json',
                'returnFormat': 'json'
            }
    try:
        response= requests.post('https://redcap.health.tn.gov/redcap/api/',data=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error getting data from API: {e}")
        return None

def get_log_detail_data_from_api(data):
    data = {
    'token': 'E2CAE892A6D129154430EF07AE11EFE7',
    'content': 'record',
    'action': 'export',
    'format': 'json',
    'type': 'flat',
    'csvDelimiter': '',
    'records[0]': data.record,
    'fields[0]': 'mg_idpreg',
    'fields[1]': 'bc_momnamefirst',
    'fields[2]': 'bc_momnamelast',
    'fields[3]': 'bc_momssn',
    'fields[4]': 'hos_name_cat_2',
    'fields[5]': 'mr_request_dt',
    'fields[6]': 'ifu_fac_num',
    'fields[7]': 'ifu_fac_phone',
    'fields[8]': 'inf_dob_mom_tr',
    'fields[9]': 'mr_rec_needs',
    'fields[10]': 'mr_rec_needs_inf',
    'fields[11]': 'mr_request_days',
    'fields[12]': 'mr_received',
    'fields[13]': 'mr_request_2',
    'fields[14]': 'mr_request_dt_2',
    'fields[13]': 'mr_request',
    'rawOrLabel': 'raw',
    'rawOrLabelHeaders': 'raw',
    'exportCheckboxLabel': 'false',
    'exportSurveyFields': 'false',
    'exportDataAccessGroups': 'false',
    'returnFormat': 'json'
}
    try:
        response= requests.post('https://redcap.health.tn.gov/redcap/api/',data=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error getting data from API: {e}")
        return None

def generate_invoice_pdf(data):
    details = get_log_detail_data_from_api(data)
    print(details)
    if details is not None:
        details_data_class =[ RedcapResponseSecond(**item) for item in details]
        for record in details_data_class: 
            print(f'details{record}')  
            #if record.mr_request      
            #template_service = TemplateService(template_path)
            #emplate_service.fill_template(output_dir,data.record, record.to_dict())
    else:
        print("No data received from API")
    exit()  

if __name__ == "__main__":
    print("Generating invoice PDF...")
    # Setup
    template_path = os.path.join(os.getcwd(), "assets/templates/infant_template.docx")
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    result = get_log_data_from_api()
    if result is not None:
        print(f'result {len(result)}')
        data_list = [RedcapResponseFirst(**item) for item in result]
        for data in data_list:
            generate_invoice_pdf(data)
    else:
        print("No data received from API.")
    exit()

        # Data input
