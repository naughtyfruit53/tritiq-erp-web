from datetime import datetime
from pydantic import BaseModel
from typing import List

class BOMComponentCreate(BaseModel):
    component_id: int
    quantity: int

class BOMCreate(BaseModel):
    manufactured_product_id: int
    components: List[BOMComponentCreate]

class BOM(BOMCreate):
    id: int
    created_at: datetime

class BOMComponent(BOMComponentCreate):
    id: int
    bom_id: int