from dataclasses import dataclass
from typing import Any


@dataclass
class NASLogRecord:
    """
    Flat record combining REDCap log top-level fields and parsed details
    for a NAS (Neonatal Abstinence Syndrome) portal entry.
    """
    record: str
    timestamp: str
    username: str

    # Core identifiers
    record_id2: Any = ""

    # Infant fields
    firstname_infant: Any = ""
    lastname_infant: Any = ""
    dob: Any = ""           # infant date of birth
    sex: Any = ""

    # Mother fields
    mothr_first_name: Any = ""
    mothr_last_name: Any = ""
    mothr_dob: Any = ""

    # Hospital / chart
    chart4: Any = ""
    birthhosp: Any = ""
    reporthosp: Any = ""
    hosptype: Any = ""
    hos_name: Any = ""
    hospital_fax_num: Any = ""

    # Request routing
    request_type: Any = ""       # "fax" → PDF generation required; other values → skip
    request_initial: Any = ""    # "1" = first request
    request_second: Any = ""     # "1" = second request; blank = first request

    # Report metadata
    report_date: Any = ""
    days_difference: Any = ""
    day_group: Any = ""
    day_group_categories: Any = ""
    state: Any = ""
    county_tn: Any = ""

    # Clinical
    clinicaldiag_chiefcomp: Any = ""
    clinicalnas_old: Any = ""
    clinicalnas: Any = ""
    symptoms_yes_group: Any = ""
    maternalsubstance_yes: Any = ""
    confirmatory_tests: Any = ""
    mothr_tox_performed: Any = ""
    infant_discharged: Any = ""
    nas_portal_test_complete: Any = ""

    def to_dict(self) -> dict:
        return {
            "record": self.record,
            "timestamp": self.timestamp,
            "username": self.username,
            "record_id2": self.record_id2,
            "firstname_infant": self.firstname_infant,
            "lastname_infant": self.lastname_infant,
            "dob": self.dob,
            "sex": self.sex,
            "mothr_first_name": self.mothr_first_name,
            "mothr_last_name": self.mothr_last_name,
            "mothr_dob": self.mothr_dob,
            "chart4": self.chart4,
            "birthhosp": self.birthhosp,
            "reporthosp": self.reporthosp,
            "hosptype": self.hosptype,
            "hos_name": self.hos_name,
            "hospital_fax_num": self.hospital_fax_num,
            "report_date": self.report_date,
        }
