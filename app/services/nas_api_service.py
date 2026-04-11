#!/usr/bin/env python
"""
NAS REDCap API service.

Handles:
- First API  : log endpoint  → list of raw log entries
- Second API : record export → full record fields for a given record_id2

When ENV=local, responses are read from sample JSON files instead of
hitting the live API.
"""

import json
import os
import sys
import requests
from typing import List, Dict, Any

from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Configuration (shared with external_api_service.py pattern)
# ---------------------------------------------------------------------------
end_point: str = os.getenv("NAS_API_END_POINT") or "https://localhost/redcap/api/"
token: str = os.getenv("NAS_API_TOKEN") or ""
env: str = os.getenv("ENV") or "local"

# Fields requested from the second (record export) API
_DETAIL_FIELDS: List[str] = [
    "record_id2",
    "report_date",
    "dob",
    "firstname_infant",
    "lastname_infant",
    "mothr_first_name",
    "mothr_last_name",
    "mothr_dob",
    "chart4",
    "birthhosp",
    "reporthosp",
    "hosptype",
    "hos_name",
    "hospital_fax_num",
]


def _build_detail_payload(record_id2: str) -> dict:
    payload = {
        "token": token,
        "content": "record",
        "action": "export",
        "format": "json",
        "type": "flat",
        "csvDelimiter": "",
        "rawOrLabel": "raw",
        "rawOrLabelHeaders": "raw",
        "exportCheckboxLabel": "false",
        "exportSurveyFields": "false",
        "exportDataAccessGroups": "false",
        "returnFormat": "json",
        f"records[0]": record_id2,
        "forms[0]": "medical_records_request_form",
    }
    for i, field in enumerate(_DETAIL_FIELDS):
        payload[f"fields[{i}]"] = field
    return payload


# ---------------------------------------------------------------------------
# Public API functions
# ---------------------------------------------------------------------------

def get_nas_log_data(begin_time: str, end_time: str) -> List[Dict[str, Any]]:
    """
    Fetch NAS REDCap log entries between begin_time and end_time.

    In local ENV, reads from app/nas_response_1_sample.json.

    Returns:
        List of raw log entry dicts (timestamp, username, action, details, record).
    """
    payload = {
        "token": token,
        "content": "log",
        "logtype": "",
        "user": "",
        "record": "",
        "beginTime": begin_time,
        "endTime": end_time,
        "format": "json",
        "returnFormat": "json",
    }
    print(f"🔍 NAS log fetch: {begin_time} → {end_time}")

    if env == "local":
        sample_paths = [
            "app/nas_response_1_sample.json",
            "nas_response_1_sample.json",
        ]
        for path in sample_paths:
            if os.path.exists(path):
                print("📂 Using local NAS sample log data")
                with open(path) as f:
                    return json.load(f)
        print("⚠️ NAS sample log file not found — returning empty list")
        return []

    try:
        response = requests.post(end_point, data=payload, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print("❌ NAS log API timeout")
        return []
    except Exception as e:
        print(f"❌ Error fetching NAS log data: {e}")
        return []


def get_nas_detail_data(record_id2: str) -> Dict[str, Any] | None:
    """
    Fetch full record fields for a single record_id2 from the NAS REDCap project.

    In local ENV, reads from app/nas_response_2_sample.json and filters by record_id2.

    Returns:
        Merged flat dict of all exported fields for the record, or None if API fails.
    """
    if env == "local":
        sample_paths = [
            "app/nas_response_2_sample.json",
            "nas_response_2_sample.json",
        ]
        for path in sample_paths:
            if os.path.exists(path):
                print(f"📂 Using local NAS sample detail data for {record_id2}")
                with open(path) as f:
                    data = json.load(f)
                matching = [r for r in data if str(r.get("record_id2", "")) == str(record_id2)]
                return _merge_rows(matching)
        print(f"⚠️ NAS sample detail file not found for {record_id2} — returning None")
        return None

    payload = _build_detail_payload(record_id2)
    print(f"🔍 NAS detail API payload for {record_id2}:")
    for key, value in payload.items():
        print(f"  {key}: {value}")
    try:
        response = requests.post(end_point, data=payload, timeout=60)
        response.raise_for_status()
        rows = response.json()
        return _merge_rows(rows)
    except requests.exceptions.Timeout:
        print(f"❌ NAS detail API timeout for {record_id2}")
        return None
    except Exception as e:
        print(f"❌ Error fetching NAS detail data for {record_id2}: {e}")
        return None


def _merge_rows(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Merge multiple REDCap repeat-instrument rows into one flat dict,
    preferring non-empty values (same pattern as existing merge_records utility).
    """
    merged: Dict[str, Any] = {}
    for row in rows:
        for key, value in row.items():
            if value not in ("", None):
                merged[key] = value
    return merged
