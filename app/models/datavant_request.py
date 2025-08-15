from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class Facility(BaseModel):
    addressLine1: str
    addressLine2: Optional[str] = None
    city: str
    state: str
    zip: str
    healthSystem: str
    siteName: str
    phone: str
    fax: str

class RequesterInfo(BaseModel):
    companyId: int
    companyName: str
    name: str
    email: str

class Patient(BaseModel):
    firstName: str
    lastName: str
    dateOfBirth: str
    ssn: str
    customId: str

class Reason(BaseModel):
    businessType: str
    apiCode: str

class RequestCriteria(BaseModel):
    recordTypes: List[str]
    startDate: str
    endDate: str

class CallbackHeaders(BaseModel):
    Authorization: str
    Content_Type: str = "application/json"

class CallbackDetails(BaseModel):
    method: str = Field(default="POST", description="HTTP method for callback")
    url: str
    headers: Optional[CallbackHeaders] = None

class DatavantRequest(BaseModel):
    facility: Facility
    requesterInfo: RequesterInfo
    patient: Patient
    reason: Reason
    requestCriteria: List[RequestCriteria]
    certificationRequired: bool = False
    authorizationForms: List[str]
    callbackDetails: Optional[CallbackDetails] = None