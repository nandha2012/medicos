import os
import json
from datetime import datetime
from models.redcap_response_first import RedcapResponseFirst
from utils.filters import filter_records, get_latest_records
from services.record_service import process_first_request, process_complete_second_request, process_partial_second_request
from utils.counter import Counter
from utils.validators import is_first_request, is_second_request_manual_not_received, is_second_request_partial_received
from utils.logger import PandasCSVLogger
from services.external_api_service import get_log_data_from_api
# Initialize logger
logger = PandasCSVLogger(f"logs/logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", ["record", "timestamp", "username", "status", "details"])


base_output = os.path.join(os.getcwd(), "output")


if __name__ == "__main__":
    counter = Counter()
    print("🚀 Starting invoice PDF generation...")

    # Setup
    template_path = os.path.join(os.getcwd(), "assets/templates/infant_template.docx")
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    result = get_log_data_from_api()
    # Filter records with non-empty details
    filtered = [entry for entry in result if entry["details"].strip()]
    # Get latest records
    latest_records = get_latest_records(filtered)
    if latest_records:
        print(f"🔎 {len(latest_records)} records found.")
        filtered_records:list[RedcapResponseFirst] = filter_records(latest_records, RedcapResponseFirst)
        for record in filtered_records:
            logger.log({
                "record": record.record,
                "timestamp": record.timestamp,
                "username": record.username,
                "status": "processing",
                "details": ", ".join(f"{key} = {value}" for key, value in record.details.items()) + ","
            })

            if is_first_request(record):
                process_first_request(record,counter)
            elif is_second_request_manual_not_received(record):
                process_complete_second_request(record,counter)
            elif is_second_request_partial_received(record):
                process_partial_second_request(record,counter)
            else:
                print(f"❌ No action needed for {record.record}")
        print(f"✅ PDF Generation Completed {counter.value()}")
    else:
        print("⚠️ No records received from API.")

    exit()


        # Data input
