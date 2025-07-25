from pydantic import BaseModel
from typing import List, Optional

class SalesInvItemBase(BaseModel):
    product_id: int
    quantity: float
    unit: str
    unit_price: float
    gst_rate: float
    amount: float

class SalesInvItemCreate(SalesInvItemBase):
    pass

class SalesInvItemUpdate(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    unit_price: Optional[float] = None
    gst_rate: Optional[float] = None
    amount: Optional[float] = None

class SalesInvItemInDB(SalesInvItemBase):
    id: int
    sales_inv_id: int

    class Config:
        from_attributes = True

class SalesInvoiceBase(BaseModel):
    sales_inv_number: str
    invoice_date: str
    sales_order_id: Optional[int] = None
    customer_id: int
    total_amount: float
    cgst_amount: Optional[float] = None
    sgst_amount: Optional[float] = None
    igst_amount: Optional[float] = None
    voucher_type_id: Optional[int] = None
    voucher_data: Optional[str] = None

class SalesInvoiceCreate(SalesInvoiceBase):
    items: List[SalesInvItemCreate] = []

class SalesInvoiceUpdate(BaseModel):
    sales_inv_number: Optional[str] = None
    invoice_date: Optional[str] = None
    sales_order_id: Optional[int] = None
    customer_id: Optional[int] = None
    total_amount: Optional[float] = None
    cgst_amount: Optional[float] = None
    sgst_amount: Optional[float] = None
    igst_amount: Optional[float] = None
    voucher_type_id: Optional[int] = None
    voucher_data: Optional[str] = None
    items: Optional[List[SalesInvItemUpdate]] = None

class SalesInvoiceInDB(SalesInvoiceBase):
    id: int
    created_at: str
    items: List[SalesInvItemInDB] = []

    class Config:
        from_attributes = True