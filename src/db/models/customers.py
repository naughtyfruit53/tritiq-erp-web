# src/db/models/customers.py
from sqlalchemy import Column, Integer, String
from .base import Base

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    contact_no = Column(String, nullable=False)
    address1 = Column(String, nullable=False)
    address2 = Column(String)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    state_code = Column(String, nullable=False)
    pin = Column(String, nullable=False)
    gst_no = Column(String)
    pan_no = Column(String)
    email = Column(String)