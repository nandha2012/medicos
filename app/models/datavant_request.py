from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class Facility(BaseModel):
    addressLine1: str
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
    method: str
    url: str
    headers: CallbackHeaders

class DatavantRequest(BaseModel):
    facility: Facility
    requesterInfo: RequesterInfo
    patient: Patient
    reason: Reason
    requestCriteria: List[RequestCriteria]
    certificationRequired: bool
    authorizationForms: List[str]
    callbackDetails: CallbackDetails