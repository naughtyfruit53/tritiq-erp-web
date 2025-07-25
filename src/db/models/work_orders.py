# src/db/models/work_orders.py
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from .base import Base

class WorkOrder(Base):
    __tablename__ = "work_orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    bom_id = Column(Integer, ForeignKey("bom.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    status = Column(String, nullable=False, default='Open')
    created_at = Column(DateTime, nullable=False)
    closed_at = Column(DateTime)