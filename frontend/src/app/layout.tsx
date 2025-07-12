import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { getAllProducts } from "@/lib/api";
import ProductSidebar from "@/components/ProductSidebar";
import { RealtimeDataProvider } from "@/context/RealtimeDataContext";

// Принудительно делаем layout динамическим для получения свежих данных
export const dynamic = 'force-dynamic';

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Базы данных - Лучшие решения для бизнеса",
  description: "Качественные базы данных для различных отраслей бизнеса",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  let products;
  
  try {
    products = await getAllProducts();
  } catch (error) {
    console.error('Failed to load products in layout:', error);
    // Фолбэк продукты если API недоступен
    products = [
      { base_name: "База HoReCa (Хорека)", slug: "baza-horeca" },
      { base_name: "База продавцов OZON", slug: "baza-prodavtsov-ozon" }
    ];
  }

  return (
    <html lang="ru">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <RealtimeDataProvider>
          <div className="flex">
            <ProductSidebar products={products} />
            <main className="flex-1">
              {children}
            </main>
          </div>
        </RealtimeDataProvider>
      </body>
    </html>
  );
}
