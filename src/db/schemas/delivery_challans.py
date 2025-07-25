from pydantic import BaseModel
from typing import List, Optional

class DeliveryChallanItemBase(BaseModel):
    product_id: int
    quantity: float
    unit: str
    unit_price: float
    gst_rate: float
    amount: float

class DeliveryChallanItemCreate(DeliveryChallanItemBase):
    pass

class DeliveryChallanItemUpdate(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    unit_price: Optional[float] = None
    gst_rate: Optional[float] = None
    amount: Optional[float] = None

class DeliveryChallanItemInDB(DeliveryChallanItemBase):
    id: int
    dc_id: int

    class Config:
        from_attributes = True

class DeliveryChallanBase(BaseModel):
    dc_number: str
    customer_id: int
    dc_date: str
    delivery_date: Optional[str] = None
    payment_terms: Optional[str] = None
    total_amount: float
    cgst_amount: Optional[float] = None
    sgst_amount: Optional[float] = None
    igst_amount: Optional[float] = None
    is_deleted: int = 0
    voucher_type_id: Optional[int] = None

class DeliveryChallanCreate(DeliveryChallanBase):
    items: List[DeliveryChallanItemCreate] = []

class DeliveryChallanUpdate(BaseModel):
    dc_number: Optional[str] = None
    customer_id: Optional[int] = None
    dc_date: Optional[str] = None
    delivery_date: Optional[str] = None
    payment_terms: Optional[str] = None
    total_amount: Optional[float] = None
    cgst_amount: Optional[float] = None
    sgst_amount: Optional[float] = None
    igst_amount: Optional[float] = None
    is_deleted: Optional[int] = None
    voucher_type_id: Optional[int] = None
    items: Optional[List[DeliveryChallanItemUpdate]] = None

class DeliveryChallanInDB(DeliveryChallanBase):
    id: int
    created_at: str
    updated_at: str
    items: List[DeliveryChallanItemInDB] = []

    class Config:
        from_attributes = True