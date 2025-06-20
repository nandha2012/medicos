import os
import requests
from dataclasses import replace 
from models.redcap_response_first import RedcapResponseFirst
from models.redcap_response_second import RedcapResponseSecond
from services.template_service import TemplateService
from services.api_instance import api
from services.external_api_service import get_log_data_from_api, get_log_detail_data_from_api
from utils.dates import get_current_time_str, get_one_hour_before_str
from fake_responses import generate_fake_detail_responses, generate_fake_log_responses
import time

# template_path = os.path.join(os.getcwd(), "assets/templates/invoice_template.docx")
# print(f"📄 Using template: {template_path}")

def generate_pdf(data_list, batch_size=5):
    data_to_process = []
    for i in range(0, len(data_list), batch_size):
        batch = data_list[i:i + batch_size]
        details = get_log_detail_data_from_api(batch,5)
        data_to_process.extend(details)
        print(f'{len(details)} found for batch {i+1} to {i+batch_size}')
        time.sleep(10)
    print(f'{len(data_to_process)} found for total')
    handle_pdf_genration_batch(data_to_process,5,10)



def handle_pdf_genration_batch(data_list, batch_size=5, delay_between_batches=3):
    for i in range(0, len(data_list), batch_size):
        batch = data_list[i:i + batch_size]
        for j, item in enumerate(batch):
            handle_pdf_generation(item,j)

        # Add delay after each batch (except last one)
        if i + batch_size < len(data_list):
            time.sleep(delay_between_batches)

# TODO: This is a temporary function to handle the PDF generation logic.
# TODO: This should be removed once the logic is implemented in the RedcapResponseSecond class.
def handle_pdf_generation(data:RedcapResponseSecond,j):
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
            data.mr_rec_needs___1 = "1"
            data.mr_rec_needs___2 = "1"
            data.mr_rec_needs___3 = "1"
            data.mr_rec_needs___4 = "1"
            data.mr_rec_needs___5 = "1"
            data.mr_rec_needs___6 = "1"
            data.mr_rec_needs___7 = "1"
            data.mr_rec_needs___8 = "1"
            data.mr_rec_needs___9 = "1"
            data.mr_rec_needs___10 = "1"
            data.mr_rec_needs___11 = "1"
            data.mr_rec_needs___12 = "1"
            data.mr_rec_needs___13 = "1"
            data = replace(data)
            # template_service = TemplateService(template_path)
            # template_service.fill_template("firstrequest",data.to_dict(),j)
    elif mr_request and mr_request_dt and mr_request_2 and mr_request_dt_2:
        folder = os.path.join(base_output, "secondrequest")
        os.makedirs(folder, exist_ok=True)
        if mr_received in ("0", ""):
            # Second request logic
            print("Second request send no response. action needed.")
            data.mr_rec_needs___1 = "1"
            data.mr_rec_needs___2 = "1"
            data.mr_rec_needs___3 = "1"
            data.mr_rec_needs___4 = "1"
            data.mr_rec_needs___7 = "1"
            data.mr_rec_needs___8 = "1"
            data.mr_rec_needs___9 = "1"
            data.mr_rec_needs___10 = "1"
            data.mr_rec_needs___11 = "1"
            data.mr_rec_needs___12 = "1"
            data.mr_rec_needs___13 = "1"
            data = replace(data)
            # template_service = TemplateService(template_path)
            # template_service.fill_template("secondrequest",data.to_dict(),j)
        elif mr_received == "1":
            if mr_rec_all == '0':
                print("Second Request received with partial. action needed.")
                # template_service = TemplateService(template_path)
                # template_service.fill_template("secondrequest",data.to_dict(),j)
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
    # result = get_log_data_from_api()
    result = generate_fake_log_responses(1)
    if result is not None:
        print(f"🔎 {len(result)} records found.")
        data_list = [RedcapResponseFirst(**item) for item in result]
        generate_pdf(data_list)
    else:
        print("⚠️ No records received from API.")
    exit()

        # Data input
