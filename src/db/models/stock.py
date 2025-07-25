# src/db/models/stock.py
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from .base import Base

class Stock(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    location = Column(String)
    last_updated = Column(String, nullable=False)