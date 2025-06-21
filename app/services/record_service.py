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
template_path = os.path.join(os.getcwd(), "assets/templates/infant_template.docx")



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
            item.mr_rec_needs___5 = "1"
            item.mr_rec_needs___6 = "1"
            item.mr_rec_needs___7 = "1"
            item.mr_rec_needs___8 = "1"
            item.mr_rec_needs___9 = "1"
            item.mr_rec_needs___10 = "1"
            item.mr_rec_needs___11 = "1"
            item.mr_rec_needs___12 = "1"
            item.mr_rec_needs___13 = "1"
            item = replace(item)
            handle_pdf_generation(item,"first",j)
            time.sleep(1)
            counter.inc()
    except Exception as e:
        print(f"❌ Error processing {data.record}: {e}")
        return

def process_complete_second_request(data:RedcapResponseFirst,counter:Counter):
    print(f"Processing complete second request for {data.record}")
    try:
        data_to_process = get_log_detail_data_from_api(data)
        for j, item in enumerate(data_to_process):
            print(f"📄 Processing {j+1} of {item.mg_idpreg}")
            item.mr_rec_needs___1 = data.details.get("mr_rec_needs(1)")
            item.mr_rec_needs___2 = data.details.get("mr_rec_needs(2)")
            item.mr_rec_needs___3 = data.details.get("mr_rec_needs(3)")
            item.mr_rec_needs___4 = data.details.get("mr_rec_needs(4)")
            item.mr_rec_needs___7 = data.details.get("mr_rec_needs(7)")
            item.mr_rec_needs___8 = data.details.get("mr_rec_needs(8)")
            item.mr_rec_needs___9 = data.details.get("mr_rec_needs(9)")
            item.mr_rec_needs___10 = data.details.get("mr_rec_needs(10)")
            item.mr_rec_needs___11 = data.details.get("mr_rec_needs(11)")
            item.mr_rec_needs___12 = data.details.get("mr_rec_needs(12)")
            item.mr_rec_needs___13 = data.details.get("mr_rec_needs(13)")
            item = replace(item)
            handle_pdf_generation(item,"second",j)
            counter.inc()
            time.sleep(1)
    except Exception as e:
        print(f"❌ Error processing {data.record}: {e}")
        return


def process_partial_second_request(data:RedcapResponseFirst,counter:Counter):
    print(f"Processing partial second request for {data.record}")
    data_to_process = get_log_detail_data_from_api(data)
    for j, item in enumerate(data_to_process):
        print(f"📄 Processing {j+1} of {item.mg_idpreg}")
        handle_pdf_generation(item,"second-partial",j)
        counter.inc()
        time.sleep(1)


def handle_pdf_generation(data,request_type,j):
    try:
        mg_idpreg = data.mg_idpreg
        print(f"📄 Generating PDF for {mg_idpreg}_{j}")
        template_service = TemplateService(template_path)
        docx_path = template_service.fill_template(request_type,data.to_dict(),j)  
        print(f"📄 Docx path test: {docx_path}")
        pdf_service = PDFService()
        pdf_service.convert_to_pdf(docx_path,request_type, f"{mg_idpreg}_{j}")      
        print(f"✅ PDF generated for {mg_idpreg}_{j}")
    except Exception as e:
        print(f"❌ Error generating PDF for {mg_idpreg}_{j}: {e}")
        return