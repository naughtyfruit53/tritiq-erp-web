from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from ..models.material_transactions import MaterialTransaction
from ..models.products import Product

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