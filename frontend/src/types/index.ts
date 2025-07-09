export interface Region {
  name_nominative: string;
  name_genitive: string;
  name_prepositional: string;
  slug: string;
}

export interface ProductInfo {
  base_name: string;
  slug: string;
}

export interface Product {
  base_name: string;
  slug: string;
  description: string | null;
  image_url: string | null;
  tags: string | null;
  is_top: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProductVariantDetail {
  id: number;
  price: number;
  total_companies: number;
  companies_with_email: number;
  companies_with_phone: number;
  companies_with_site: number;
  companies_with_address: number;
  companies_with_activity: number;
  is_active: boolean;
  product: Product;
  region: Region;
}

export interface RegionInfo {
  name_nominative: string;
  slug: string;
  price: number;
} 