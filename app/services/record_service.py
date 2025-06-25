import time
from services.external_api_service import get_log_detail_data_from_api
from utils.filters import filter_records
from models.redcap_response_second import RedcapResponseSecond
from typing import List
from dataclasses import replace 
from services.template_service import TemplateService
import os
from services.pdf_service import PDFService
from models.redcap_response_first import RedcapResponseFirst
from utils.counter import Counter
from utils.logger import PandasCSVLogger
from datetime import datetime

pdf_logger = PandasCSVLogger(f"logs/pdfs/logs_{datetime.now().strftime('%Y%m%d')}.csv", ["record", "timestamp", "username", "request_type","process_type", "status", "details"])
extended_record_logger = PandasCSVLogger(f"logs/extended_records/logs_{datetime.now().strftime('%Y%m%d')}.csv", ["record", "timestamp", "username", "request_type","process_type", "status", "details"])
logger = PandasCSVLogger(f"logs/logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", ["record", "timestamp", "username", "status", "details"])



def process_first_request(data:RedcapResponseFirst,counter:Counter):
    print(f"Processing first request for {data.record}")
    try:
        data_to_process = get_log_detail_data_from_api(data)
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
            item.mr_rec_needs_inf___88 = "1"
            item = replace(item)
            handle_pdf_generation(item,"first",data,j)
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
            item.mr_rec_needs_inf___88 = "1"
            item = replace(item)
            handle_pdf_generation(item,"second",data,j)
            counter.inc()
    except Exception as e:
        print(f"❌ Error processing {data.record}: {e}")
        return


def process_partial_second_request(data:RedcapResponseFirst,counter:Counter):
    print(f"Processing partial second request for {data.record}")
    data_to_process = get_log_detail_data_from_api(data)
    for j, item in enumerate(data_to_process):
        print(f"📄 Processing {j+1} of {item.mg_idpreg}")
        handle_pdf_generation(item,"second-partial",data,j)
        counter.inc()



def handle_pdf_generation(data,request_type,first_data,j):
    try:
        request_for = data.mr_req_for
        mg_idpreg = data.mg_idpreg
        print(f"data-dict {data}")
        print(f"📄 Generating PDF for {mg_idpreg}_{j}")
        template_path = get_template_path(request_for)
        template_service = TemplateService(template_path)
        docx_path = template_service.fill_template(request_type,data.to_dict(),j)  
        print(f"📄 Docx path test: {docx_path}")
        pdf_service = PDFService()
        pdf_service.convert_to_pdf(docx_path,request_type, f"{mg_idpreg}_{j}")      
        print(f"✅ PDF generated for {mg_idpreg}_{j}")
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