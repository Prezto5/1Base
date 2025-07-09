import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { getProductVariantDetail, getRegionsForProduct } from '@/lib/api';
import ProductCard from '@/components/ProductCard';
import RegionSelector from '@/components/RegionSelector';
import ProductStats from '@/components/ProductStats';
import ProductTags from '@/components/ProductTags';

interface PageProps {
  params: {
    productSlug: string;
    regionSlug: string;
  };
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  try {
    const resolvedParams = await params;
    const productVariant = await getProductVariantDetail(resolvedParams.productSlug, resolvedParams.regionSlug);
    const title = `База ${productVariant.product.base_name} в ${productVariant.region.name_prepositional}`;
    
    return {
      title,
      description: productVariant.product.description || 'База данных HoReCa',
    };
  } catch {
    return {
      title: 'Продукт не найден',
    };
  }
}

export default async function ProductRegionPage({ params }: PageProps) {
  try {
    const resolvedParams = await params;
    
    // Получаем данные параллельно для лучшей производительности
    const [productVariant, regions] = await Promise.all([
      getProductVariantDetail(resolvedParams.productSlug, resolvedParams.regionSlug),
      getRegionsForProduct(resolvedParams.productSlug),
    ]);

    return (
      <div className="min-h-screen bg-gray-50 text-gray-900">
        <div className="container max-w-4xl mx-auto py-8 px-4">
          {/* Селектор региона */}
          <RegionSelector
            regions={regions}
            currentRegionSlug={resolvedParams.regionSlug}
            productSlug={resolvedParams.productSlug}
          />

          {/* Карточка продукта */}
          <ProductCard productVariant={productVariant} />

          {/* Теги */}
          <ProductTags tags={productVariant.product.tags} />

          {/* Статистика */}
          <ProductStats productVariant={productVariant} />
        </div>
      </div>
    );
  } catch (error) {
    console.error('Error loading product data:', error);
    notFound();
  }
} 