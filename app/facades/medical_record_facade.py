"""
Medical Record Facade - Unified interface for medical record processing

This module provides a simplified facade interface that orchestrates
the entire medical record processing workflow using the strategy and builder patterns.
"""
import os
import sys
from typing import Optional
from dataclasses import replace

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from strategies.template_factory import TemplateFactory
from strategies.base_template_strategy import BaseTemplateStrategy
from builders.datavant_request_builder import DatavantRequestBuilder
from services.template_service import TemplateService
from services.pdf_service import PDFService
from services.sas_email_service import SASEmailService
from services.external_api_service import get_log_detail_data_from_api, submit_datavant_request
from models.redcap_response_first import RedcapResponseFirst
from models.redcap_response_second import RedcapResponseSecond
from models.datavant_request import Facility, RequesterInfo, Patient, Reason
from utils.counter import Counter
from utils.logger import PandasCSVLogger
from utils.request_tracker import track_smartrequest
from utils.dashboard_tracker import (
    track_processing_start, track_pdf_success, track_pdf_error,
    track_smartrequest_sent, track_smartrequest_success, track_smartrequest_error
)
from utils.dates import get_datavant_date_range
from datetime import datetime


class MedicalRecordFacade:
    """
    Facade providing a unified interface for medical record processing.

    This class orchestrates the entire workflow:
    1. Strategy selection based on template type
    2. PDF generation using templates
    3. Datavant API request submission
    4. Email notifications
    5. Tracking and logging

    The facade hides the complexity of the subsystems and provides
    a simple interface for the record service.
    """

    def __init__(self, factory: Optional[TemplateFactory] = None):
        """
        Initialize the medical record facade

        Args:
            factory: Optional TemplateFactory instance. If None, creates a new one.
        """
        self.factory = factory if factory else TemplateFactory()
        self.template_service: Optional[TemplateService] = None
        self.pdf_service = PDFService()
        self.email_service = SASEmailService()

        # Initialize loggers
        self.pdf_logger = PandasCSVLogger(
            f"logs/pdfs/logs_{datetime.now().strftime('%Y%m%d')}.csv",
            ["record", "timestamp", "username", "request_type", "process_type", "status", "details"]
        )
        self.extended_record_logger = PandasCSVLogger(
            f"logs/extended_records/logs_{datetime.now().strftime('%Y%m%d')}.csv",
            ["record", "timestamp", "username", "request_type", "process_type", "status", "details"]
        )
        self.logger = PandasCSVLogger(
            f"logs/logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            ["record", "timestamp", "username", "status", "details"]
        )

        print("🏛️ MedicalRecordFacade initialized")

    def process_request(
        self,
        data: RedcapResponseFirst,
        request_type: str,
        counter: Counter
    ) -> None:
        """
        Main entry point for processing a medical record request

        Args:
            data: RedcapResponseFirst object with request data
            request_type: Type of request ("first_request", "second_request_complete", etc.)
            counter: Counter object for tracking processed records
        """
        print(f"📋 Processing {request_type} for record {data.record}")

        try:
            # Get mr_req_for value (1=mother, 2=infant, 3=combined)
            mr_req_for = getattr(data, 'mr_req_for', None)
            if not mr_req_for:
                # Try to get from details
                mr_req_for = data.details.get('mr_req_for', '3')  # Default to combined

            # Get strategy for this template type
            strategy = self.factory.get_strategy_for_request(mr_req_for)

            if not strategy:
                raise ValueError(f"No strategy found for mr_req_for={mr_req_for}")

            # Execute workflow with strategy
            self._execute_workflow(strategy, data, request_type, counter, mr_req_for)

        except Exception as e:
            self.logger.log({
                "record": data.record,
                "timestamp": data.timestamp,
                "username": data.username,
                "status": "error",
                "details": f"Error processing {data.record}: {e}"
            })
            print(f"❌ Error processing {data.record}: {e}")
            raise

    def _execute_workflow(
        self,
        strategy: BaseTemplateStrategy,
        data: RedcapResponseFirst,
        request_type: str,
        counter: Counter,
        mr_req_for: str
    ) -> None:
        """
        Execute the common workflow for processing records

        Args:
            strategy: Template strategy to use
            data: Request data
            request_type: Type of request
            counter: Counter for tracking
            mr_req_for: Request for value (1, 2, or 3)
        """
        # Get detailed data from API
        data_to_process = get_log_detail_data_from_api(data)

        if len(data_to_process) == 0:
            print(f"❌ No data to process for {data.record}")
            return

        # Process each item
        for j, item in enumerate(data_to_process):
            print(f"📄 Processing {j+1} of {item.mg_idpreg}")

            # Customize record needs based on strategy
            strategy.customize_record_needs(item)

            # Replace item with updated version
            item = replace(item)

            # Generate PDF
            pdf_path = self._handle_pdf_generation(strategy, item, j, data, request_type)

            # Handle Datavant request if needed
            if item.mr_dv == "1":
                self._handle_datavant_request(strategy, item, j, mr_req_for)
            else:
                print(f"🔄 Skipping Datavant request for {item.mg_idpreg}_{j}")
                # Send SAS email notification
                patient_name = f"{getattr(item, 'bc_momnamefirst', '')} {getattr(item, 'bc_momnamelast', '')}".strip()
                facility_name = getattr(item, 'hos_name', '')
                self.email_service.send_mr_dv_notification(
                    record_id=f"{item.mg_idpreg}_{j}",
                    patient_name=patient_name if patient_name else None,
                    facility_name=facility_name if facility_name else None
                )

            counter.inc()

    def _handle_pdf_generation(
        self,
        strategy: BaseTemplateStrategy,
        item: RedcapResponseSecond,
        j: int,
        first_data: RedcapResponseFirst,
        request_type: str
    ) -> Optional[str]:
        """
        Handle PDF generation using the strategy's template

        Args:
            strategy: Template strategy
            item: Data item to process
            j: Item index
            first_data: First request data
            request_type: Type of request

        Returns:
            Path to generated PDF or None on error
        """
        try:
            mg_idpreg = item.mg_idpreg
            print(f"📄 Generating PDF for {mg_idpreg}_{j}")

            # Track processing start
            patient_name = f"{getattr(item, 'bc_momnamefirst', '')} {getattr(item, 'bc_momnamelast', '')}".strip()
            facility_name = getattr(item, 'hos_name', '')
            username = getattr(first_data, 'username', '')

            track_processing_start(
                f"{mg_idpreg}_{j}",
                request_type,
                patient_name if patient_name else None,
                facility_name if facility_name else None,
                username if username else None
            )

            # Get template path from strategy
            template_path = strategy.get_template_path()

            # Initialize template service if needed
            self.template_service = TemplateService(template_path)

            # Fill template
            docx_path = self.template_service.fill_template(request_type, item.to_dict(), j)
            print(f"📄 DOCX path: {docx_path}")

            # Convert to PDF
            pdf_path = self.pdf_service.convert_to_pdf(docx_path, request_type, f"{mg_idpreg}_{j}")
            print(f"✅ PDF generated for {mg_idpreg}_{j}")

            # Track success
            template_name = strategy.config.name
            track_pdf_success(f"{mg_idpreg}_{j}", pdf_path or "", template_name)

            # Log extended records if needed
            if item.mr_request_days and item.mr_request_days.isdigit() and int(item.mr_request_days) > 50:
                self.extended_record_logger.log({
                    "record": mg_idpreg,
                    "timestamp": first_data.timestamp,
                    "username": first_data.username,
                    "request_type": template_name,
                    "process_type": request_type,
                    "status": "generated",
                    "details": ", ".join(f"{key} = {value}" for key, value in first_data.details.items())
                })

            # Log PDF generation
            self.pdf_logger.log({
                "record": mg_idpreg,
                "timestamp": first_data.timestamp,
                "username": first_data.username,
                "request_type": template_name,
                "process_type": request_type,
                "status": "generated",
                "details": ", ".join(f"{key} = {value}" for key, value in first_data.details.items())
            })

            return pdf_path

        except Exception as e:
            # Track error
            track_pdf_error(f"{mg_idpreg}_{j}", str(e))

            self.logger.log({
                "record": mg_idpreg,
                "timestamp": first_data.timestamp,
                "username": first_data.username,
                "status": "error",
                "details": f"Error generating PDF for {mg_idpreg}_{j}: {e}"
            })
            print(f"❌ Error generating PDF for {mg_idpreg}_{j}: {e}")
            return None

    def _handle_datavant_request(
        self,
        strategy: BaseTemplateStrategy,
        item: RedcapResponseSecond,
        j: int,
        mr_req_for: str
    ) -> None:
        """
        Handle Datavant API request submission using the builder pattern

        Args:
            strategy: Template strategy
            item: Data item
            j: Item index
            mr_req_for: Request for value
        """
        try:
            # Get date range
            date_range = get_datavant_date_range()
            print(f"🗓️ Using Datavant date range: {date_range[0]} to {date_range[1]}")

            # Initialize builder
            builder = DatavantRequestBuilder()

            # Let strategy configure the builder
            strategy.configure_datavant_builder(builder)

            # Get facility (from CSV or form data)
            from services.record_service import _get_facility_for_datavant_request
            facility = _get_facility_for_datavant_request(item)

            # Set requester info
            builder.set_requester_info(
                company_id=1792190,
                company_name="TN DEPT OF HEALTH",
                name="Bhanu Gaddam",
                email="bhanu.prathap.gaddam@tn.gov"
            )

            # Set patient
            builder.set_patient(
                first_name=getattr(item, 'bc_momnamefirst', ''),
                last_name=getattr(item, 'bc_momnamelast', ''),
                date_of_birth=getattr(item, 'bc_mom_dob', ''),
                ssn=getattr(item, 'bc_momssn', ''),
                custom_id=getattr(item, 'mr_custom_id', item.mg_idpreg)
            )

            # Set reason
            params = strategy.get_datavant_params()
            builder.set_reason(
                business_type=params.get('business_type', 'ATTY'),
                api_code=params.get('api_code', 'STATE_ATTY_OFFICE')
            )

            # Set facility
            builder.set_facility(facility)

            # Set request criteria with dates
            builder.set_request_criteria(
                start_date=date_range[0],
                end_date=date_range[1]
            )

            # Set certification
            builder.set_certification_required(params.get('certification_required', False))

            # Set authorization forms
            PATIENT_AUTH_ENCODED = "PATIENT_AUTH_ENCODED"
            REPRESENTATION_LETTER_ENCODED = "REPRESENTATION_LETTER_ENCODED"
            builder.set_authorization_forms([
                PATIENT_AUTH_ENCODED,
                REPRESENTATION_LETTER_ENCODED
            ])

            # Build request
            datavant_request = builder.build()

            print(f"🔄 Datavant request data: {datavant_request}")

            # Submit to API
            api_response = submit_datavant_request(datavant_request)
            print(f"🔄 SmartRequest API response: {api_response}")

            # Track request
            if api_response and api_response.get('requestId'):
                request_id = api_response['requestId']
                patient_name = f"{getattr(item, 'bc_momnamefirst', '')} {getattr(item, 'bc_momnamelast', '')}".strip()
                facility_name = getattr(item, 'hos_name', '')

                track_smartrequest_sent(
                    f"{item.mg_idpreg}_{j}",
                    request_id,
                    datavant_request.model_dump() if hasattr(datavant_request, 'model_dump') else None
                )
                track_smartrequest_success(f"{item.mg_idpreg}_{j}", request_id)
                print(f"✅ SmartRequest tracked as successful for {item.mg_idpreg}_{j}")

                # Original tracking
                track_smartrequest(
                    request_id=request_id,
                    record_id=item.mg_idpreg,
                    document_type="datavant_request",
                    patient_name=patient_name if patient_name else None,
                    facility_name=facility_name if facility_name else None
                )
            else:
                error_msg = "SmartRequest API call failed or returned no requestId"
                if api_response:
                    error_msg += f": {api_response}"
                track_smartrequest_error(f"{item.mg_idpreg}_{j}", error_msg)
                print(f"❌ SmartRequest failed for {item.mg_idpreg}_{j}: {error_msg}")

        except Exception as e:
            error_msg = f"Unexpected error during SmartRequest: {str(e)}"
            track_smartrequest_error(f"{item.mg_idpreg}_{j}", error_msg)
            print(f"❌ SmartRequest exception for {item.mg_idpreg}_{j}: {error_msg}")
