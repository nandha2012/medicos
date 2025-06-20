import os
from models.redcap_response_first import RedcapResponseFirst
from utils.filters import filter_records, get_latest_records
from services.record_service import process_first_request, process_complete_second_request, process_partial_second_request
from utils.counter import Counter
from utils.validators import is_first_request, is_second_request, is_second_request_partial
import json
base_output = os.path.join(os.getcwd(), "output")


if __name__ == "__main__":
    counter = Counter()
    print("🚀 Starting invoice PDF generation...")

    # Setup
    template_path = os.path.join(os.getcwd(), "assets/templates/infant_template.docx")
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # result = get_log_data_from_api()
    # Load result
    result = json.load(open('app/response_1_sample.json'))
    print(len(result))

    # Get latest records
    latest_records = get_latest_records(result)

    if latest_records:
        print(f"🔎 {len(latest_records)} records found.")
        filtered_records = filter_records(latest_records, RedcapResponseFirst)
        for record in filtered_records:
            process_partial_second_request(record,counter)
            '''
            if is_first_request(record):
                process_first_request(record,counter)
            elif is_second_request(record):
                process_complete_second_request(record)
            elif is_second_request_partial(record):
                process_partial_second_request(record)
            else:
                print(f"❌ No action needed for {record.record}")
            print(f"✅ PDF Generation Completed {counter.value()}")
    else:
        print("⚠️ No records received from API.")
'''
    exit()


        # Data input
