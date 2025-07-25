# src/db/models/doc_sequences.py
from sqlalchemy import Column, String, Integer
from .base import Base

class DocSequence(Base):
    __tablename__ = "doc_sequences"
    doc_type = Column(String, primary_key=True)
    fiscal_year = Column(String, primary_key=True)
    last_sequence = Column(Integer, nullable=False)