from pydantic import BaseModel
from typing import List, Optional

class PurchaseInvItemBase(BaseModel):
    product_id: int
    quantity: float
    unit: str
    unit_price: float
    gst_rate: float
    amount: float

class PurchaseInvItemCreate(PurchaseInvItemBase):
    pass

class PurchaseInvItemUpdate(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    unit_price: Optional[float] = None
    gst_rate: Optional[float] = None
    amount: Optional[float] = None

class PurchaseInvItemInDB(PurchaseInvItemBase):
    id: int
    pur_inv_id: int

    class Config:
        from_attributes = True

class PurchaseInvBase(BaseModel):
    pur_inv_number: str
    invoice_number: str
    invoice_date: str
    grn_id: Optional[int] = None
    po_id: int
    vendor_id: int
    pur_inv_date: str
    total_amount: float
    cgst_amount: Optional[float] = None
    sgst_amount: Optional[float] = None
    igst_amount: Optional[float] = None
    voucher_type_id: Optional[int] = None

class PurchaseInvCreate(PurchaseInvBase):
    items: List[PurchaseInvItemCreate] = []

class PurchaseInvUpdate(BaseModel):
    pur_inv_number: Optional[str] = None
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    grn_id: Optional[int] = None
    po_id: Optional[int] = None
    vendor_id: Optional[int] = None
    pur_inv_date: Optional[str] = None
    total_amount: Optional[float] = None
    cgst_amount: Optional[float] = None
    sgst_amount: Optional[float] = None
    igst_amount: Optional[float] = None
    voucher_type_id: Optional[int] = None
    items: Optional[List[PurchaseInvItemUpdate]] = None

class PurchaseInvInDB(PurchaseInvBase):
    id: int
    created_at: str
    items: List[PurchaseInvItemInDB] = []

    class Config:
        from_attributes = True