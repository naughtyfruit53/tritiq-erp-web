# src/db/schemas/vendors.py
from pydantic import BaseModel

class VendorBase(BaseModel):
    name: str
    contact_no: str
    address1: str
    address2: str | None = None
    city: str
    state: str
    pin: str
    state_code: str
    gst_no: str | None = None
    pan_no: str | None = None
    email: str | None = None

class VendorCreate(VendorBase):
    pass

class VendorUpdate(BaseModel):
    name: str | None = None
    contact_no: str | None = None
    address1: str | None = None
    address2: str | None = None
    city: str | None = None
    state: str | None = None
    pin: str | None = None
    state_code: str | None = None
    gst_no: str | None = None
    pan_no: str | None = None
    email: str | None = None

class VendorInDB(VendorBase):
    id: int

    class Config:
        from_attributes = True