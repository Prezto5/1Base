import { redirect } from 'next/navigation';

export default function HomePage() {
  // Редирект на страницу продукта по умолчанию - "Россия"
  redirect('/baza-horeca/russia');
}
