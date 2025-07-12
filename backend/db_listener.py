"""
Database Listener для прослушивания PostgreSQL NOTIFY уведомлений
и рассылки их через WebSocket соединения.
"""

import asyncio
import json
import logging
import os
from typing import Optional

import asyncpg
from websocket_manager import manager
import crud
from database import async_session

logger = logging.getLogger(__name__)


class DatabaseListener:
    """Класс для прослушивания уведомлений от PostgreSQL"""
    
    def __init__(self):
        self.connection: Optional[asyncpg.Connection] = None
        self.is_listening = False
        
    async def connect(self):
        """Устанавливает соединение с базой данных для прослушивания"""
        database_url = os.getenv("DATABASE_URL")
        
        if not database_url:
            logger.error("❌ DATABASE_URL не задана! Database Listener не может подключиться к БД")
            raise Exception("DATABASE_URL environment variable is not set")
        
        logger.info(f"🔗 Database Listener подключается к БД: {database_url[:50]}...")
        
        # Конвертируем URL для asyncpg (убираем +asyncpg если есть)
        if "+asyncpg" in database_url:
            database_url = database_url.replace("+asyncpg", "")
            
        try:
            self.connection = await asyncpg.connect(database_url)
            logger.info("✅ Database Listener: соединение с БД для прослушивания уведомлений установлено")
            
            # Тест соединения - проверяем что мы подключены к правильной БД
            result = await self.connection.fetchval("SELECT current_database()")
            logger.info(f"📊 Database Listener подключен к БД: {result}")
            
        except Exception as e:
            logger.error(f"❌ Database Listener: ошибка подключения к БД: {e}")
            raise
    
    async def disconnect(self):
        """Закрывает соединение с базой данных"""
        if self.connection:
            await self.connection.close()
            self.connection = None
            logger.info("Соединение с БД для прослушивания закрыто")
    
    async def handle_notification(self, notification):
        """Обрабатывает уведомление от PostgreSQL"""
        try:
            # Парсим JSON payload
            payload = json.loads(notification.payload)
            table = payload.get('table')
            operation = payload.get('operation')
            data = payload.get('data')
            
            logger.info(f"DB notify: {table}.{operation} ID {data.get('id')}")
            
            # Обрабатываем только изменения в product_variants
            if table == 'product_variants' and operation in ['INSERT', 'UPDATE']:
                await self.handle_product_variant_change(data)
            elif table == 'products' and operation in ['INSERT', 'UPDATE']:
                await self.handle_product_change(data)
                
        except Exception as e:
            logger.error(f"Ошибка обработки уведомления: {e}")
    
    async def handle_product_variant_change(self, variant_data):
        """Обрабатывает изменения в product_variants"""
        try:
            variant_id = variant_data.get('id')
            if not variant_id:
                logger.warning("Получено уведомление без ID варианта продукта")
                return
            
            logger.info(f"🔄 Обработка изменения варианта ID {variant_id}")
            
            # Получаем актуальные данные варианта из БД
            async with async_session() as session:
                # Ищем variant по ID и получаем полную информацию с продуктом и регионом
                from sqlalchemy.future import select
                from sqlalchemy.orm import joinedload
                from models import ProductVariant, Product, Region
                
                query = (
                    select(ProductVariant)
                    .options(
                        joinedload(ProductVariant.product),
                        joinedload(ProductVariant.region)
                    )
                    .where(ProductVariant.id == variant_id)
                )
                result = await session.execute(query)
                variant = result.scalars().first()
                
                if not variant:
                    logger.warning(f"Вариант продукта с ID {variant_id} не найден")
                    return
                
                logger.info(f"📦 Найден вариант: {variant.product.base_name} в {variant.region.name_nominative}, цена: {variant.price}")
                
                # Формируем сообщение для отправки клиентам
                message = {
                    "type": "PRODUCT_VARIANT_UPDATE",
                    "payload": {
                        "id": variant.id,
                        "price": float(variant.price),
                        "total_companies": variant.total_companies,
                        "companies_with_email": variant.companies_with_email,
                        "companies_with_phone": variant.companies_with_phone,
                        "companies_with_site": variant.companies_with_site,
                        "companies_with_address": variant.companies_with_address,
                        "companies_with_activity": variant.companies_with_activity,
                        "is_active": variant.is_active,
                        "title": variant.title,
                        "description": variant.description,
                        "seo_text": variant.seo_text,
                        "product": {
                            "id": variant.product.id,
                            "base_name": variant.product.base_name,
                            "slug": variant.product.slug,
                            "image_url": variant.product.image_url,
                            "tags": variant.product.tags,
                            "is_top": variant.product.is_top,
                            "created_at": variant.product.created_at.isoformat() if variant.product.created_at else None,
                            "updated_at": variant.product.updated_at.isoformat() if variant.product.updated_at else None,
                        },
                        "region": {
                            "id": variant.region.id,
                            "name_nominative": variant.region.name_nominative,
                            "name_genitive": variant.region.name_genitive,
                            "name_prepositional": variant.region.name_prepositional,
                            "slug": variant.region.slug,
                        }
                    }
                }
                
                # Проверяем количество подключенных клиентов
                connection_count = manager.get_connection_count()
                logger.info(f"📡 Отправка обновления {connection_count} подключенным клиентам")
                
                # Отправляем сообщение всем подключенным клиентам
                await manager.broadcast(message)
                logger.info(f"✅ Обновление отправлено для варианта ID {variant_id}")
                
        except Exception as e:
            logger.error(f"❌ Ошибка обработки изменения варианта продукта: {e}")
            import traceback
            logger.error(f"Полная трассировка: {traceback.format_exc()}")
    
    async def handle_product_change(self, product_data):
        """Обрабатывает изменения в products"""
        try:
            # Для простоты можно просто залогировать изменение продукта
            # В будущем можно добавить специфичную логику
            product_id = product_data.get('id')
            logger.info(f"Изменение продукта ID {product_id} - обработка может быть добавлена в будущем")
            
        except Exception as e:
            logger.error(f"Ошибка обработки изменения продукта: {e}")
    
    async def listen_for_notifications(self):
        """Основная функция прослушивания уведомлений"""
        if not self.connection:
            logger.error("Нет соединения с БД для прослушивания")
            return
            
        try:
            # Подписываемся на канал уведомлений
            await self.connection.add_listener('data_updates', self.handle_notification)
            self.is_listening = True
            logger.info("Начато прослушивание канала 'data_updates'")
            
            # Бесконечный цикл прослушивания
            while self.is_listening:
                await asyncio.sleep(1)  # Небольшая пауза чтобы не нагружать CPU
                
        except Exception as e:
            logger.error(f"Ошибка в процессе прослушивания уведомлений: {e}")
        finally:
            self.is_listening = False
            logger.info("Прослушивание уведомлений остановлено")
    
    async def stop_listening(self):
        """Останавливает прослушивание уведомлений"""
        self.is_listening = False
        if self.connection:
            await self.connection.remove_listener('data_updates', self.handle_notification)
            logger.info("Подписка на уведомления отменена")


# Глобальный экземпляр листенера
listener = DatabaseListener()


async def start_db_listener():
    """Запускает прослушивание уведомлений от БД"""
    try:
        await listener.connect()
        await listener.listen_for_notifications()
    except Exception as e:
        logger.error(f"Критическая ошибка в DB Listener: {e}")
        # Попытка переподключения через 5 секунд
        await asyncio.sleep(5)
        logger.info("Попытка переподключения DB Listener...")
        await start_db_listener()


async def stop_db_listener():
    """Останавливает прослушивание уведомлений от БД"""
    await listener.stop_listening()
    await listener.disconnect() 