# src/db/schemas/users.py
from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    role: str
    active: bool = True
    must_change_password: bool = False

class UserCreate(UserBase):
    password: str  # Required only during creation

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    active: Optional[bool] = None
    must_change_password: Optional[bool] = None

class UserInDB(UserBase):
    id: int

    class Config:
        orm_mode = True