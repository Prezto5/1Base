from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
import crud
import schemas
from typing import List
import random
import asyncio
import logging
from websocket_manager import manager
from db_listener import start_db_listener, stop_db_listener

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Настройка CORS для работы с Next.js фронтендом и WebSocket
import os

# Получаем окружение и URL фронтенда
API_ENV = os.getenv("API_ENV", "development")
FRONTEND_URL = os.getenv("FRONTEND_URL", "")

# Настройка CORS в зависимости от окружения
if API_ENV == "production":
    allowed_origins = [
        "https://frontend-production-8178.up.railway.app",
        "https://backend-production-7dfe.up.railway.app",
    ]
    # Добавляем URL фронтенда если он задан
    if FRONTEND_URL:
        allowed_origins.append(FRONTEND_URL)
else:  # development
    allowed_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://frontend-dev-7b28.up.railway.app",
        "https://backend-dev-962f.up.railway.app",
    ]
    # Добавляем URL фронтенда если он задан  
    if FRONTEND_URL:
        allowed_origins.append(FRONTEND_URL)

# Логируем для отладки
logger.info(f"API_ENV: {API_ENV}")
logger.info(f"FRONTEND_URL: {FRONTEND_URL}")
logger.info(f"Allowed CORS origins: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация данных вынесена в отдельный скрипт seed.py
# Для первой настройки запустите: python backend/seed.py

# ВАЖНО: Более специфичные маршруты должны быть определены ПЕРЕД более общими!

@app.get("/api/v1/products", response_model=List[schemas.ProductInfo])
async def get_all_products(session: AsyncSession = Depends(get_session)):
    """Получает список всех продуктов"""
    products = await crud.get_all_products(session)
    return [
        schemas.ProductInfo(
            base_name=product.base_name,
            slug=product.slug
        )
        for product in products
    ]

@app.get("/api/v1/products/{product_slug}/regions", response_model=List[schemas.RegionInfo])
async def get_regions_for_product(product_slug: str, session: AsyncSession = Depends(get_session)):
    variants = await crud.get_regions_for_product(session, product_slug)
    
    # Сортируем регионы: "Россия" первой, остальные в алфавитном порядке
    russia_variant = None
    other_variants = []
    
    for variant in variants:
        if variant.region.slug == 'russia':
            russia_variant = variant
        else:
            other_variants.append(variant)
    
    # Сортируем остальные регионы в алфавитном порядке
    other_variants.sort(key=lambda v: v.region.name_nominative)
    
    # Формируем итоговый список
    sorted_variants = []
    if russia_variant:
        sorted_variants.append(russia_variant)
    sorted_variants.extend(other_variants)
    
    regions = [
        schemas.RegionInfo(
            name_nominative=variant.region.name_nominative,
            slug=variant.region.slug,
            price=float(variant.price)
        )
        for variant in sorted_variants
    ]
    return regions

@app.get("/api/v1/products/{product_slug}/{region_slug}", response_model=schemas.ProductVariantDetail)
async def get_product_variant_detail(product_slug: str, region_slug: str, session: AsyncSession = Depends(get_session)):
    variant = await crud.get_product_variant_detail(session, product_slug, region_slug)

    # Generate stable random rating data based on variant ID
    random.seed(variant.id)
    rating_value = round(random.uniform(4.7, 5.0), 1)
    review_count = random.randint(30, 300)

    return schemas.ProductVariantDetail(
        id=variant.id,
        price=float(variant.price),
        total_companies=variant.total_companies,
        companies_with_email=variant.companies_with_email,
        companies_with_phone=variant.companies_with_phone,
        companies_with_site=variant.companies_with_site,
        companies_with_address=variant.companies_with_address,
        companies_with_activity=variant.companies_with_activity,
        is_active=variant.is_active,
        # SEO fields now come from variant instead of product
        title=variant.title,
        description=variant.description,
        seo_text=variant.seo_text,
        # Generated rating data
        ratingValue=rating_value,
        reviewCount=review_count,
        product=schemas.ProductBase(
            id=variant.product.id,
            base_name=variant.product.base_name,
            slug=variant.product.slug,
            image_url=variant.product.image_url,
            tags=variant.product.tags,
            is_top=variant.product.is_top,
            created_at=variant.product.created_at,
            updated_at=variant.product.updated_at,
        ),
        region=schemas.RegionBase(
            id=variant.region.id,
            name_nominative=variant.region.name_nominative,
            name_genitive=variant.region.name_genitive,
            name_prepositional=variant.region.name_prepositional,
            slug=variant.region.slug,
        ),
    )


# WebSocket эндпоинт для real-time обновлений
@app.websocket("/ws/updates")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket эндпоинт для получения real-time обновлений"""
    await manager.connect(websocket)
    logger.info("Новое WebSocket соединение")
    
    try:
        # Отправляем приветственное сообщение
        await manager.send_personal_message(
            '{"type": "CONNECTION_ESTABLISHED", "message": "WebSocket соединение установлено"}', 
            websocket
        )
        
        # Создаем задачу для ping-pong механизма
        ping_task = asyncio.create_task(send_ping_periodically(websocket))
        
        try:
            # Ожидаем сообщения от клиента
            while True:
                try:
                    data = await websocket.receive_text()
                    # Обработка сообщений от клиента может быть добавлена в будущем
                    logger.info(f"Получено сообщение от клиента: {data}")
                except WebSocketDisconnect:
                    logger.info("WebSocket клиент отключился")
                    break
                except Exception as e:
                    logger.error(f"Ошибка при получении сообщения от WebSocket клиента: {e}")
                    break
        finally:
            # Отменяем ping задачу при отключении
            ping_task.cancel()
            try:
                await ping_task
            except asyncio.CancelledError:
                pass
                
    except WebSocketDisconnect:
        logger.info("WebSocket соединение было закрыто")
    except Exception as e:
        logger.error(f"Ошибка в WebSocket соединении: {e}")
    finally:
        manager.disconnect(websocket)


async def send_ping_periodically(websocket: WebSocket):
    """Отправляет ping сообщения каждые 25 секунд для поддержания соединения"""
    try:
        while True:
            await asyncio.sleep(25)  # Пинг каждые 25 секунд
            try:
                await websocket.send_text('{"type": "PING", "timestamp": "' + str(asyncio.get_event_loop().time()) + '"}')
                logger.debug("Ping отправлен")
            except Exception as e:
                logger.warning(f"Ошибка отправки ping: {e}")
                break
    except asyncio.CancelledError:
        logger.info("Ping задача отменена")
        raise


# События жизненного цикла приложения
@app.on_event("startup")
async def startup_event():
    """Запуск фоновых задач при старте приложения"""
    logger.info("Запуск FastAPI приложения...")
    
    # Запускаем DB listener в фоновом режиме
    asyncio.create_task(start_db_listener())
    logger.info("Database listener запущен в фоне")


@app.on_event("shutdown")
async def shutdown_event():
    """Очистка ресурсов при остановке приложения"""
    logger.info("Остановка FastAPI приложения...")
    
    # Останавливаем DB listener
    await stop_db_listener()
    logger.info("Database listener остановлен")


# Статические файлы теперь обрабатываются Next.js фронтендом 