from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base

class Grn(Base):
    __tablename__ = "grn"
    id = Column(Integer, primary_key=True, autoincrement=True)
    po_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False)
    grn_number = Column(String, unique=True, nullable=False)
    description = Column(String)
    created_at = Column(String, nullable=False)
    status = Column(String, nullable=False)