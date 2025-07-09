from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RegionInfo(BaseModel):
    name_nominative: str
    slug: str
    price: float

class ProductRating(BaseModel):
    average_rating: float
    reviews_count: int

class ProductBase(BaseModel):
    base_name: str
    slug: str
    description: Optional[str]
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
    image_url: Optional[str]
    total_companies: int
    companies_with_email: int
    companies_with_phone: int
    companies_with_site: int
    companies_with_address: int
    companies_with_activity: int
    is_active: bool
    product: ProductBase
    region: RegionBase

    class Config:
        from_attributes = True 