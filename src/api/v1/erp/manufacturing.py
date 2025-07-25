from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ....db.session import get_db
from ....db.models.products import Product
from ....db.schemas.bom import BOMCreate, BOM
from ....db.schemas.work_orders import WorkOrderCreate, WorkOrder
from ....db.crud.bom import create_bom, get_boms
from ....db.crud.work_orders import create_work_order, get_open_work_orders, close_work_order

router = APIRouter(
    prefix="/manufacturing",
    tags=["manufacturing"],
    responses={404: {"description": "Not found"}},
)

@router.get("/manufactured-products")
async def get_manufactured_products(db: AsyncSession = Depends(get_db)):
    """
    Fetch manufactured products (for BOM selection).
    """
    result = await db.execute(select(Product).where(Product.is_manufactured == 1).order_by(Product.name))
    products = result.scalars().all()
    return [{"id": p.id, "name": p.name} for p in products]

@router.get("/component-products")
async def get_component_products(db: AsyncSession = Depends(get_db)):
    """
    Fetch non-manufactured products (components for BOM).
    """
    result = await db.execute(select(Product).where(Product.is_manufactured == 0).order_by(Product.name))
    products = result.scalars().all()
    return [{"id": p.id, "name": p.name} for p in products]

@router.post("/bom", response_model=BOM)
async def create_bom_endpoint(bom: BOMCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new Bill of Materials (BOM).
    """
    try:
        return await create_bom(db, bom)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/boms")
async def get_boms_endpoint(db: AsyncSession = Depends(get_db)):
    """
    Fetch all BOMs with product names (for work order selection).
    """
    return await get_boms(db)

@router.post("/work-order", response_model=WorkOrder)
async def create_work_order_endpoint(wo: WorkOrderCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new work order, check/deduct stock, and log transactions.
    """
    try:
        return await create_work_order(db, wo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/open-work-orders")
async def get_open_work_orders_endpoint(db: AsyncSession = Depends(get_db)):
    """
    Fetch open work orders with details.
    """
    return await get_open_work_orders(db)

@router.post("/close-work-order/{wo_id}", response_model=WorkOrder)
async def close_work_order_endpoint(wo_id: int, db: AsyncSession = Depends(get_db)):
    """
    Close a work order, update stock, and log.
    """
    try:
        return await close_work_order(db, wo_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")