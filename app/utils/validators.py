from typing import Dict, Any, Optional, Union
#import logging
from models.redcap_response_first import RedcapResponseFirst

#logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)

def _extract_details(data: RedcapResponseFirst) -> Dict[str, Any]:
    """
    Helper function to safely extract details from RedcapResponseFirst object.
    
    Args:
        data: RedcapResponseFirst object
        
    Returns:
        Dict containing the details
        
    Raises:
        ValueError: If details cannot be extracted
    """
    try:
        if isinstance(data.details, dict):
            return data.details
        elif hasattr(data.details, 'to_dict'):
            return data.details.to_dict()
        else:
            # Fallback - try to convert to dict if it's a different type
            return dict(data.details) if data.details else {}
    except Exception as e:
        print(f"❌ Failed to extract details from data object: {e}")
        raise ValueError(f"Invalid details format in data object: {e}")

def _is_truthy_value(value: Any) -> bool:
    """
    Check if a value represents a truthy state in the context of these validators.
    
    Args:
        value: Value to check
        
    Returns:
        bool: True if value represents a truthy state
    """
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() not in ("0", "", "false", "False", "FALSE")
    return bool(value)

def _is_falsy_value(value: Any) -> bool:
    """
    Check if a value represents a falsy state in the context of these validators.
    
    Args:
        value: Value to check
        
    Returns:
        bool: True if value represents a falsy state
    """
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() in ("0", "", "false", "False", "FALSE")
    return not bool(value)

def is_first_request(data: RedcapResponseFirst) -> bool:
    """
    Real-Time: Trigger if First Request is made and no second request yet.
    
    Conditions:
    - mr_request == "1"
    - mr_request_dt is not null/empty
    - mr_request_dt_2 is null/empty
    
    Args:
        data: RedcapResponseFirst object
        
    Returns:
        bool: True if conditions are met
    """
    try:
        details = _extract_details(data)
        
        # Check conditions
        mr_request_valid = is_truthy_or_checked(details.get("mr_request"))
        mr_request_dt_valid = _is_truthy_value(details.get("mr_request_dt"))
        mr_request_dt_2_empty = _is_falsy_value(details.get("mr_request_dt_2"))
        
        result = mr_request_valid and mr_request_dt_valid and mr_request_dt_2_empty
        
        print(f"ℹ️ is_first_request: mr_request={details.get('mr_request')}, "
                    f"mr_request_dt={details.get('mr_request_dt')}, "
                    f"mr_request_dt_2={details.get('mr_request_dt_2')}, "
                    f"result={result}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error in is_first_request: {e}")
        raise ValueError(f"Failed to validate first request: {e}")

def is_second_request_manual_not_received(data: RedcapResponseFirst) -> bool:
    """
    Real-Time: Second request explicitly triggered but records not received.
    
    Conditions:
    - mr_request_2 == "1"
    - mr_request_dt_2 is not null/empty
    - mr_received == "0" or empty/null
    
    Args:
        data: RedcapResponseFirst object
        
    Returns:
        bool: True if conditions are met
    """
    try:
        details = _extract_details(data)
        
        # Check conditions
        mr_request_2_valid = is_truthy_or_checked(details.get("mr_request_2"))
        mr_request_dt_2_valid = _is_truthy_value(details.get("mr_request_dt_2"))
        mr_needs_valid = has_medical_record_needs(data)
        result = mr_request_2_valid and mr_request_dt_2_valid and not mr_needs_valid 
        
        print(f"ℹ️ is_second_request_manual_not_received: mr_request_2={details.get('mr_request_2')}, "
                    f"mr_request_dt_2={details.get('mr_request_dt_2')}, "
                    f"mr_received={details.get('mr_received')}, "
                    f"result={result}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error in is_second_request_manual_not_received: {e}")
        raise ValueError(f"Failed to validate second request manual not received: {e}")

def is_second_request_partial_received(data: RedcapResponseFirst) -> bool:
    """
    Real-Time: Second request done, some records received but not all.
    
    Conditions:
    - mr_request_2 == "1"
    - mr_request_dt_2 is not null/empty
    - mr_received == "1" (some received)
    - mr_rec_all == "0" or empty/null (not all received)
    
    Args:
        data: RedcapResponseFirst object
        
    Returns:
        bool: True if conditions are met
        
    Raises:
        ValueError: If data is invalid
    """
    if not data:
        raise ValueError("Data object cannot be None")
    
    try:
        details = _extract_details(data)
        
        # Check conditions
        mr_request_2_valid = is_truthy_or_checked(details.get("mr_request_2"))
        mr_request_dt_2_valid = _is_truthy_value(details.get("mr_request_dt_2"))
        mr_needs_valid = has_medical_record_needs(data)
        result = (mr_request_2_valid and mr_request_dt_2_valid and mr_needs_valid)
        
        print(f"ℹ️ is_second_request_partial_received: mr_request_2={details.get('mr_request_2')}, "
                    f"mr_request_dt_2={details.get('mr_request_dt_2')}, "
                    f"has_medical_record_needs={mr_needs_valid}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error in is_second_request_partial_received: {e}")
        raise ValueError(f"Failed to validate second request partial received: {e}")

