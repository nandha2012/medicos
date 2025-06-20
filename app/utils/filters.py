from dataclasses import fields, is_dataclass
from typing import Type, List, Dict, Any

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