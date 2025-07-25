# src/db/models/voucher_columns.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from .base import Base

class VoucherColumn(Base):
    __tablename__ = "voucher_columns"
    id = Column(Integer, primary_key=True, autoincrement=True)
    voucher_type_id = Column(Integer, ForeignKey("voucher_types.id"), nullable=False)
    column_name = Column(String, nullable=False)
    data_type = Column(String, nullable=False)  # 'TEXT', 'INTEGER', 'REAL', 'DATE'
    is_mandatory = Column(Boolean, default=False)
    display_order = Column(Integer, nullable=False)
    is_calculated = Column(Boolean, default=False)
    calculation_logic = Column(String)