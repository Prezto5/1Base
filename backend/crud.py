from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, load_only
from sqlalchemy import func
from models import Product, Region, ProductVariant
from typing import Optional, List
from fastapi import HTTPException, status

async def get_all_products(session: AsyncSession):
    """Получает список всех продуктов с загрузкой только необходимых полей"""
    query = select(Product).options(load_only(Product.base_name, Product.slug))
    result = await session.execute(query)
    products = result.scalars().all()
    return products

async def get_product_variant_detail(session: AsyncSession, product_slug: str, region_slug: str):
    query = (
        select(ProductVariant)
        .join(ProductVariant.product)
        .join(ProductVariant.region)
        .options(
            joinedload(ProductVariant.product),
            joinedload(ProductVariant.region)
        )
        .where(Product.slug == product_slug, Region.slug == region_slug)
    )
    result = await session.execute(query)
    variant = result.scalars().first()
    if not variant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product or region not found")
    return variant

async def get_regions_for_product(session: AsyncSession, product_slug: str):
    # Сначала найдем продукт
    product_query = select(Product).where(Product.slug == product_slug)
    product_result = await session.execute(product_query)
    product = product_result.scalars().first()
    
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with slug '{product_slug}' not found")
    
    # Затем найдем все варианты этого продукта с регионами
    query = (
        select(ProductVariant)
        .options(joinedload(ProductVariant.region))
        .where(ProductVariant.product_id == product.id, ProductVariant.is_active == True)
    )
    result = await session.execute(query)
    variants = result.scalars().all()
    
    if not variants:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No active variants found for product '{product_slug}'")
    
    return variants 