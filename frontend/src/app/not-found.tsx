import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-gray-900 mb-4">404</h1>
        <h2 className="text-2xl font-semibold text-gray-700 mb-4">
          Страница не найдена
        </h2>
        <p className="text-gray-600 mb-8">
          Запрашиваемая страница не существует или была перемещена.
        </p>
        <Link 
          href="/baza-horeca/russia"
          className="inline-block bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg font-medium transition-colors"
        >
          На главную
        </Link>
      </div>
    </div>
  );
} 