# src/db/schemas/quotations.py
from pydantic import BaseModel
from typing import List, Optional

class QuoteItemBase(BaseModel):
    product_id: int
    quantity: float
    unit: str
    unit_price: float
    gst_rate: float
    amount: float

class QuoteItemCreate(QuoteItemBase):
    pass

class QuoteItemUpdate(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    unit_price: Optional[float] = None
    gst_rate: Optional[float] = None
    amount: Optional[float] = None

class QuoteItemInDB(QuoteItemBase):
    id: int
    quote_id: int

    class Config:
        from_attributes = True

class QuoteBase(BaseModel):
    quotation_number: str
    quotation_date: str
    customer_id: int
    total_amount: float
    cgst_amount: Optional[float] = None
    sgst_amount: Optional[float] = None
    igst_amount: Optional[float] = None
    voucher_type_id: Optional[int] = None
    voucher_data: Optional[str] = None

class QuoteCreate(QuoteBase):
    items: List[QuoteItemCreate] = []

class QuoteUpdate(BaseModel):
    quotation_number: Optional[str] = None
    quotation_date: Optional[str] = None
    customer_id: Optional[int] = None
    total_amount: Optional[float] = None
    cgst_amount: Optional[float] = None
    sgst_amount: Optional[float] = None
    igst_amount: Optional[float] = None
    voucher_type_id: Optional[int] = None
    voucher_data: Optional[str] = None
    items: Optional[List[QuoteItemUpdate]] = None

class QuoteInDB(QuoteBase):
    id: int
    created_at: str
    items: List[QuoteItemInDB] = []

    class Config:
        from_attributes = True