# src/db/models/sales_invoices.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .base import Base

class SalesInvoice(Base):
    __tablename__ = "sales_invoices"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sales_inv_number = Column(String, unique=True, nullable=False)
    invoice_date = Column(String)
    sales_order_id = Column(Integer, ForeignKey("sales_orders.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    cgst_amount = Column(Float)
    sgst_amount = Column(Float)
    igst_amount = Column(Float)
    created_at = Column(String, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    voucher_type_id = Column(Integer, ForeignKey("voucher_types.id"))
    voucher_data = Column(String)