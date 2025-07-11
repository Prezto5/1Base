import { ProductVariantDetail } from '@/types';
import Image from 'next/image';
import { formatNumber } from '@/lib/utils';
import Rating from './Rating';

interface ProductCardProps {
  productVariant: ProductVariantDetail;
}

export default function ProductCard({ productVariant }: ProductCardProps) {
  const { product, region, price, ratingValue, reviewCount } = productVariant;

  return (
    <div className="container max-w-4xl mx-auto my-8 bg-white rounded-xl shadow-lg p-6 text-gray-900">
      <div className="flex flex-col lg:flex-row gap-6">
        {/* Левая колонка - изображение */}
        <div className="lg:w-80 flex-shrink-0">
          <div className="relative">
            {product.is_top && (
              <span className="absolute top-4 left-4 bg-yellow-400 text-white font-bold px-3 py-1 rounded text-sm z-10">
                ТОП
              </span>
            )}
            {product.image_url ? (
              <Image
                src={product.image_url}
                alt={product.base_name}
                width={320}
                height={240}
                className="w-full rounded-xl"
              />
            ) : (
              <div className="w-full h-60 bg-gray-200 rounded-xl flex items-center justify-center">
                <span className="text-gray-500">Нет изображения</span>
              </div>
            )}
          </div>
          <div className="text-center mt-3">
            <h2 className="text-xl font-bold text-gray-900">{region.name_nominative.toUpperCase()}</h2>
            <Rating ratingValue={ratingValue} reviewCount={reviewCount} />
          </div>
        </div>

        {/* Правая колонка - информация */}
        <div className="flex-1">
          <h1 className="text-2xl font-bold mb-2 text-gray-900">{product.base_name}</h1>
          <div className="text-3xl font-bold text-green-600 mb-4">
            {formatNumber(price, ' руб.')}
          </div>

          {/* SEO текст блок */}
          {productVariant.seo_text && (
            <div className="mt-4 mb-6 p-4 bg-gray-50 rounded-lg">
              <p className="text-gray-700 text-sm leading-relaxed">{productVariant.seo_text}</p>
            </div>
          )}

          <div className="bg-gray-50 rounded-lg p-4 mb-4 text-gray-900">
            <div className="mb-2">
              Всего компаний в базе: <strong>
                {formatNumber(productVariant.total_companies, ' шт.')}
              </strong>
            </div>
          </div>

          <ul className="space-y-2 mb-6 text-gray-900">
            <li>✓ 6 месяцев бесплатного обновления</li>
            <li><strong>База обновлена:</strong> {new Date(product.updated_at).toLocaleDateString('ru-RU')}</li>
            <li><strong>Наш телефон:</strong> <a href="tel:88007752912" className="text-blue-600">8 800 775-29-12</a></li>
          </ul>

          <div className="flex gap-3">
            <button className="bg-green-500 hover:bg-green-600 text-white px-8 py-3 rounded-lg font-medium transition-colors">
              Скачать демо
            </button>
            <button className="bg-green-500 hover:bg-green-600 text-white px-8 py-3 rounded-lg font-medium transition-colors">
              Оплатить
            </button>
          </div>
        </div>
      </div>
    </div>
  );
} 