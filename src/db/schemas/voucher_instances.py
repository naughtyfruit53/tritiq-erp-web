from datetime import datetime
from typing import Dict, Optional
from pydantic import BaseModel

class VoucherInstanceBase(BaseModel):
    voucher_number: str
    data_json: Dict  # Parsed as dict in API
    module_name: str
    record_id: int = 0

class VoucherInstanceCreate(VoucherInstanceBase):
    voucher_type_id: int

class VoucherInstanceUpdate(BaseModel):
    voucher_number: Optional[str] = None
    data_json: Optional[Dict] = None
    module_name: Optional[str] = None
    record_id: Optional[int] = None

class VoucherInstance(VoucherInstanceBase):
    id: int
    voucher_type_id: int
    created_at: datetime

    model_config = {"from_attributes": True}  # For Pydantic v2