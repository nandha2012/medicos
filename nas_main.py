#!/usr/bin/env python
"""
NAS Medical Records PDF Generator
-----------------------------------
Fetches NAS REDCap log entries, resolves full record details, and generates
two PDFs per record using the NAS fax transmittal templates:
  - NAS_MR_MOTHER.docx  → <record_id2>_mother.pdf
  - NAS_MR_INFANT.docx  → <record_id2>_infant.pdf

Output folder: output/nas/<date>/<record_type>/

Usage:
    python nas_main.py
    python nas_main.py --begin_time="2026-04-03 08:00" --end_time="2026-04-04 11:04"
    python nas_main.py --time_delta=2 --time_delta_period=hours
"""

import os
import sys
import subprocess
import platform

# Override OUTPUT_DIR BEFORE importing any app services — pdf_service and
# nas_template_service read this env var at module level.
os.environ["OUTPUT_DIR"] = os.path.join(os.getenv("OUTPUT_DIR") or "output", "nas")

# Make app/ importable without modifying existing code
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

from datetime import datetime

from models.nas_record import NASLogRecord
from services.nas_api_service import get_nas_log_data, get_nas_detail_data
from services.nas_template_service import NASTemplateService
from services.pdf_service import PDFService
from utils.filters import filter_records, get_latest_records
from utils.counter import Counter
from utils.logger import PandasCSVLogger
from utils.dates import get_current_time_str, subtract_time_from_str, generate_dir_name


# ---------------------------------------------------------------------------
# CLI argument parsing (same pattern as external_api_service.py)
# ---------------------------------------------------------------------------
def _parse_arg(flag_name: str, default_value: str) -> str:
    for arg in sys.argv[1:]:
        if arg.startswith(f"--{flag_name}="):
            return arg.split("=", 1)[1]
    return default_value


begin_time_arg: str = _parse_arg("begin_time", "")
end_time_arg: str = _parse_arg("end_time", "")
time_delta: int = int(_parse_arg("time_delta", os.getenv("NAS_TIME_DELTA") or "1"))
time_delta_period: str = _parse_arg("time_delta_period", os.getenv("NAS_TIME_DELTA_PERIOD") or "hours")

# Resolve begin/end times
_now = get_current_time_str()
end_time: str = end_time_arg or _now
begin_time: str = begin_time_arg or subtract_time_from_str(_now, time_delta, time_delta_period)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
NAS_MOTHER_TEMPLATE = os.path.join(
    os.path.dirname(__file__), "assets", "templates", "nas_mr", "NAS_MR_MOTHER.docx"
)
NAS_INFANT_TEMPLATE = os.path.join(
    os.path.dirname(__file__), "assets", "templates", "nas_mr", "NAS_MR_INFANT.docx"
)

# Output subdirectory names per request type
NAS_FIRST_REQUEST  = "first_request"
NAS_SECOND_REQUEST = "second_request"


def _get_record_type(nas_record) -> str | None:
    """
    Determine whether this NAS record should be processed and which type it is.

    Rules:
      - request_type must contain "fax" (case-insensitive); otherwise skip (return None)
      - request_initial = "1"  AND request_second blank → first_request
      - request_second  = "1"                           → second_request
      - Neither condition met                           → skip (return None)
    """
    request_type = str(nas_record.request_type or "").strip().lower()
    if "fax" not in request_type:
        return None

    request_second  = str(nas_record.request_second  or "").strip()
    request_initial = str(nas_record.request_initial or "").strip()

    if request_second == "1":
        return NAS_SECOND_REQUEST
    if request_initial == "1" and request_second == "":
        return NAS_FIRST_REQUEST

    return None

