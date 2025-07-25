from pydantic import BaseModel
from typing import List, Optional

class SalesOrderItemBase(BaseModel):
    product_id: int
    product_name: str
    hsn_code: Optional[str] = None
    quantity: float
    unit: str
    unit_price: float
    gst_rate: float
    amount: float

class SalesOrderItemCreate(SalesOrderItemBase):
    pass

class SalesOrderItemUpdate(BaseModel):
    product_id: Optional[int] = None
    product_name: Optional[str] = None
    hsn_code: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    unit_price: Optional[float] = None
    gst_rate: Optional[float] = None
    amount: Optional[float] = None

class SalesOrderItemInDB(SalesOrderItemBase):
    id: int
    sales_order_id: int

    class Config:
        from_attributes = True

class SalesOrderBase(BaseModel):
    sales_order_number: str
    customer_id: int
    sales_order_date: str
    delivery_date: Optional[str] = None
    payment_terms: Optional[str] = None
    total_amount: float
    cgst_amount: Optional[float] = None
    sgst_amount: Optional[float] = None
    igst_amount: Optional[float] = None
    is_deleted: int = 0
    voucher_type_id: Optional[int] = None

class SalesOrderCreate(SalesOrderBase):
    items: List[SalesOrderItemCreate] = []

class SalesOrderUpdate(BaseModel):
    sales_order_number: Optional[str] = None
    customer_id: Optional[int] = None
    sales_order_date: Optional[str] = None
    delivery_date: Optional[str] = None
    payment_terms: Optional[str] = None
    total_amount: Optional[float] = None
    cgst_amount: Optional[float] = None
    sgst_amount: Optional[float] = None
    igst_amount: Optional[float] = None
    is_deleted: Optional[int] = None
    voucher_type_id: Optional[int] = None
    items: Optional[List[SalesOrderItemUpdate]] = None

class SalesOrderInDB(SalesOrderBase):
    id: int
    created_at: str
    updated_at: str
    items: List[SalesOrderItemInDB] = []

    class Config:
        from_attributes = True