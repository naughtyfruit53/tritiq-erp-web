from pydantic import BaseModel
from typing import Optional

class RejectionBase(BaseModel):
    grn_item_id: int
    reason: str
    quantity: float
    rejected_date: str
    remarks: Optional[str] = None

class RejectionCreate(RejectionBase):
    pass

class RejectionUpdate(BaseModel):
    grn_item_id: Optional[int] = None
    reason: Optional[str] = None
    quantity: Optional[float] = None
    rejected_date: Optional[str] = None
    remarks: Optional[str] = None

class RejectionInDB(RejectionBase):
    id: int

    class Config:
        from_attributes = True