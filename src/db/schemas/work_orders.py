from datetime import datetime
from pydantic import BaseModel

class WorkOrderCreate(BaseModel):
    bom_id: int
    quantity: int

class WorkOrder(WorkOrderCreate):
    id: int
    status: str
    created_at: datetime
    closed_at: datetime | None = None