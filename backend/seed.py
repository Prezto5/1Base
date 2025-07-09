#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных начальными данными.
"""

import asyncio
import random
from sqlalchemy import func, select
from database import async_session
from models import Product, Region, ProductVariant, Review


async def seed_database():
    """Заполняет базу данных начальными данными."""
    async with async_session() as session:
        # Проверяем, есть ли уже данные
        result = await session.execute(select(func.count(Region.id)))
        if result.scalar_one() > 0:
            print("База данных уже содержит данные. Пропускаем инициализацию.")
            return

        print("Начинаем инициализацию базы данных...")

        # Создаем регионы (включая "Россия" для агрегированных данных)
        regions_data = [
            {'name_nominative': 'Россия', 'name_genitive': 'России', 'name_prepositional': 'России', 'slug': 'russia'},
            {'name_nominative': 'Белгород', 'name_genitive': 'Белгорода', 'name_prepositional': 'Белгороде', 'slug': 'belgorod'},
            {'name_nominative': 'Москва', 'name_genitive': 'Москвы', 'name_prepositional': 'Москве', 'slug': 'moscow'},
            {'name_nominative': 'Санкт-Петербург', 'name_genitive': 'Санкт-Петербурга', 'name_prepositional': 'Санкт-Петербурге', 'slug': 'spb'},
            {'name_nominative': 'Новосибирск', 'name_genitive': 'Новосибирска', 'name_prepositional': 'Новосибирске', 'slug': 'novosibirsk'},
            {'name_nominative': 'Екатеринбург', 'name_genitive': 'Екатеринбурга', 'name_prepositional': 'Екатеринбурге', 'slug': 'ekaterinburg'},
            {'name_nominative': 'Казань', 'name_genitive': 'Казани', 'name_prepositional': 'Казани', 'slug': 'kazan'},
            {'name_nominative': 'Нижний Новгород', 'name_genitive': 'Нижнего Новгорода', 'name_prepositional': 'Нижнем Новгороде', 'slug': 'nizhniy-novgorod'},
            {'name_nominative': 'Челябинск', 'name_genitive': 'Челябинска', 'name_prepositional': 'Челябинске', 'slug': 'chelyabinsk'},
            {'name_nominative': 'Самара', 'name_genitive': 'Самары', 'name_prepositional': 'Самаре', 'slug': 'samara'},
            {'name_nominative': 'Омск', 'name_genitive': 'Омска', 'name_prepositional': 'Омске', 'slug': 'omsk'},
            {'name_nominative': 'Ростов-на-Дону', 'name_genitive': 'Ростова-на-Дону', 'name_prepositional': 'Ростове-на-Дону', 'slug': 'rostov-on-don'},
            {'name_nominative': 'Уфа', 'name_genitive': 'Уфы', 'name_prepositional': 'Уфе', 'slug': 'ufa'},
            {'name_nominative': 'Красноярск', 'name_genitive': 'Красноярска', 'name_prepositional': 'Красноярске', 'slug': 'krasnoyarsk'},
            {'name_nominative': 'Воронеж', 'name_genitive': 'Воронежа', 'name_prepositional': 'Воронеже', 'slug': 'voronezh'},
            {'name_nominative': 'Пермь', 'name_genitive': 'Перми', 'name_prepositional': 'Перми', 'slug': 'perm'},
            {'name_nominative': 'Волгоград', 'name_genitive': 'Волгограда', 'name_prepositional': 'Волгограде', 'slug': 'volgograd'},
            {'name_nominative': 'Краснодар', 'name_genitive': 'Краснодара', 'name_prepositional': 'Краснодаре', 'slug': 'krasnodar'},
            {'name_nominative': 'Саратов', 'name_genitive': 'Саратова', 'name_prepositional': 'Саратове', 'slug': 'saratov'},
            {'name_nominative': 'Тольятти', 'name_genitive': 'Тольятти', 'name_prepositional': 'Тольятти', 'slug': 'tolyatti'},
            {'name_nominative': 'Ижевск', 'name_genitive': 'Ижевска', 'name_prepositional': 'Ижевске', 'slug': 'izhevsk'},
            {'name_nominative': 'Ульяновск', 'name_genitive': 'Ульяновска', 'name_prepositional': 'Ульяновске', 'slug': 'ulyanovsk'},
            {'name_nominative': 'Хабаровск', 'name_genitive': 'Хабаровска', 'name_prepositional': 'Хабаровске', 'slug': 'khabarovsk'},
            {'name_nominative': 'Владивосток', 'name_genitive': 'Владивостока', 'name_prepositional': 'Владивостоке', 'slug': 'vladivostok'},
            {'name_nominative': 'Ярославль', 'name_genitive': 'Ярославля', 'name_prepositional': 'Ярославле', 'slug': 'yaroslavl'},
            {'name_nominative': 'Иркутск', 'name_genitive': 'Иркутска', 'name_prepositional': 'Иркутске', 'slug': 'irkutsk'},
            {'name_nominative': 'Тюмень', 'name_genitive': 'Тюмени', 'name_prepositional': 'Тюмени', 'slug': 'tyumen'},
        ]
        
        regions = [Region(**data) for data in regions_data]
        session.add_all(regions)
        await session.flush()
        print(f"Создано регионов: {len(regions)}")

        # Создаем продукт
        product = Product(
            base_name="База HoReCa (Хорека)",
            slug="baza-horeca",
            description="Полная база данных заведений общественного питания и гостиничного бизнеса.",
            is_top=True
        )
        session.add(product)
        await session.flush()
        print(f"Создан продукт: {product.base_name}")

        # Создаем варианты продукта для регионов
        variants = []
        regional_variants = []  # Сначала создаем региональные варианты (кроме России)
        
        # Создаем варианты для всех регионов кроме "Россия"
        for region in regions:
            if region.slug == 'russia':
                continue
                
            total_companies = random.randint(500, 2500)
            companies_with_email = int(total_companies * random.uniform(0.6, 0.9))
            companies_with_phone = int(total_companies * random.uniform(0.8, 0.98))
            companies_with_site = int(total_companies * random.uniform(0.3, 0.6))
            companies_with_address = int(total_companies * random.uniform(0.9, 1.0))
            companies_with_activity = int(total_companies * random.uniform(0.7, 0.95))
            
            variant = ProductVariant(
                product_id=product.id,
                region_id=region.id,
                price=random.randint(1500, 3000),
                image_url="https://via.placeholder.com/400x300/8bc34a/ffffff?text=HoReCa+База",
                total_companies=total_companies,
                companies_with_email=companies_with_email,
                companies_with_phone=companies_with_phone,
                companies_with_site=companies_with_site,
                companies_with_address=companies_with_address,
                companies_with_activity=companies_with_activity,
                is_active=True,
            )
            regional_variants.append(variant)
        
        # Находим регион "Россия" и создаем агрегированный вариант
        russia_region = next((r for r in regions if r.slug == 'russia'), None)
        if russia_region and regional_variants:
            # Вычисляем агрегированные данные
            total_all_companies = sum(v.total_companies for v in regional_variants)
            total_all_email = sum(v.companies_with_email for v in regional_variants)
            total_all_phone = sum(v.companies_with_phone for v in regional_variants)
            total_all_site = sum(v.companies_with_site for v in regional_variants)
            total_all_address = sum(v.companies_with_address for v in regional_variants)
            total_all_activity = sum(v.companies_with_activity for v in regional_variants)
            
            # Средняя цена по всем регионам
            avg_price = sum(v.price for v in regional_variants) / len(regional_variants)
            
            russia_variant = ProductVariant(
                product_id=product.id,
                region_id=russia_region.id,
                price=int(avg_price),
                image_url="https://via.placeholder.com/400x300/8bc34a/ffffff?text=HoReCa+База+Россия",
                total_companies=total_all_companies,
                companies_with_email=total_all_email,
                companies_with_phone=total_all_phone,
                companies_with_site=total_all_site,
                companies_with_address=total_all_address,
                companies_with_activity=total_all_activity,
                is_active=True,
            )
            variants.append(russia_variant)
            print(f"Создан агрегированный вариант для России: {total_all_companies} компаний")
        
        variants.extend(regional_variants)
        session.add_all(variants)
        print(f"Создано вариантов продукта: {len(variants)}")

        # Создаем отзывы
        reviews = [
            Review(product_id=product.id, author_name="Иван Петров", rating=5),
            Review(product_id=product.id, author_name="Мария Сидорова", rating=4),
            Review(product_id=product.id, author_name="Алексей", rating=5),
            Review(product_id=product.id, author_name="Елена", rating=4),
            Review(product_id=product.id, author_name="Дмитрий", rating=5),
            Review(product_id=product.id, author_name="Анна", rating=4),
        ]
        session.add_all(reviews)
        print(f"Создано отзывов: {len(reviews)}")

        await session.commit()
        print("Инициализация базы данных завершена успешно!")


if __name__ == "__main__":
    asyncio.run(seed_database()) 