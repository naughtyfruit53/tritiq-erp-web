from sqlalchemy import Column, Integer, String, Float, ForeignKey
from datetime import datetime
from .base import Base

class SalesOrder(Base):
    __tablename__ = "sales_orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sales_order_number = Column(String, unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    sales_order_date = Column(String, nullable=False)
    delivery_date = Column(String)
    payment_terms = Column(String)
    total_amount = Column(Float, nullable=False)
    cgst_amount = Column(Float)
    sgst_amount = Column(Float)
    igst_amount = Column(Float)
    created_at = Column(String, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at = Column(String, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    is_deleted = Column(Integer, default=0)
    voucher_type_id = Column(Integer, ForeignKey("voucher_types.id"))