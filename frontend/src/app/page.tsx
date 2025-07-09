import { redirect } from 'next/navigation';
import { getAllProducts } from '@/lib/api';

export default async function HomePage() {
  try {
    const products = await getAllProducts();
    
    // Если есть продукты, перенаправляем на первый из них
    if (products.length > 0) {
      redirect(`/${products[0].slug}/russia`);
    }
  } catch (error) {
    console.error('Error fetching products:', error);
  }

  // Фолбэк на baza-horeca, если что-то пошло не так
  redirect('/baza-horeca/russia');
}
