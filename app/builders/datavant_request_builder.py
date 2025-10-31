"""
Builder for constructing DatavantRequest objects
"""
from typing import List, Optional
from models.datavant_request import (
    DatavantRequest,
    Facility,
    RequesterInfo,
    Patient,
    Reason,
    RequestCriteria,
    CallbackDetails,
    CallbackHeaders
)


class DatavantRequestBuilder:
    """
    Builder class for constructing complex DatavantRequest objects.

    This class implements the Builder Pattern, providing a fluent interface
    for step-by-step construction of Datavant API requests.

    Example usage:
        builder = DatavantRequestBuilder()
        request = (builder
            .set_facility(facility_obj)
            .set_patient(patient_obj)
            .set_record_types(["Lab Reports", "Radiology"])
            .set_request_criteria("2025-01-01", "2025-12-31")
            .build())
    """

    def __init__(self):
        """Initialize the builder with default values"""
        self.reset()

    def reset(self) -> 'DatavantRequestBuilder':
        """
        Reset the builder to initial state

        Returns:
            Self for method chaining
        """
        self._facility: Optional[Facility] = None
        self._requester_info: Optional[RequesterInfo] = None
        self._patient: Optional[Patient] = None
        self._reason: Optional[Reason] = None
        self._request_criteria: List[RequestCriteria] = []
        self._certification_required: bool = False
        self._authorization_forms: List[str] = []
        self._callback_details: Optional[CallbackDetails] = None

        return self

    def set_facility(self, facility: Facility) -> 'DatavantRequestBuilder':
        """
        Set facility information

        Args:
            facility: Facility object

        Returns:
            Self for method chaining
        """
        self._facility = facility
        return self

    def set_facility_from_dict(self, facility_dict: dict) -> 'DatavantRequestBuilder':
        """
        Set facility information from dictionary

        Args:
            facility_dict: Dictionary with facility data

        Returns:
            Self for method chaining
        """
        self._facility = Facility(**facility_dict)
        return self

    def set_requester_info(
        self,
        company_id: int,
        company_name: str,
        name: str,
        email: str
    ) -> 'DatavantRequestBuilder':
        """
        Set requester information

        Args:
            company_id: Company ID in Datavant system
            company_name: Company name
            name: Requester's name
            email: Requester's email

        Returns:
            Self for method chaining
        """
        self._requester_info = RequesterInfo(
            companyId=company_id,
            companyName=company_name,
            name=name,
            email=email
        )
        return self

    def set_patient(
        self,
        first_name: str,
        last_name: str,
        date_of_birth: str,
        ssn: str,
        custom_id: str
    ) -> 'DatavantRequestBuilder':
        """
        Set patient information

        Args:
            first_name: Patient's first name
            last_name: Patient's last name
            date_of_birth: Patient's date of birth (YYYY-MM-DD)
            ssn: Patient's SSN
            custom_id: Custom identifier for tracking

        Returns:
            Self for method chaining
        """
        self._patient = Patient(
            firstName=first_name,
            lastName=last_name,
            dateOfBirth=date_of_birth,
            ssn=ssn,
            customId=custom_id
        )
        return self

    def set_patient_from_obj(self, patient: Patient) -> 'DatavantRequestBuilder':
        """
        Set patient information from Patient object

        Args:
            patient: Patient object

        Returns:
            Self for method chaining
        """
        self._patient = patient
        return self

    def set_reason(self, business_type: str, api_code: str) -> 'DatavantRequestBuilder':
        """
        Set reason for medical record request

        Args:
            business_type: Type of business (e.g., "ATTY")
            api_code: API code for reason (e.g., "STATE_ATTY_OFFICE")

        Returns:
            Self for method chaining
        """
        self._reason = Reason(
            businessType=business_type,
            apiCode=api_code
        )
        return self

    def set_record_types(self, record_types: List[str]) -> 'DatavantRequestBuilder':
        """
        Set record types for the request

        Note: This sets the record types but requires dates to be set via
        set_request_criteria() to create the complete RequestCriteria.

        Args:
            record_types: List of record type names

        Returns:
            Self for method chaining
        """
        self._record_types = record_types
        return self

    def set_request_criteria(
        self,
        start_date: str,
        end_date: str,
        record_types: Optional[List[str]] = None
    ) -> 'DatavantRequestBuilder':
        """
        Set request criteria (date range and record types)

        Args:
            start_date: Start date for records (YYYY-MM-DD)
            end_date: End date for records (YYYY-MM-DD)
            record_types: Optional list of record types. If None, uses previously set types.

        Returns:
            Self for method chaining
        """
        types_to_use = record_types if record_types is not None else getattr(self, '_record_types', [])

        criteria = RequestCriteria(
            recordTypes=types_to_use,
            startDate=start_date,
            endDate=end_date
        )

        # Replace any existing criteria with the same date range
        self._request_criteria = [criteria]

        return self

    def add_request_criteria(
        self,
        start_date: str,
        end_date: str,
        record_types: List[str]
    ) -> 'DatavantRequestBuilder':
        """
        Add additional request criteria (for multiple date ranges)

        Args:
            start_date: Start date for this criteria
            end_date: End date for this criteria
            record_types: Record types for this criteria

        Returns:
            Self for method chaining
        """
        criteria = RequestCriteria(
            recordTypes=record_types,
            startDate=start_date,
            endDate=end_date
        )

        self._request_criteria.append(criteria)

        return self

    def set_certification_required(self, required: bool = True) -> 'DatavantRequestBuilder':
        """
        Set whether certification is required

        Args:
            required: Whether certification is required

        Returns:
            Self for method chaining
        """
        self._certification_required = required
        return self

    def set_authorization_forms(self, forms: List[str]) -> 'DatavantRequestBuilder':
        """
        Set authorization forms (base64 encoded)

        Args:
            forms: List of base64 encoded authorization forms

        Returns:
            Self for method chaining
        """
        self._authorization_forms = forms
        return self

    def add_authorization_form(self, form: str) -> 'DatavantRequestBuilder':
        """
        Add a single authorization form

        Args:
            form: Base64 encoded authorization form

        Returns:
            Self for method chaining
        """
        self._authorization_forms.append(form)
        return self

    def set_callback_details(
        self,
        url: str,
        method: str = "POST",
        authorization: Optional[str] = None
    ) -> 'DatavantRequestBuilder':
        """
        Set callback details for async notifications

        Args:
            url: Callback URL
            method: HTTP method (default: POST)
            authorization: Optional authorization header value

        Returns:
            Self for method chaining
        """
        headers = None
        if authorization:
            headers = CallbackHeaders(
                Authorization=authorization,
                Content_Type="application/json"
            )

        self._callback_details = CallbackDetails(
            method=method,
            url=url,
            headers=headers
        )

        return self

    def build(self) -> DatavantRequest:
        """
        Build and return the DatavantRequest object

        Returns:
            Constructed DatavantRequest object

        Raises:
            ValueError: If required fields are missing
        """
        # Validate required fields
        if not self._facility:
            raise ValueError("Facility is required")

        if not self._requester_info:
            raise ValueError("Requester info is required")

        if not self._patient:
            raise ValueError("Patient info is required")

        if not self._reason:
            raise ValueError("Reason is required")

        if not self._request_criteria:
            raise ValueError("At least one request criteria is required")

        if not self._authorization_forms:
            raise ValueError("At least one authorization form is required")

        # Construct the request
        request = DatavantRequest(
            facility=self._facility,
            requesterInfo=self._requester_info,
            patient=self._patient,
            reason=self._reason,
            requestCriteria=self._request_criteria,
            certificationRequired=self._certification_required,
            authorizationForms=self._authorization_forms,
            callbackDetails=self._callback_details
        )

        return request

    def __repr__(self) -> str:
        """Detailed representation"""
        return (f"DatavantRequestBuilder(facility={'set' if self._facility else 'unset'}, "
                f"patient={'set' if self._patient else 'unset'}, "
                f"criteria={len(self._request_criteria)} items)")
