# src/db/models/audit_log.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .base import Base

class AuditLog(Base):
    __tablename__ = "audit_log"
    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String, nullable=False)
    record_id = Column(Integer, nullable=False)
    action = Column(String, nullable=False)  # INSERT, UPDATE, DELETE
    username = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)