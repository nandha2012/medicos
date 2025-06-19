import os
import requests
from dataclasses import replace 
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
        print(f"❌ Error getting detailed data from API: {e}")
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
    'fields[6]': 'ifu_fac_num',
    'fields[7]': 'ifu_fac_phone',
    'fields[8]': 'inf_dob_mom_tr',
    'fields[9]': 'mr_rec_needs',
    'fields[10]': 'mr_rec_needs_inf',
    'fields[11]': 'mr_request',
    'fields[12]': 'mr_request_dt',
    'fields[13]':'mr_received',
    'fields[14]': 'mr_request_2',
    'fields[15]': 'mr_request_dt_2',
    'fields[16]':'mr_received_2',
    'fields[17]': 'mr_rec_needs_2',
    'fields[18]': 'mr_rec_needs_inf_2', 
    'fields[19]': 'mr_rec_all',
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
        print(f"❌ Error getting detailed data from API: {e}")
        return None

def generate_pdf(data):
    details = get_log_detail_data_from_api(data)
    if details is not None:
        details_data_class =[ RedcapResponseSecond(**item) for item in details]
        for record in details_data_class:    
            handle_pdf_generation(record)
    else:
        print("No data received from API")
    exit()   


# TODO: This is a temporary function to handle the PDF generation logic.
# TODO: This should be removed once the logic is implemented in the RedcapResponseSecond class.
def handle_pdf_generation(data:RedcapResponseSecond):
    print(data)
    mr_request = data.mr_request == "1"
    mr_request_dt = data.mr_request_dt
    mr_request_2 = data.mr_request_2
    mr_request_dt_2 = data.mr_request_dt_2
    mr_received = data.mr_received
    mr_rec_all = data.mr_rec_all
    mr_rec_all_2 = data.mr_rec_all_2

    base_output = os.path.join(os.getcwd(), "output")
    os.makedirs(base_output, exist_ok=True)

    if mr_request and mr_request_dt and not mr_request_dt_2:
            print("First request received with fields missing. action needed.")
            folder = os.path.join(base_output, "firstrequest")
            os.makedirs(folder, exist_ok=True)
            print("First request received with fields missing. action needed.")
            data.mr_rec_needs___1 = 1
            data.mr_rec_needs___2 = 1
            data.mr_rec_needs___3 = 1
            data.mr_rec_needs___4 = 1
            data.mr_rec_needs___5 = 1
            data.mr_rec_needs___6 = 1
            data.mr_rec_needs___7 = 1
            data.mr_rec_needs___8 = 1
            data.mr_rec_needs___9 = 1
            data.mr_rec_needs___10 = 1
            data.mr_rec_needs___11 = 1
            data.mr_rec_needs___12 = 1
            data.mr_rec_needs___13 = 1
            data = replace(data)
            template_service = TemplateService(template_path)
            template_service.fill_template("firstrequest",data.to_dict())
    elif mr_request and mr_request_dt and mr_request_2 and mr_request_dt_2:
        folder = os.path.join(base_output, "secondrequest")
        os.makedirs(folder, exist_ok=True)
        if mr_received in ("0", ""):
            # Second request logic
            print("Second request send no response. action needed.")
            data.mr_rec_needs___1 = 1
            data.mr_rec_needs___2 = 1
            data.mr_rec_needs___3 = 1
            data.mr_rec_needs___4 = 1
            data.mr_rec_needs___5 = 1
            data.mr_rec_needs___6 = 1
            data.mr_rec_needs___7 = 1
            data.mr_rec_needs___8 = 1
            data.mr_rec_needs___9 = 1
            data.mr_rec_needs___10 = 1
            data.mr_rec_needs___11 = 1
            data.mr_rec_needs___12 = 1
            data.mr_rec_needs___13 = 1
            data = replace(data)
            template_service = TemplateService(template_path)
            template_service.fill_template("secondrequest",data.to_dict())
        elif mr_received == "1":
            if mr_rec_all == '0':
                print("Second Request received with partial. action needed.")
                template_service = TemplateService(template_path)
                template_service.fill_template("secondrequest",data.to_dict())
            elif mr_rec_all == '1':
                print("Second request already received. No action needed.")
            else:
                 print("Invalid or missing value for 'mr_rec_all'.")
        else:
            print("Invalid or missing value for 'mr_received_2'.")
    else:
        print("Conditions not met for any request.")



if __name__ == "__main__":
    print("🚀 Starting invoice PDF generation...")
    # Setup
    template_path = os.path.join(os.getcwd(), "assets/templates/infant_template.docx")
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    result = get_log_data_from_api()
    if result is not None:
        print(f"🔎 {len(result)} records found.")
        data_list = [RedcapResponseFirst(**item) for item in result]
        for data in data_list:
            generate_pdf(data)
    else:
        print("⚠️ No records received from API.")
    exit()

        # Data input
