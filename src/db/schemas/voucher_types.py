# src/db/schemas/voucher_types.py
from pydantic import BaseModel

class VoucherTypeBase(BaseModel):
    name: str
    is_default: bool = False
    module_name: str
    category: str = "internal"

class VoucherTypeCreate(VoucherTypeBase):
    pass

class VoucherTypeUpdate(BaseModel):
    name: str | None = None
    is_default: bool | None = None
    module_name: str | None = None
    category: str | None = None

class VoucherTypeInDB(VoucherTypeBase):
    id: int

    class Config:
        from_attributes = True