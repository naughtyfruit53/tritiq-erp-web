# src/db/models/cn_items.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .base import Base

class CnItem(Base):
    __tablename__ = "cn_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cn_id = Column(Integer, ForeignKey("credit_notes.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    unit_price = Column(Float, nullable=False)
    gst_rate = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)