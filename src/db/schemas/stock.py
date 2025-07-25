from pydantic import BaseModel
from typing import Optional

class StockBase(BaseModel):
    product_id: int
    quantity: float
    unit: str
    location: Optional[str] = None
    last_updated: str

class StockCreate(StockBase):
    pass

class StockUpdate(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    location: Optional[str] = None
    last_updated: Optional[str] = None

class StockInDB(StockBase):
    id: int

    class Config:
        from_attributes = True