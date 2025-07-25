# src/db/models/users.py
from sqlalchemy import Column, Integer, String, Boolean
from .base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'super_admin', 'admin', 'standard_user'
    active = Column(Boolean, default=True)
    must_change_password = Column(Boolean, default=False)