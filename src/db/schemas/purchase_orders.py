from pydantic import BaseModel
from typing import List, Optional

class PoItemBase(BaseModel):
    product_id: int
    quantity: float
    unit: str
    unit_price: float
    gst_rate: float
    amount: float

class PoItemCreate(PoItemBase):
    pass

class PoItemUpdate(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    unit_price: Optional[float] = None
    gst_rate: Optional[float] = None
    amount: Optional[float] = None

class PoItemInDB(PoItemBase):
    id: int
    po_id: int

    class Config:
        from_attributes = True

class PurchaseOrderBase(BaseModel):
    po_number: str
    vendor_id: int
    po_date: str
    delivery_date: Optional[str] = None
    total_amount: float
    cgst_amount: Optional[float] = None
    sgst_amount: Optional[float] = None
    igst_amount: Optional[float] = None
    grn_status: Optional[str] = "Pending"
    is_deleted: int = 0
    payment_terms: Optional[str] = None

class PurchaseOrderCreate(PurchaseOrderBase):
    items: List[PoItemCreate] = []

class PurchaseOrderUpdate(BaseModel):
    po_number: Optional[str] = None
    vendor_id: Optional[int] = None
    po_date: Optional[str] = None
    delivery_date: Optional[str] = None
    total_amount: Optional[float] = None
    cgst_amount: Optional[float] = None
    sgst_amount: Optional[float] = None
    igst_amount: Optional[float] = None
    grn_status: Optional[str] = None
    is_deleted: Optional[int] = None
    payment_terms: Optional[str] = None
    items: Optional[List[PoItemUpdate]] = None

class PurchaseOrderInDB(PurchaseOrderBase):
    id: int

    class Config:
        from_attributes = True