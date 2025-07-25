from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy import select, text
from ..models.bom import BOM as BOMModel
from ..models.bom_components import BOMComponent as BOMComponentModel
from ..models.products import Product
from ..schemas.bom import BOMCreate, BOM, BOMComponent

async def create_bom(db: AsyncSession, bom: BOMCreate):
    db_bom = BOMModel(
        manufactured_product_id=bom.manufactured_product_id,
        created_at=datetime.now()
    )
    db.add(db_bom)
    await db.commit()
    await db.refresh(db_bom)
    for comp in bom.components:
        db_comp = BOMComponentModel(
            bom_id=db_bom.id,
            component_id=comp.component_id,
            quantity=comp.quantity
        )
        db.add(db_comp)
    await db.commit()
    # Add audit log (raw SQL)
    await db.execute(
        text("INSERT INTO audit_log (table_name, record_id, action, user, timestamp) VALUES (:table, :id, :action, :user, :timestamp)"),
        {"table": "bom", "id": db_bom.id, "action": "INSERT", "user": "system_user", "timestamp": datetime.now()}
    )
    await db.commit()
    # Return with components (fetch components asynchronously)
    result = await db.execute(select(BOMComponentModel).where(BOMComponentModel.bom_id == db_bom.id))
    components = result.scalars().all()
    return BOM(
        id=db_bom.id,
        manufactured_product_id=db_bom.manufactured_product_id,
        created_at=db_bom.created_at,
        components=[BOMComponent(**c.__dict__) for c in components]
    )

async def get_boms(db: AsyncSession):
    result = await db.execute(select(BOMModel))
    boms = result.scalars().all()
    result_list = []
    for b in boms:
        product_result = await db.execute(select(Product).where(Product.id == b.manufactured_product_id))
        product = product_result.scalars().first()
        result_list.append({
            "id": b.id,
            "product_name": product.name if product else "Unknown"
        })
    return result_list