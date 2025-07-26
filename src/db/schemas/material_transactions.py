# src/db/schemas/material_transactions.py
from pydantic import BaseModel
from typing import Optional

class MaterialTransactionBase(BaseModel):
    doc_number: str
    type: str
    date: str
    product_id: int
    quantity: float
    purpose: Optional[str] = None
    remarks: Optional[str] = None

class MaterialTransactionCreate(MaterialTransactionBase):
    pass

class MaterialTransactionUpdate(BaseModel):
    doc_number: Optional[str] = None
    type: Optional[str] = None
    date: Optional[str] = None
    product_id: Optional[int] = None
    quantity: Optional[float] = None
    purpose: Optional[str] = None
    remarks: Optional[str] = None

class MaterialTransactionInDB(MaterialTransactionBase):
    id: int

    class Config:
        from_attributes = True