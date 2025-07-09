'use client';

import { ProductInfo } from '@/types';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

interface ProductSidebarProps {
  products: ProductInfo[];
}

export default function ProductSidebar({ products }: ProductSidebarProps) {
  const pathname = usePathname();
  
  // Определяем текущий активный продукт из URL
  const currentProductSlug = pathname.split('/')[1];

  return (
    <div className="w-80 min-h-screen bg-white border-r border-gray-200 p-6">
      <h2 className="text-xl font-bold text-gray-900 mb-6">Наши базы данных</h2>
      
      <nav className="space-y-2">
        {products.map((product) => {
          const isActive = currentProductSlug === product.slug;
          const href = `/${product.slug}/russia`;
          
          return (
            <Link
              key={product.slug}
              href={href}
              className={`
                block w-full p-3 text-left rounded-lg transition-colors
                ${isActive 
                  ? 'bg-green-50 text-green-700 border-l-4 border-green-500' 
                  : 'text-gray-700 hover:bg-gray-50'
                }
              `}
            >
              <div className="font-medium">{product.base_name}</div>
              {isActive && (
                <div className="text-sm text-green-600 mt-1">
                  ← Активная база
                </div>
              )}
            </Link>
          );
        })}
      </nav>
      
      <div className="mt-8 p-4 bg-gray-50 rounded-lg">
        <h3 className="font-medium text-gray-900 mb-2">Нужна помощь?</h3>
        <p className="text-sm text-gray-600 mb-3">
          Свяжитесь с нами для получения консультации по базам данных
        </p>
        <a 
          href="tel:88007752912" 
          className="text-sm text-green-600 hover:text-green-700"
        >
          8 800 775-29-12
        </a>
      </div>
    </div>
  );
} 