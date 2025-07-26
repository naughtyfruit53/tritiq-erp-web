# src/db/crud/material_transactions.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from ..models.material_transactions import MaterialTransaction
from ..models.products import Product
from ..schemas.material_transactions import MaterialTransactionCreate  # Assume schema exists

async def get_material_transactions(db: AsyncSession, type: Optional[str] = None) -> List[dict]:
    query = select(MaterialTransaction)
    if type:
        query = query.where(MaterialTransaction.type == type)
    result = await db.execute(query)
    trans = result.scalars().all()
    enriched = []
    for t in trans:
        prod_result = await db.execute(select(Product).where(Product.id == t.product_id))
        product = prod_result.scalars().first()
        enriched.append({
            "id": t.id,
            "doc_number": t.doc_number,
            "type": t.type,
            "date": t.date,
            "product_name": product.name if product else "Unknown",
            "quantity": t.quantity,
            "purpose": t.purpose,
            "remarks": t.remarks
        })
    return enriched

async def create_material_transaction(db: AsyncSession, transaction: MaterialTransactionCreate) -> MaterialTransaction:
    db_transaction = MaterialTransaction(**transaction.dict())
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction