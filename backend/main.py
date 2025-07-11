from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
import crud
import schemas
from typing import List
import random

app = FastAPI()

# Настройка CORS для работы с Next.js фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация данных вынесена в отдельный скрипт seed.py
# Для первой настройки запустите: python backend/seed.py

# ВАЖНО: Более специфичные маршруты должны быть определены ПЕРЕД более общими!

@app.get("/api/v1/products", response_model=List[schemas.ProductInfo])
async def get_all_products(session: AsyncSession = Depends(get_session)):
    """Получает список всех продуктов"""
    products = await crud.get_all_products(session)
    return [
        schemas.ProductInfo(
            base_name=product.base_name,
            slug=product.slug
        )
        for product in products
    ]

@app.get("/api/v1/products/{product_slug}/regions", response_model=List[schemas.RegionInfo])
async def get_regions_for_product(product_slug: str, session: AsyncSession = Depends(get_session)):
    variants = await crud.get_regions_for_product(session, product_slug)
    
    # Сортируем регионы: "Россия" первой, остальные в алфавитном порядке
    russia_variant = None
    other_variants = []
    
    for variant in variants:
        if variant.region.slug == 'russia':
            russia_variant = variant
        else:
            other_variants.append(variant)
    
    # Сортируем остальные регионы в алфавитном порядке
    other_variants.sort(key=lambda v: v.region.name_nominative)
    
    # Формируем итоговый список
    sorted_variants = []
    if russia_variant:
        sorted_variants.append(russia_variant)
    sorted_variants.extend(other_variants)
    
    regions = [
        schemas.RegionInfo(
            name_nominative=variant.region.name_nominative,
            slug=variant.region.slug,
            price=float(variant.price)
        )
        for variant in sorted_variants
    ]
    return regions

@app.get("/api/v1/products/{product_slug}/{region_slug}", response_model=schemas.ProductVariantDetail)
async def get_product_variant_detail(product_slug: str, region_slug: str, session: AsyncSession = Depends(get_session)):
    variant = await crud.get_product_variant_detail(session, product_slug, region_slug)

    # Generate stable random rating data based on variant ID
    random.seed(variant.id)
    rating_value = round(random.uniform(4.7, 5.0), 1)
    review_count = random.randint(30, 300)

    return schemas.ProductVariantDetail(
        id=variant.id,
        price=float(variant.price),
        total_companies=variant.total_companies,
        companies_with_email=variant.companies_with_email,
        companies_with_phone=variant.companies_with_phone,
        companies_with_site=variant.companies_with_site,
        companies_with_address=variant.companies_with_address,
        companies_with_activity=variant.companies_with_activity,
        is_active=variant.is_active,
        # SEO fields now come from variant instead of product
        title=variant.title,
        description=variant.description,
        seo_text=variant.seo_text,
        # Generated rating data
        ratingValue=rating_value,
        reviewCount=review_count,
        product=schemas.ProductBase(
            id=variant.product.id,
            base_name=variant.product.base_name,
            slug=variant.product.slug,
            image_url=variant.product.image_url,
            tags=variant.product.tags,
            is_top=variant.product.is_top,
            created_at=variant.product.created_at,
            updated_at=variant.product.updated_at,
        ),
        region=schemas.RegionBase(
            id=variant.region.id,
            name_nominative=variant.region.name_nominative,
            name_genitive=variant.region.name_genitive,
            name_prepositional=variant.region.name_prepositional,
            slug=variant.region.slug,
        ),
    )

# Статические файлы теперь обрабатываются Next.js фронтендом 