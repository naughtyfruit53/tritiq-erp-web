# src/db/schemas/voucher_columns.py
from pydantic import BaseModel

class VoucherColumnBase(BaseModel):
    voucher_type_id: int
    column_name: str
    data_type: str
    is_mandatory: bool = False
    display_order: int
    is_calculated: bool = False
    calculation_logic: str | None = None

class VoucherColumnCreate(VoucherColumnBase):
    pass

class VoucherColumnUpdate(BaseModel):
    column_name: str | None = None
    data_type: str | None = None
    is_mandatory: bool | None = None
    display_order: int | None = None
    is_calculated: bool | None = None
    calculation_logic: str | None = None

class VoucherColumnInDB(VoucherColumnBase):
    id: int

    class Config:
        from_attributes = True