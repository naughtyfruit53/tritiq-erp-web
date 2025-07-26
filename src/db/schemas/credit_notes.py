# src/db/schemas/credit_notes.py
from pydantic import BaseModel
from typing import List, Optional

class CnItemBase(BaseModel):
    product_id: int
    quantity: float
    unit: str
    unit_price: float
    gst_rate: float
    amount: float

class CnItemCreate(CnItemBase):
    pass

class CnItemUpdate(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    unit_price: Optional[float] = None
    gst_rate: Optional[float] = None
    amount: Optional[float] = None

class CnItemInDB(CnItemBase):
    id: int
    cn_id: int

    class Config:
        from_attributes = True

class CreditNoteBase(BaseModel):
    cn_number: str
    cn_date: str
    sales_inv_id: Optional[int] = None
    customer_id: int
    total_amount: float
    cgst_amount: Optional[float] = None
    sgst_amount: Optional[float] = None
    igst_amount: Optional[float] = None
    voucher_type_id: Optional[int] = None
    voucher_data: Optional[str] = None

class CreditNoteCreate(CreditNoteBase):
    items: List[CnItemCreate] = []

class CreditNoteUpdate(BaseModel):
    cn_number: Optional[str] = None
    cn_date: Optional[str] = None
    sales_inv_id: Optional[int] = None
    customer_id: Optional[int] = None
    total_amount: Optional[float] = None
    cgst_amount: Optional[float] = None
    sgst_amount: Optional[float] = None
    igst_amount: Optional[float] = None
    voucher_type_id: Optional[int] = None
    voucher_data: Optional[str] = None
    items: Optional[List[CnItemUpdate]] = None

class CreditNoteInDB(CreditNoteBase):
    id: int
    created_at: str
    items: List[CnItemInDB] = []

    class Config:
        from_attributes = True