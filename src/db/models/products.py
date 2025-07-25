# src/db/models/products.py
from sqlalchemy import Column, Integer, String, Float, Boolean
from .base import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    hsn_code = Column(String)
    unit = Column(String, nullable=False)
    unit_price = Column(Float, nullable=False)
    gst_rate = Column(Float, nullable=False)
    is_gst_inclusive = Column(String, nullable=False)  # 'Inclusive' or 'Exclusive'
    reorder_level = Column(Integer, nullable=False)
    description = Column(String)
    is_manufactured = Column(Boolean, default=False)