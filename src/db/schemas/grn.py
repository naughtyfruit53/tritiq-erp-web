from pydantic import BaseModel
from typing import List, Optional

class GrnItemBase(BaseModel):
    product_id: int
    po_item_id: int
    quantity: float
    accepted_quantity: float
    rejected_quantity: float
    unit: str
    unit_price: float
    total_cost: float
    remarks: Optional[str] = None

class GrnItemCreate(GrnItemBase):
    pass

class GrnItemUpdate(BaseModel):
    product_id: Optional[int] = None
    po_item_id: Optional[int] = None
    quantity: Optional[float] = None
    accepted_quantity: Optional[float] = None
    rejected_quantity: Optional[float] = None
    unit: Optional[str] = None
    unit_price: Optional[float] = None
    total_cost: Optional[float] = None
    remarks: Optional[str] = None

class GrnItemInDB(GrnItemBase):
    id: int
    grn_id: int

    class Config:
        from_attributes = True

class GrnBase(BaseModel):
    po_id: int
    grn_number: str
    description: Optional[str] = None
    created_at: str
    status: str

class GrnCreate(GrnBase):
    items: List[GrnItemCreate] = []

class GrnUpdate(BaseModel):
    po_id: Optional[int] = None
    grn_number: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[str] = None
    status: Optional[str] = None
    items: Optional[List[GrnItemUpdate]] = None

class GrnInDB(GrnBase):
    id: int
    items: List[GrnItemInDB] = []

    class Config:
        from_attributes = True