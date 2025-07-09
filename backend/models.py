from sqlalchemy import Column, Integer, String, Text, Boolean, Numeric, ForeignKey, SmallInteger, UniqueConstraint, TIMESTAMP, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    base_name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    image_url = Column(String(255))
    tags = Column(Text)
    is_top = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")

class Region(Base):
    __tablename__ = "regions"
    id = Column(Integer, primary_key=True)
    name_nominative = Column(String(100), nullable=False)
    name_genitive = Column(String(100), nullable=False)
    name_prepositional = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False, unique=True)

    variants = relationship("ProductVariant", back_populates="region")

class ProductVariant(Base):
    __tablename__ = "product_variants"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id", ondelete="RESTRICT"), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    total_companies = Column(Integer, default=0, nullable=False)
    companies_with_email = Column(Integer, default=0, nullable=False)
    companies_with_phone = Column(Integer, default=0, nullable=False)
    companies_with_site = Column(Integer, default=0, nullable=False)
    companies_with_address = Column(Integer, default=0, nullable=False)
    companies_with_activity = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True)

    product = relationship("Product", back_populates="variants")
    region = relationship("Region", back_populates="variants")

    __table_args__ = (UniqueConstraint("product_id", "region_id", name="uix_product_region"),)

class CmsPage(Base):
    __tablename__ = "cms_pages"
    id = Column(Integer, primary_key=True)
    page_name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    count = Column(Integer)
    price = Column(Numeric(10, 2))
    demo_url = Column(String(255)) 