def is_all_records_received(data: RedcapResponseFirst) -> bool:
    """
    Check if all records have been received.
    
    Conditions:
    - mr_received == "1"
    - mr_rec_all == "1"
    
    Args:
        data: RedcapResponseFirst object
        
    Returns:
        bool: True if all records received
    """
    if not data:
        raise ValueError("Data object cannot be None")
    
    try:
        details = _extract_details(data)
        
        mr_received_valid = details.get("mr_received") == "1"
        mr_rec_all_complete = details.get("mr_rec_all") == "1"
        
        result = mr_received_valid and mr_rec_all_complete
        
        print(f"ℹ️ is_all_records_received: mr_received={details.get('mr_received')}, "
                    f"mr_rec_all={details.get('mr_rec_all')}, "
                    f"result={result}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error in is_all_records_received: {e}")
        raise ValueError(f"Failed to validate all records received: {e}")

def get_request_status(data: RedcapResponseFirst) -> str:
    """
    Get a human-readable status of the request based on the data.
    
    Args:
        data: RedcapResponseFirst object
        
    Returns:
        str: Status description
    """
    try:
        if is_all_records_received(data):
            return "All records received"
        elif is_second_request_partial_received(data):
            return "Second request - partial records received"
        elif is_second_request_manual_not_received(data):
            return "Second request - no records received"
        elif is_first_request(data):
            return "First request made"
        else:
            return "Unknown status"
    except Exception as e:
        print(f"❌ Error getting request status: {e}")
        return "Error determining status"

# Validation function to check data integrity
def validate_data_integrity(data: RedcapResponseFirst) -> Dict[str, Any]:
    try:
        details = _extract_details(data)
        
        # Required fields for validation
        required_fields = [
            "mr_request", "mr_request_dt", "mr_request_2", "mr_request_dt_2",
            "mr_received", "mr_rec_all", "mr_rec_all_2", "mr_request_days", "mr_request_days_2"
        ]
        
        missing_fields = [field for field in required_fields if field not in details]
        
        # Logical consistency checks
        inconsistencies = []
        
        # If second request is made, first request should also be made
        if details.get("mr_request_2") == "1" and details.get("mr_request") != "1":
            inconsistencies.append("Second request made without first request")
        
        # If records received, there should be a request
        if (details.get("mr_received") == "1" and 
            details.get("mr_request") != "1" and 
            details.get("mr_request_2") != "1"):
            inconsistencies.append("Records received without any request")
        
        # If all records received, some records should be received
        if details.get("mr_rec_all") == "1" and details.get("mr_received") != "1":
            inconsistencies.append("All records received but mr_received is not 1")
        
        return {
            "valid": len(missing_fields) == 0 and len(inconsistencies) == 0,
            "missing_fields": missing_fields,
            "inconsistencies": inconsistencies,
            "status": get_request_status(data),
            "details_count": len(details)
        }
        
    except Exception as e:
        print(f"❌ Error validating data integrity: {e}")
        return {
            "valid": False,
            "error": str(e),
            "missing_fields": [],
            "inconsistencies": [],
            "status": "Error",
            "details_count": 0
        }

def is_truthy_or_checked(value: Any) -> bool:
    """
    Enhanced helper to check if a value is truthy or checked in REDCap context.
    
    Args:
        value: Value to check
        
    Returns:
        True if value is considered truthy/checked
    """
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() not in ("", "0", "false", "False", "FALSE", "unchecked")
    if isinstance(value, bool):
        return value
    return bool(value)

def has_medical_record_needs(data: RedcapResponseFirst) -> bool:
    """
    Check if there are any medical record needs identified.
    
    Conditions:
    - Any mr_rec_needs field is True or truthy
    - Fields follow pattern: mr_rec_needs(4), mr_rec_needs(6), etc.
    
    Args:
        data: RedcapResponseFirst object
        
    Returns:
        bool: True if any medical record needs are identified
    """
    if not data:
        raise ValueError("Data object cannot be None")
    
    try:
        details = _extract_details(data)
        
        # Find all mr_rec_needs fields and check if any are truthy
        has_needs = False
        active_needs = []
        
        for field_name, field_value in details.items():
            print(f"🔍 field_name: {field_name} field_value: {field_value}")
            # Check if field matches mr_rec_needs pattern
            if "needs" in field_name and _is_truthy_value(field_value):
                    has_needs = True
                    active_needs.append(field_name)
        
        print(f"ℹ️ has_medical_record_needs: active_needs={active_needs}, "
              f"result={has_needs}")
        
        return has_needs
        
    except Exception as e:
        print(f"❌ Error in has_medical_record_needs: {e}")
        raise ValueError(f"Failed to validate medical record needs: {e}")