from pydantic import BaseModel
from typing import Optional

class DocSequenceBase(BaseModel):
    doc_type: str
    fiscal_year: str
    last_sequence: int

class DocSequenceCreate(DocSequenceBase):
    pass

class DocSequenceUpdate(BaseModel):
    last_sequence: Optional[int] = None

class DocSequenceInDB(DocSequenceBase):
    class Config:
        from_attributes = True