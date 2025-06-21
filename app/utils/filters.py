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

def parse_details(details_str: str, strict_mode: bool = False) -> Dict[str, Any]:
    """
    Advanced version with type conversion and validation.
    
    Args:
        details_str (str): The details string to parse
        strict_mode (bool): If True, raises exceptions on parsing errors
        
    Returns:
        Dict[str, Any]: Parsed key-value pairs with type conversion
        
    Raises:
        ValueError: If strict_mode=True and parsing fails
    """
    if not details_str or not isinstance(details_str, str):
        if strict_mode:
            raise ValueError("Details string cannot be empty or non-string")
        return {}
    
    details_str = details_str.strip()
    if not details_str:
        return {}
    
    try:
        if '=' not in details_str:
            if strict_mode:
                raise ValueError(f"No key=value patterns found in: {details_str}")
            return {}
        
        result = {}
        
        # More comprehensive pattern that handles:
        # - Regular fields: key = 'value'
        # - Checkbox fields: key(number) = checked/unchecked
        # - Nested quotes and special characters
        pattern = r"(\w+(?:\(\d+\))?)\s*=\s*(?:'([^']*)'|\"([^\"]*)\"|([^,]+))"
        
        matches = re.findall(pattern, details_str)
        
        if not matches:
            error_msg = f"No valid key=value pairs found in: {details_str}"
            if strict_mode:
                raise ValueError(error_msg)
            print(f"Error parsing details: {error_msg}")
            return {}
        
        for match in matches:
            key = match[0].strip()
            raw_value = (match[1] or match[2] or match[3] or '').strip()
            
            if not key:
                continue
            
            # Type conversion
            value = _convert_value_type(raw_value)
            result[key] = value
            
        return result
        
    except Exception as e:
        error_msg = f"Error parsing details '{details_str}': {e}"
        if strict_mode:
            raise ValueError(error_msg) from e
        print(f'Error parsing details: {error_msg}')
        return {}

def _convert_value_type(value_str: str) -> Any:
    """
    Convert string value to appropriate Python type.
    Handles special cases for REDCap checkbox values.
    
    Args:
        value_str (str): String value to convert
        
    Returns:
        Any: Converted value (bool for checked/unchecked, int, float, or str)
    """
    if not value_str:
        return ''
    
    value_str = value_str.strip()
    
    # Handle REDCap checkbox values
    if value_str.lower() == 'checked':
        return True
    elif value_str.lower() == 'unchecked':
        return False
    
    # Boolean conversion
    if value_str.lower() in ('true', 'false'):
        return value_str.lower() == 'true'
    
    # Integer conversion
    if value_str.isdigit() or (value_str.startswith('-') and value_str[1:].isdigit()):
        try:
            return int(value_str)
        except ValueError:
            pass
    
    # Float conversion
    try:
        if '.' in value_str:
            return float(value_str)
    except ValueError:
        pass
    
    # Return as string
    return value_str

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
            required_fields = [
                "mr_request", "mr_request_dt", "mr_request_2", "mr_request_dt_2",
                "mr_received", "mr_rec_all", "mr_rec_all_2","mr_request_days","mr_request_days_2"
            ]
            for key in required_fields:
                if key not in parsed_details:  # Only set if key doesn't exist
                    parsed_details[key] = "0"
            rec_copy['details'] = parsed_details
            latest_records[record_id] = rec_copy

    # Convert timestamp back to string if needed
    for rec in latest_records.values():
        rec['timestamp'] = rec['timestamp'].strftime("%Y-%m-%d %H:%M")

    return list(latest_records.values())

def merge_records(records: List[Dict]) -> Dict:
    merged = {}
    for record in records:
        for key, value in record.items():
            if value not in ("", None):
                merged[key] = value
    return merged
    