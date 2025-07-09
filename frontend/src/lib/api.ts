import { ProductVariantDetail, RegionInfo } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

async function fetchAPI<T>(endpoint: string): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  try {
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new ApiError(response.status, `HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new Error(`Failed to fetch ${endpoint}: ${error}`);
  }
}

export async function getProductVariantDetail(
  productSlug: string, 
  regionSlug: string
): Promise<ProductVariantDetail> {
  return fetchAPI<ProductVariantDetail>(`/api/v1/products/${productSlug}/${regionSlug}`);
}

export async function getRegionsForProduct(productSlug: string): Promise<RegionInfo[]> {
  return fetchAPI<RegionInfo[]>(`/api/v1/products/${productSlug}/regions`);
} 