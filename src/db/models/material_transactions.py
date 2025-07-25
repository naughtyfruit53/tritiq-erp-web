# src/db/models/material_transactions.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .base import Base

class MaterialTransaction(Base):
    __tablename__ = "material_transactions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    doc_number = Column(String, unique=True, nullable=False)
    delivery_challan_number = Column(String)
    type = Column(String, nullable=False)
    date = Column(String, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    purpose = Column(String)
    remarks = Column(String)