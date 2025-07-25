# src/db/models/company_details.py
from sqlalchemy import Column, Integer, String
from .base import Base

class CompanyDetail(Base):
    __tablename__ = "company_details"
    id = Column(Integer, primary_key=True)
    company_name = Column(String, nullable=False)
    address1 = Column(String, nullable=False)
    address2 = Column(String)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    pin = Column(String, nullable=False)
    state_code = Column(String, nullable=False)
    gst_no = Column(String)
    pan_no = Column(String)
    contact_no = Column(String, nullable=False)
    email = Column(String)
    logo_path = Column(String)