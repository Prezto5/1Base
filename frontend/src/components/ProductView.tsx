'use client';

import React from 'react';
import { ProductVariantDetail, RegionInfo } from '@/types';
import { useVariantWithRealtime } from '@/context/RealtimeDataContext';
import ProductCard from './ProductCard';
import RegionSelector from './RegionSelector';
import ProductStats from './ProductStats';
import ProductTags from './ProductTags';

interface ProductViewProps {
  initialVariant: ProductVariantDetail;
  regions: RegionInfo[];
  productSlug: string;
  regionSlug: string;
}

export default function ProductView({ 
  initialVariant, 
  regions, 
  productSlug, 
  regionSlug 
}: ProductViewProps) {
  // Получаем актуальный вариант продукта с real-time обновлениями
  const currentVariant = useVariantWithRealtime(initialVariant);

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <div className="container max-w-4xl mx-auto py-8 px-4">
        {/* Селектор региона */}
        <RegionSelector
          regions={regions}
          currentRegionSlug={regionSlug}
          productSlug={productSlug}
        />

        {/* Карточка продукта с актуальными данными */}
        <ProductCard productVariant={currentVariant} />

        {/* Теги */}
        <ProductTags tags={currentVariant.product.tags} />

        {/* Статистика с актуальными данными */}
        <ProductStats productVariant={currentVariant} />
      </div>
    </div>
  );
} 