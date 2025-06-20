from dataclasses import fields, is_dataclass
from typing import Type, List, Dict, Any
from datetime import datetime
import re


def filter_records(records: List[Dict[str, Any]], model_class: Type):
    valid_field_names = {f.name for f in fields(model_class)}
    result = []
    for record in records:
        filtered_record = {k: v for k, v in record.items() if k in valid_field_names}
        
        try:
            result.append(model_class(**filtered_record))  # Can raise TypeError if required fields are missing
        except TypeError as e:
            print(f"Skipping invalid record due to error: {e}\nRecord: {record}")

    return result

def parse_details(details_str):
    """Converts a details string like "mr_upload = '1382031'" to a dictionary."""
    try:
        # Basic parsing assuming format: key = 'value'
        match = re.match(r"(\w+)\s*=\s*'([^']+)'", details_str)
        if match:
            key, value = match.groups()
            return {key: value}
    except Exception as e:
        print(f"Error parsing details: {e}")
    return {}

def get_latest_records(records):
    latest_records = {}

    for rec in records:
        record_id = rec.get("record")
        timestamp_str = rec.get("timestamp")

        # Convert string to datetime object
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M")

        if record_id not in latest_records or timestamp > latest_records[record_id]['timestamp']:
            rec_copy = rec.copy()
            rec_copy['timestamp'] = timestamp
            parsed_details = parse_details(rec.get('details', ''))
                        # Default required fields to "0" if not present
            for key in [
                "mr_request", "mr_request_dt", "mr_request_2", "mr_request_dt_2",
                "mr_received", "mr_rec_all", "mr_rec_all_2"
            ]:
                parsed_details.setdefault(key, "0")

            rec_copy['details'] = parsed_details
            latest_records[record_id] = rec_copy

    # Convert timestamp back to string if needed
    for rec in latest_records.values():
        rec['timestamp'] = rec['timestamp'].strftime("%Y-%m-%d %H:%M")

    return list(latest_records.values())
    