# ---------------------------------------------------------------------------
# Logger
# ---------------------------------------------------------------------------
_log_dir = os.path.join("logs", "nas")
os.makedirs(_log_dir, exist_ok=True)
_log_path = os.path.join(_log_dir, f"logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
logger = PandasCSVLogger(
    _log_path,
    ["record_id2", "timestamp", "username", "template", "status", "details"],
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _ensure_word_running():
    """
    On macOS, docx2pdf uses Word AppleScript automation and will time out if
    Word is not already open. This function activates Word before the first
    conversion so subsequent calls succeed immediately.
    """
    if platform.system() != "Darwin":
        return
    try:
        subprocess.run(
            ["osascript", "-e", 'tell application "Microsoft Word" to activate'],
            check=True, capture_output=True, timeout=15
        )
        import time; time.sleep(3)   # give Word a moment to fully launch
        print("📝 Microsoft Word is ready for PDF conversion")
    except Exception as e:
        print(f"⚠️ Could not activate Microsoft Word — PDF conversion may time out: {e}")


def _flatten_log_record(rec: dict) -> dict:
    """
    Merge top-level log fields (record, timestamp, username) with the parsed
    details dict into a single flat dict suitable for filter_records().
    """
    flat = {
        "record":    rec.get("record", ""),
        "timestamp": rec.get("timestamp", ""),
        "username":  rec.get("username", ""),
    }
    details = rec.get("details", {})
    if isinstance(details, dict):
        flat.update(details)
    return flat


def _build_data(nas_record: NASLogRecord, detail: dict) -> dict:
    """
    Combine NASLogRecord fields with second-API detail fields into a flat data
    dict for the template service. Detail values take precedence for shared keys.
    """
    data = nas_record.to_dict()
    for key, value in detail.items():
        if value not in ("", None):
            data[key] = value
    return data


def _generate_pdf(template_path: str, data: dict, suffix: str,
                  template_svc: NASTemplateService, pdf_svc: PDFService,
                  record_id2: str, record_type: str) -> str:
    """
    Fill template → save docx → convert to PDF.
    Returns the PDF path on success, "" on failure.
    docx2pdf on macOS can fail silently (no exception), so we verify the
    file was actually created after conversion.
    """
    filename = f"{record_id2}_{suffix}"
    try:
        docx_path = template_svc.fill_template(
            template_path=template_path,
            data=data,
            sub_dir=record_type,
            output_filename=filename,
        )
        pdf_path = pdf_svc.convert_to_pdf(docx_path, record_type, filename)

        # docx2pdf on macOS can time out without raising an exception;
        # verify the output file actually exists before declaring success.
        if not os.path.exists(pdf_path):
            raise RuntimeError(
                f"PDF file was not created at {pdf_path} — "
                "docx2pdf conversion may have timed out (check that Microsoft Word is running)"
            )

        print(f"✅ PDF generated: {pdf_path}")
        return pdf_path
    except Exception as e:
        print(f"❌ Error generating {suffix} PDF for {record_id2}: {e}")
        return ""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    counter = Counter()
    print("🚀 Starting NAS PDF generation...")
    print(f"📅 Fetching records from {begin_time} to {end_time}")

    # 1. Fetch log entries
    raw_logs = get_nas_log_data(begin_time, end_time)
    filtered_logs = [entry for entry in raw_logs if entry.get("details", "").strip()]

    if not filtered_logs:
        print("⚠️ No NAS log records found.")
        sys.exit(0)

    # 2. Deduplicate to latest entry per record
    latest = get_latest_records(filtered_logs)
    print(f"🔎 {len(latest)} unique NAS record(s) found.")

    # 3. Map to NASLogRecord instances
    flattened = [_flatten_log_record(r) for r in latest]
    nas_records: list[NASLogRecord] = filter_records(flattened, NASLogRecord)

    if not nas_records:
        print("⚠️ No valid NAS records after filtering.")
        sys.exit(0)

    # 4. Initialise services once (they set up dated output dirs internally)
    _ensure_word_running()
    template_svc = NASTemplateService()
    pdf_svc = PDFService()

    # 5. Process each record
    for nas_record in nas_records:
        record_id2 = str(nas_record.record_id2 or nas_record.record)

        # Determine request type; skip records that don't require a fax PDF
        record_type = _get_record_type(nas_record)
        if record_type is None:
            print(f"\n⏭️  Skipping {record_id2} — request_type={nas_record.request_type!r}, "
                  f"request_initial={nas_record.request_initial!r}, "
                  f"request_second={nas_record.request_second!r}")
            continue

        print(f"\n📋 Processing NAS record: {record_id2} [{record_type}]")

        # Fetch second-API detail data
        detail = get_nas_detail_data(record_id2)

        # Merge all data
        data = _build_data(nas_record, detail)

        # Generate mother PDF
        mother_pdf = _generate_pdf(
            NAS_MOTHER_TEMPLATE, data, "mother", template_svc, pdf_svc, record_id2, record_type
        )
        logger.log({
            "record_id2": record_id2,
            "timestamp":  nas_record.timestamp,
            "username":   nas_record.username,
            "template":   "mother",
            "status":     "generated" if mother_pdf else "error",
            "details":    mother_pdf or "PDF conversion failed",
        })

        # Generate infant PDF
        infant_pdf = _generate_pdf(
            NAS_INFANT_TEMPLATE, data, "infant", template_svc, pdf_svc, record_id2, record_type
        )
        logger.log({
            "record_id2": record_id2,
            "timestamp":  nas_record.timestamp,
            "username":   nas_record.username,
            "template":   "infant",
            "status":     "generated" if infant_pdf else "error",
            "details":    infant_pdf or "PDF conversion failed",
        })

        counter.inc()

    print(f"\n✅ NAS PDF generation complete. Records processed: {counter.value()}")
