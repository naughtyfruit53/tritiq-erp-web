# src/db/schemas/proforma_invoices.py
from pydantic import BaseModel
from typing import List, Optional

class ProformaInvItemBase(BaseModel):
    product_id: int
    quantity: float
    unit: str
    unit_price: float
    gst_rate: float
    amount: float

class ProformaInvItemCreate(ProformaInvItemBase):
    pass

class ProformaInvItemUpdate(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    unit_price: Optional[float] = None
    gst_rate: Optional[float] = None
    amount: Optional[float] = None

class ProformaInvItemInDB(ProformaInvItemBase):
    id: int
    proforma_inv_id: int

    class Config:
        from_attributes = True

class ProformaInvoiceBase(BaseModel):
    proforma_inv_number: str
    proforma_date: str
    customer_id: int
    total_amount: float
    cgst_amount: Optional[float] = None
    sgst_amount: Optional[float] = None
    igst_amount: Optional[float] = None
    voucher_type_id: Optional[int] = None
    voucher_data: Optional[str] = None

class ProformaInvoiceCreate(ProformaInvoiceBase):
    items: List[ProformaInvItemCreate] = []

class ProformaInvoiceUpdate(BaseModel):
    proforma_inv_number: Optional[str] = None
    proforma_date: Optional[str] = None
    customer_id: Optional[int] = None
    total_amount: Optional[float] = None
    cgst_amount: Optional[float] = None
    sgst_amount: Optional[float] = None
    igst_amount: Optional[float] = None
    voucher_type_id: Optional[int] = None
    voucher_data: Optional[str] = None
    items: Optional[List[ProformaInvItemUpdate]] = None

class ProformaInvoiceInDB(ProformaInvoiceBase):
    id: int
    created_at: str
    items: List[ProformaInvItemInDB] = []

    class Config:
        from_attributes = True