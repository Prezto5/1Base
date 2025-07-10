import { ProductVariantDetail } from '@/types';
import { formatNumber } from '@/lib/utils';

interface ProductStatsProps {
  productVariant: ProductVariantDetail;
}

export default function ProductStats({ productVariant }: ProductStatsProps) {
  const { region } = productVariant;

  const stats = [
    {
      value: productVariant.total_companies,
      label: 'Всего компаний в базе'
    },
    {
      value: productVariant.companies_with_phone,
      label: 'Компаний с телефонами'
    },
    {
      value: productVariant.companies_with_email,
      label: 'Компаний с Email'
    },
    {
      value: productVariant.companies_with_site,
      label: 'Компаний с сайтами'
    },
    {
      value: productVariant.companies_with_address,
      label: 'Компаний с адресами'
    },
    {
      value: productVariant.companies_with_activity,
      label: 'Компаний с указанием сферы деятельности'
    },
  ];

  return (
    <div className="container max-w-4xl mx-auto my-8 bg-white rounded-xl shadow-lg p-6 text-gray-900">
      <h2 className="text-xl font-bold mb-4 text-gray-900">
        О Базе HoReCa (Хорека) {region.name_genitive}
      </h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {stats.map((stat, index) => (
          <div key={`${region.slug}-${index}`} className="bg-gray-50 rounded-lg p-4 text-center">
            <div className="text-2xl font-bold text-green-600 mb-1">
              {formatNumber(stat.value, ' шт.')}
            </div>
            <div className="text-sm text-gray-700">
              {stat.label}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
} 