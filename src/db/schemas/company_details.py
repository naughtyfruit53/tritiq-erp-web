# src/db/schemas/company_details.py
from pydantic import BaseModel

class CompanyDetailBase(BaseModel):
    company_name: str
    address1: str
    address2: str | None = None
    city: str
    state: str
    pin: str
    state_code: str
    gst_no: str | None = None
    pan_no: str | None = None
    contact_no: str
    email: str | None = None
    logo_path: str | None = None

class CompanyDetailCreate(CompanyDetailBase):
    pass

class CompanyDetailUpdate(BaseModel):
    company_name: str | None = None
    address1: str | None = None
    address2: str | None = None
    city: str | None = None
    state: str | None = None
    pin: str | None = None
    state_code: str | None = None
    gst_no: str | None = None
    pan_no: str | None = None
    contact_no: str | None = None
    email: str | None = None
    logo_path: str | None = None

class CompanyDetailInDB(CompanyDetailBase):
    id: int

    class Config:
        from_attributes = True