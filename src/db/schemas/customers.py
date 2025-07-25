from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class CustomerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Customer's full name (required, unique)")
    contact_no: str = Field(..., min_length=10, max_length=15, description="Customer's contact number (required, 10-15 digits)")
    address1: str = Field(..., max_length=255, description="Primary address line (required)")
    address2: Optional[str] = Field(None, max_length=255, description="Secondary address line")
    city: str = Field(..., max_length=100, description="City (required)")
    state: str = Field(..., max_length=100, description="State (required)")
    state_code: str = Field(..., min_length=2, max_length=2, description="State code (required, 2 digits for India)")
    pin: str = Field(..., min_length=6, max_length=6, description="PIN code (required, 6 digits for India)")
    gst_no: Optional[str] = Field(
        None,
        min_length=15,
        max_length=15,
        description="GST number (15 characters for India)",
        pattern=r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$"
    )
    pan_no: Optional[str] = Field(
        None,
        min_length=10,
        max_length=10,
        description="PAN number (10 characters for India)",
        pattern=r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$"
    )
    email: Optional[EmailStr] = Field(None, description="Customer's email address")

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Customer's full name")
    contact_no: Optional[str] = Field(None, min_length=10, max_length=15, description="Customer's contact number")
    address1: Optional[str] = Field(None, max_length=255, description="Primary address line")
    address2: Optional[str] = Field(None, max_length=255, description="Secondary address line")
    city: Optional[str] = Field(None, max_length=100, description="City")
    state: Optional[str] = Field(None, max_length=100, description="State")
    state_code: Optional[str] = Field(None, min_length=2, max_length=2, description="State code (2 digits for India)")
    pin: Optional[str] = Field(None, min_length=6, max_length=6, description="PIN code (6 digits for India)")
    gst_no: Optional[str] = Field(
        None,
        min_length=15,
        max_length=15,
        description="GST number (15 characters for India)",
        pattern=r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$"
    )
    pan_no: Optional[str] = Field(
        None,
        min_length=10,
        max_length=10,
        description="PAN number (10 characters for India)",
        pattern=r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$"
    )
    email: Optional[EmailStr] = Field(None, description="Customer's email address")

class CustomerInDB(CustomerBase):
    id: int = Field(..., description="Unique customer ID (auto-generated)")

    class Config:
        from_attributes = True