from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RegionInfo(BaseModel):
    name_nominative: str
    slug: str
    price: float

class ProductInfo(BaseModel):
    base_name: str
    slug: str

class ProductBase(BaseModel):
    base_name: str
    slug: str
    image_url: Optional[str]
    tags: Optional[str]
    is_top: bool
    created_at: datetime
    updated_at: datetime

class RegionBase(BaseModel):
    name_nominative: str
    name_genitive: str
    name_prepositional: str
    slug: str

class ProductVariantDetail(BaseModel):
    id: int
    price: float
    total_companies: int
    companies_with_email: int
    companies_with_phone: int
    companies_with_site: int
    companies_with_address: int
    companies_with_activity: int
    is_active: bool
    # SEO fields moved from Product to ProductVariant
    title: Optional[str]
    description: Optional[str]
    seo_text: Optional[str]
    product: ProductBase
    region: RegionBase

    class Config:
        from_attributes = True 