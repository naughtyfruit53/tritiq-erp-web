# src/db/schemas/products.py
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    hsn_code: str | None = None
    unit: str
    unit_price: float
    gst_rate: float
    is_gst_inclusive: str  # 'Inclusive' or 'Exclusive'
    reorder_level: int
    description: str | None = None
    is_manufactured: bool = False

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str | None = None
    hsn_code: str | None = None
    unit: str | None = None
    unit_price: float | None = None
    gst_rate: float | None = None
    is_gst_inclusive: str | None = None
    reorder_level: int | None = None
    description: str | None = None
    is_manufactured: bool | None = None

class ProductInDB(ProductBase):
    id: int

    class Config:
        from_attributes = True