from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, text
from datetime import datetime
from ..models.work_orders import WorkOrder as WorkOrderModel
from ..models.bom import BOM as BOMModel
from ..models.bom_components import BOMComponent as BOMComponentModel
from ..models.stock import Stock
from ..models.material_transactions import MaterialTransaction
from ..models.products import Product
from ..schemas.work_orders import WorkOrderCreate, WorkOrder
from .sequences import get_next_sequence  # Corrected import

async def create_work_order(db: AsyncSession, wo: WorkOrderCreate):
    result = await db.execute(select(BOMModel).where(BOMModel.id == wo.bom_id))
    bom = result.scalars().first()
    if not bom:
        raise ValueError("BOM not found")
    comp_result = await db.execute(select(BOMComponentModel).where(BOMComponentModel.bom_id == bom.id))
    components = comp_result.scalars().all()
    # Check stock
    insufficient = []
    for comp in components:
        required = comp.quantity * wo.quantity
        stock_result = await db.execute(select(Stock).where(Stock.product_id == comp.component_id))
        stock = stock_result.scalars().first()
        available = stock.quantity if stock else 0
        if available < required:
            prod_result = await db.execute(select(Product).where(Product.id == comp.component_id))
            product = prod_result.scalars().first()
            insufficient.append(f"{product.name if product else 'Unknown'}: Need {required}, Available {available}")
    if insufficient:
        raise ValueError("Insufficient stock:\n" + "\n".join(insufficient))
    
    current_time = datetime.now()
    # Fiscal year calculation (assuming April 1 start; e.g., July 2025 -> "2526")
    year = current_time.year
    if current_time.month >= 4:
        fiscal_year = f"{year % 100:02d}{(year + 1) % 100:02d}"
    else:
        fiscal_year = f"{(year - 1) % 100:02d}{year % 100:02d}"
    
    doc_number = await get_next_sequence(db, "WO_OUT", fiscal_year)
    
    # Deduct stock and add transactions
    for comp in components:
        required = comp.quantity * wo.quantity
        stock_result = await db.execute(select(Stock).where(Stock.product_id == comp.component_id))
        stock = stock_result.scalars().first()
        if stock:
            stock.quantity -= required
            stock.last_updated = current_time
        trans = MaterialTransaction(
            doc_number=doc_number,
            type='Out',
            date=current_time,
            product_id=comp.component_id,
            quantity=required,
            purpose='Work Order',
            remarks=f'Work Order BOM ID {wo.bom_id}'
        )
        db.add(trans)
    
    db_wo = WorkOrderModel(
        bom_id=wo.bom_id,
        quantity=wo.quantity,
        status='Open',
        created_at=current_time
    )
    db.add(db_wo)
    await db.commit()
    await db.refresh(db_wo)
    # Add audit log
    await db.execute(
        text("INSERT INTO audit_log (table_name, record_id, action, user, timestamp) VALUES (:table, :id, :action, :user, :timestamp)"),
        {"table": "work_orders", "id": db_wo.id, "action": "INSERT", "user": "system_user", "timestamp": current_time}
    )
    await db.commit()
    return WorkOrder(**db_wo.__dict__)

async def get_open_work_orders(db: AsyncSession):
    wo_result = await db.execute(select(WorkOrderModel).where(WorkOrderModel.status == 'Open'))
    wos = wo_result.scalars().all()
    result = []
    for wo in wos:
        bom_result = await db.execute(select(BOMModel).where(BOMModel.id == wo.bom_id))
        bom = bom_result.scalars().first()
        if bom:
            prod_result = await db.execute(select(Product).where(Product.id == bom.manufactured_product_id))
            product = prod_result.scalars().first()
        else:
            product = None
        result.append({
            "id": wo.id,
            "product_name": product.name if product else "Unknown",
            "quantity": wo.quantity
        })
    return result

async def get_work_orders(db: AsyncSession):
    wo_result = await db.execute(select(WorkOrderModel))
    wos = wo_result.scalars().all()
    result = []
    for wo in wos:
        bom_result = await db.execute(select(BOMModel).where(BOMModel.id == wo.bom_id))
        bom = bom_result.scalars().first()
        if bom:
            prod_result = await db.execute(select(Product).where(Product.id == bom.manufactured_product_id))
            product = prod_result.scalars().first()
        else:
            product = None
        result.append({
            "id": wo.id,
            "product_name": product.name if product else "Unknown",
            "quantity": wo.quantity,
            "status": wo.status
        })
    return result

async def close_work_order(db: AsyncSession, wo_id: int):
    wo_result = await db.execute(select(WorkOrderModel).where(WorkOrderModel.id == wo_id))
    db_wo = wo_result.scalars().first()
    if not db_wo or db_wo.status != 'Open':
        raise ValueError("Invalid or already closed work order")
    bom_result = await db.execute(select(BOMModel).where(BOMModel.id == db_wo.bom_id))
    bom = bom_result.scalars().first()
    if not bom:
        raise ValueError("BOM not found")
    product_id = bom.manufactured_product_id
    prod_result = await db.execute(select(Product).where(Product.id == product_id))
    product = prod_result.scalars().first()
    if not product:
        raise ValueError("Product not found")
    current_time = datetime.now()
    stock_result = await db.execute(select(Stock).where(Stock.product_id == product_id))
    stock = stock_result.scalars().first()
    if stock:
        stock.quantity += db_wo.quantity
        stock.last_updated = current_time
    else:
        new_stock = Stock(
            product_id=product_id,
            quantity=db_wo.quantity,
            unit=product.unit,
            last_updated=current_time
        )
        db.add(new_stock)
    db_wo.status = 'Closed'
    db_wo.closed_at = current_time
    await db.commit()
    # Add audit log
    await db.execute(
        text("INSERT INTO audit_log (table_name, record_id, action, user, timestamp) VALUES (:table, :id, :action, :user, :timestamp)"),
        {"table": "work_orders", "id": db_wo.id, "action": "UPDATE", "user": "system_user", "timestamp": current_time}
    )
    await db.commit()
    return WorkOrder(**db_wo.__dict__)