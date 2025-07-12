import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { getProductVariantDetail, getRegionsForProduct, getAllProducts } from '@/lib/api';
import ProductView from '@/components/ProductView';

// Принудительно делаем страницы динамическими для получения свежих данных
export const dynamic = 'force-dynamic';

interface PageProps {
  params: Promise<{
    productSlug: string;
    regionSlug: string;
  }>;
}

// Генерация статических параметров для всех страниц продуктов
export async function generateStaticParams() {
  try {
    // Получаем все продукты
    const products = await getAllProducts();
    
    // Для каждого продукта получаем все его регионы
    const params = await Promise.all(
      products.map(async (product) => {
        try {
          const regions = await getRegionsForProduct(product.slug);
          return regions.map((region) => ({
            productSlug: product.slug,
            regionSlug: region.slug,
          }));
        } catch (error) {
          console.error(`Error getting regions for product ${product.slug}:`, error);
          return [];
        }
      })
    );
    
    // Флэттенинг массива массивов в один массив
    const staticParams = params.flat();
    
    console.log(`Generating ${staticParams.length} static pages`);
    return staticParams;
  } catch (error) {
    console.error('Error generating static params:', error);
    // Возвращаем базовые страницы если API недоступен
    return [
      { productSlug: 'baza-horeca', regionSlug: 'russia' },
      { productSlug: 'baza-prodavtsov-ozon', regionSlug: 'russia' }
    ];
  }
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  try {
    const resolvedParams = await params;
    const productVariant = await getProductVariantDetail(resolvedParams.productSlug, resolvedParams.regionSlug);
    
    return {
      title: productVariant.title || `База ${productVariant.product.base_name} в ${productVariant.region.name_prepositional}`,
      description: productVariant.description || 'База данных HoReCa',
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

    // Генерируем полный URL для JSON-LD
    const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://ваш-сайт.ru';
    const fullUrl = `${baseUrl}/${resolvedParams.productSlug}/${resolvedParams.regionSlug}`;

    // Создаем объект JSON-LD микроразметки
    const jsonLd = {
      "@context": "https://schema.org/",
      "@type": "Product",
      "name": `${productVariant.product.base_name} в ${productVariant.region.name_prepositional}`,
      "description": productVariant.description || `База данных ${productVariant.product.base_name} для ${productVariant.region.name_genitive}`,
      "image": productVariant.product.image_url,
      "sku": `RU-${productVariant.product.id}-${productVariant.region.id}`,
      "offers": {
        "@type": "Offer",
        "url": fullUrl,
        "priceCurrency": "RUB",
        "price": productVariant.price,
        "availability": productVariant.is_active ? "https://schema.org/InStock" : "https://schema.org/OutOfStock",
        "seller": {
          "@type": "Organization",
          "name": "1Base"
        }
      },
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": productVariant.ratingValue,
        "reviewCount": productVariant.reviewCount,
        "bestRating": 5,
        "worstRating": 1
      },
      "brand": {
        "@type": "Brand",
        "name": "1Base"
      }
    };

    return (
      <>
        {/* JSON-LD микроразметка */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
        
        {/* Используем новый ProductView компонент с real-time обновлениями */}
        <ProductView 
          initialVariant={productVariant}
          regions={regions}
          productSlug={resolvedParams.productSlug}
          regionSlug={resolvedParams.regionSlug}
        />
      </>
    );
  } catch (error) {
    console.error('Error loading product data:', error);
    notFound();
  }
} 