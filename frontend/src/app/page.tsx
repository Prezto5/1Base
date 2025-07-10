import { redirect } from 'next/navigation';

export default function HomePage() {
  // Статический редирект на базовый продукт и регион
  // Избегаем блокирующего API запроса при каждом посещении главной страницы
  redirect('/baza-horeca/russia');
}
