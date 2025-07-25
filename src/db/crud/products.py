# src/db/crud/products.py
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.products import Product
from src.db.schemas.products import ProductCreate, ProductUpdate
from typing import List

async def create_product(db: AsyncSession, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def get_products(db: AsyncSession) -> List[Product]:
    result = await db.execute(select(Product))
    return result.scalars().all()

async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).where(Product.id == product_id))
    return result.scalar_one_or_none()

async def update_product(db: AsyncSession, product_id: int, product_update: ProductUpdate):
    stmt = update(Product).where(Product.id == product_id).values(**product_update.dict(exclude_unset=True))
    await db.execute(stmt)
    await db.commit()
    return await get_product(db, product_id)

async def delete_product(db: AsyncSession, product_id: int):
    stmt = delete(Product).where(Product.id == product_id)
    await db.execute(stmt)
    await db.commit()