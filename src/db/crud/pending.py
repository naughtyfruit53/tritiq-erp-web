# src/db/crud/pending.py
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Tuple

async def get_pending(db: AsyncSession) -> List[Tuple]:
    query = text("""
        SELECT mt.doc_number, mt.type, mt.date, p.name, mt.quantity
        FROM material_transactions mt
        JOIN products p ON mt.product_id = p.id
        WHERE mt.type IN ('Purchase Order', 'Goods Receipt Note')
        ORDER BY mt.date DESC
    """)
    result = await db.execute(query)
    return result.fetchall()

async def filter_pending(db: AsyncSession, search_text: str) -> List[Tuple]:
    query = text("""
        SELECT mt.doc_number, mt.type, mt.date, p.name, mt.quantity
        FROM material_transactions mt
        JOIN products p ON mt.product_id = p.id
        WHERE mt.type IN ('Purchase Order', 'Goods Receipt Note')
        AND (p.name ILIKE :search_text OR mt.doc_number ILIKE :search_text)
        ORDER BY mt.date DESC
    """)
    result = await db.execute(query, {"search_text": f"%{search_text}%"})
    return result.fetchall()