#!/usr/bin/env python3
"""
Скрипт для тестирования real-time обновлений WebSocket.
Изменяет данные в базе данных, что должно вызвать уведомления через WebSocket.
"""

import asyncio
import asyncpg
import os
import random
import time
from datetime import datetime

async def test_realtime_updates():
    """Тестирует real-time обновления через изменение данных в БД"""
    
    # Подключаемся к базе данных
    database_url = os.getenv("DATABASE_URL", "postgresql://antonuricin@localhost:5432/mydb")
    if "+asyncpg" in database_url:
        database_url = database_url.replace("+asyncpg", "")
    
    print(f"🔌 Подключение к базе данных...")
    conn = await asyncpg.connect(database_url)
    
    try:
        # Получаем список всех product_variants
        variants = await conn.fetch("""
            SELECT pv.id, pv.price, pv.total_companies, p.base_name, r.name_nominative
            FROM product_variants pv
            JOIN products p ON pv.product_id = p.id
            JOIN regions r ON pv.region_id = r.id
            WHERE pv.is_active = true
            ORDER BY pv.id
            LIMIT 10
        """)
        
        if not variants:
            print("❌ Нет активных вариантов продуктов для тестирования")
            return
        
        print(f"📊 Найдено {len(variants)} вариантов продуктов для тестирования")
        print("\nСписок вариантов:")
        for variant in variants:
            print(f"  ID: {variant['id']} | {variant['base_name']} - {variant['name_nominative']}")
            print(f"    Цена: {variant['price']} руб, Компаний: {variant['total_companies']}")
        
        print("\n" + "="*60)
        print("🚀 НАЧИНАЕМ ТЕСТИРОВАНИЕ REAL-TIME ОБНОВЛЕНИЙ")
        print("="*60)
        
        # Бесконечный цикл тестирования
        while True:
            # Выбираем случайный вариант для обновления
            variant = random.choice(variants)
            variant_id = variant['id']
            
            # Генерируем новые случайные данные
            new_price = round(random.uniform(1000, 5000), 2)
            new_total_companies = random.randint(500, 3000)
            new_companies_with_email = int(new_total_companies * random.uniform(0.6, 0.9))
            new_companies_with_phone = int(new_total_companies * random.uniform(0.8, 0.98))
            new_companies_with_site = int(new_total_companies * random.uniform(0.3, 0.6))
            new_companies_with_address = int(new_total_companies * random.uniform(0.9, 1.0))
            new_companies_with_activity = int(new_total_companies * random.uniform(0.7, 0.95))
            
            # Обновляем данные в базе данных
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"\n[{timestamp}] 🔄 Обновляем вариант ID {variant_id}")
            print(f"  Продукт: {variant['base_name']} - {variant['name_nominative']}")
            print(f"  Старая цена: {variant['price']} руб → Новая цена: {new_price} руб")
            print(f"  Старое кол-во компаний: {variant['total_companies']} → Новое: {new_total_companies}")
            
            # Выполняем UPDATE запрос
            await conn.execute("""
                UPDATE product_variants 
                SET 
                    price = $1,
                    total_companies = $2,
                    companies_with_email = $3,
                    companies_with_phone = $4,
                    companies_with_site = $5,
                    companies_with_address = $6,
                    companies_with_activity = $7
                WHERE id = $8
            """, new_price, new_total_companies, new_companies_with_email, 
                 new_companies_with_phone, new_companies_with_site, 
                 new_companies_with_address, new_companies_with_activity, variant_id)
            
            print(f"  ✅ Обновление выполнено! Триггер должен отправить WebSocket уведомление.")
            
            # Обновляем локальный кеш для следующей итерации
            for i, v in enumerate(variants):
                if v['id'] == variant_id:
                    variants[i] = {
                        **v,
                        'price': new_price,
                        'total_companies': new_total_companies
                    }
                    break
            
            # Ждем перед следующим обновлением
            print(f"  ⏱️ Ждем 10 секунд перед следующим обновлением...")
            await asyncio.sleep(10)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Тестирование остановлено пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
    finally:
        await conn.close()
        print("🔌 Соединение с базой данных закрыто")

if __name__ == "__main__":
    print("🧪 Real-Time Update Tester")
    print("Этот скрипт будет изменять данные в базе каждые 10 секунд")
    print("Откройте фронтенд в браузере и наблюдайте за обновлениями!")
    print("Для остановки нажмите Ctrl+C")
    print("\n" + "="*60)
    
    asyncio.run(test_realtime_updates()) 