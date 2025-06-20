import os
import requests
from dataclasses import replace 
from models.redcap_response_first import RedcapResponseFirst
from models.redcap_response_second import RedcapResponseSecond
from services.template_service import TemplateService
from services.api_instance import api
from services.external_api_service import get_log_data_from_api, get_log_detail_data_from_api
from utils import get_current_time_str, get_one_hour_before_str
import os

# template_path = os.path.join(os.getcwd(), "assets/templates/invoice_template.docx")
# print(f"📄 Using template: {template_path}")

def generate_pdf(data):
    print(f'processing for record: {data.record}')
    details = get_log_detail_data_from_api(data.record)
    print(details)
    if details is None:
        print("No data received from API")
        return
    print(f'{len(details)} fround for {data.record}')
    if details is not None:
        details_data_class =[ RedcapResponseSecond(**item) for item in details]
        for record in details_data_class:    
            handle_pdf_generation(record)
    else:
        print("No data received from API") 


# TODO: This is a temporary function to handle the PDF generation logic.
# TODO: This should be removed once the logic is implemented in the RedcapResponseSecond class.
def handle_pdf_generation(data:RedcapResponseSecond):
    mr_request = data.mr_request == "1"
    mr_request_dt = data.mr_request_dt
    mr_request_2 = data.mr_request_2
    mr_request_dt_2 = data.mr_request_dt_2
    mr_received = data.mr_received
    mr_rec_all = data.mr_rec_all
    mr_rec_all_2 = data.mr_rec_all_2

    base_output = os.path.join(os.getcwd(), "output")
    os.makedirs(base_output, exist_ok=True)
    print(f' conditons mr_request:{mr_request} - mr_request_dt:{mr_request_dt} - mr_request_dt_2:{mr_request_dt_2}')
    print(f' condtions mr_request_2:{mr_request_2} - mr_received:{mr_received}')
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
