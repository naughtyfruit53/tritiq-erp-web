# src/db/schemas/cn_items.py
from pydantic import BaseModel
from typing import Optional

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