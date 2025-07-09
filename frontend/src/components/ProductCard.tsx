import { ProductVariantDetail } from '@/types';
import Image from 'next/image';
import CountUp from './CountUp';

interface ProductCardProps {
  productVariant: ProductVariantDetail;
}

export default function ProductCard({ productVariant }: ProductCardProps) {
  const { product, region, price, image_url } = productVariant;

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
            {image_url ? (
              <Image
                src={image_url}
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
          </div>
        </div>

        {/* Правая колонка - информация */}
        <div className="flex-1">
          <h1 className="text-2xl font-bold mb-2 text-gray-900">{product.base_name}</h1>
          <div className="text-3xl font-bold text-green-600 mb-4">
            <CountUp 
              key={`price-${region.slug}`}
              end={price} 
              suffix=" руб."
              formatNumber={true}
              duration={1200}
            />
          </div>

          <div className="bg-gray-50 rounded-lg p-4 mb-4 text-gray-900">
            <div className="mb-2">
              Всего компаний в базе: <strong>
                <CountUp 
                  key={`total-${region.slug}`}
                  end={productVariant.total_companies} 
                  suffix=" шт."
                  formatNumber={true}
                  duration={1500}
                />
              </strong>
            </div>
            <div className="text-green-600 mb-2">✓ Контакты без повторов</div>
            <div className="text-sm text-gray-600">
              Вы можете изменить регион выборки или настроить базу в нашем гибком конфигураторе
            </div>
          </div>

          <ul className="space-y-2 mb-6 text-gray-900">
            <li>✓ 6 месяцев бесплатного обновления</li>
            <li><strong>База обновлена:</strong> {new Date().toLocaleDateString('ru-RU')}</li>
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