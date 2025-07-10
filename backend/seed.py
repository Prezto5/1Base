#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных начальными данными.
"""

import asyncio
import random
from sqlalchemy import func, select
from database import async_session
from models import Product, Region, ProductVariant


# Структура данных для продуктов
PRODUCTS_DATA = [
    {
        "base_name": "База HoReCa (Хорека)",
        "slug": "baza-horeca", 
        "image_url": "https://i.ibb.co/603DcX47/photo-2025-01-31-15-57-56.jpg",
        "tags": "рестораны, кафе, гостиницы, базы отдыха, отели, бары, клубы, столовые, хорека",
        "is_top": True
    },
    {
        "base_name": "База продавцов OZON",
        "slug": "baza-prodavtsov-ozon",
        "image_url": "https://i.ibb.co/8zBN9JQ/ozon-sellers-database.jpg",
        "tags": "продавцы, магазины, интернет-торговля, маркетплейс, электронная коммерция, ozon",
        "is_top": False
    }
]


async def create_product_variants(session, product_id, regions, product_info):
    """Создает варианты продукта для всех регионов"""
    variants = []
    regional_variants = []
    
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
        
        # Генерируем SEO контент для региона
        title = f"Купить {product_info['base_name']} в {region.name_prepositional} - обновляемая база данных"
        description = f"Актуальная база данных '{product_info['base_name']}' для региона {region.name_genitive}. Содержит {total_companies} контактов. Скачайте демо-версию!"
        seo_text = f"База данных '{product_info['base_name']}' для {region.name_genitive} - это полная и актуальная информация о компаниях региона. В базе содержится {total_companies} проверенных контактов с подробной информацией о каждой компании. Регулярное обновление данных гарантирует актуальность информации. Получите конкурентное преимущество с нашей базой данных!"
        
        variant = ProductVariant(
            product_id=product_id,
            region_id=region.id,
            price=random.randint(1500, 3000),
            total_companies=total_companies,
            companies_with_email=companies_with_email,
            companies_with_phone=companies_with_phone,
            companies_with_site=companies_with_site,
            companies_with_address=companies_with_address,
            companies_with_activity=companies_with_activity,
            is_active=True,
            title=title,
            description=description,
            seo_text=seo_text,
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
        
        # Генерируем SEO контент для России
        russia_title = f"Купить {product_info['base_name']} по всей России - обновляемая база данных"
        russia_description = f"Актуальная база данных '{product_info['base_name']}' по всей России. Содержит {total_all_companies} контактов. Скачайте демо-версию!"
        russia_seo_text = f"База данных '{product_info['base_name']}' по всей России - это самая полная и актуальная информация о компаниях всех регионов. В базе содержится {total_all_companies} проверенных контактов с подробной информацией о каждой компании. Объединенная база всех регионов России для максимального охвата рынка. Получите конкурентное преимущество с нашей базой данных!"
        
        russia_variant = ProductVariant(
            product_id=product_id,
            region_id=russia_region.id,
            price=int(avg_price),
            total_companies=total_all_companies,
            companies_with_email=total_all_email,
            companies_with_phone=total_all_phone,
            companies_with_site=total_all_site,
            companies_with_address=total_all_address,
            companies_with_activity=total_all_activity,
            is_active=True,
            title=russia_title,
            description=russia_description,
            seo_text=russia_seo_text,
        )
        variants.append(russia_variant)
    
    variants.extend(regional_variants)
    return variants


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

        # Создаем продукты и их варианты
        all_variants = []
        for product_data in PRODUCTS_DATA:
            product = Product(**product_data)
            session.add(product)
            await session.flush()
            print(f"Создан продукт: {product.base_name}")
            
            # Создаем варианты для продукта
            variants = await create_product_variants(session, product.id, regions, product_data)
            all_variants.extend(variants)
            
            # Агрегированные данные для России
            russia_variants = [v for v in variants if v.region_id == next(r.id for r in regions if r.slug == 'russia')]
            if russia_variants:
                print(f"Создан агрегированный вариант для России: {russia_variants[0].total_companies} компаний")
            
            print(f"Создано вариантов для продукта '{product.base_name}': {len(variants)}")

        # Сохраняем все варианты
        session.add_all(all_variants)
        print(f"Создано всего вариантов продуктов: {len(all_variants)}")

        await session.commit()
        print("Инициализация базы данных завершена успешно!")


if __name__ == "__main__":
    asyncio.run(seed_database()) 