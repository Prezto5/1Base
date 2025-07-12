"""
WebSocket Connection Manager для управления активными соединениями
и рассылки real-time обновлений клиентам.
"""

import json
import logging
from typing import List, Dict, Any
from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Менеджер для управления WebSocket соединениями"""
    
    def __init__(self):
        # Список активных WebSocket соединений
        self.active_connections: List[WebSocket] = []
        
    async def connect(self, websocket: WebSocket):
        """Принимает новое WebSocket соединение"""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket подключен. Всего: {len(self.active_connections)}")
        
    def disconnect(self, websocket: WebSocket):
        """Удаляет WebSocket соединение из списка активных"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket отключен. Всего: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Отправляет сообщение конкретному клиенту"""
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Ошибка при отправке персонального сообщения: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: Dict[str, Any]):
        """Рассылает сообщение всем подключенным клиентам"""
        if not self.active_connections:
            logger.debug("Нет активных WebSocket соединений для рассылки")
            return
            
        message_str = json.dumps(message, ensure_ascii=False)
        logger.info(f"Рассылка сообщения {len(self.active_connections)} клиентам: {message.get('type', 'UNKNOWN')}")
        
        # Создаем копию списка для безопасной итерации
        connections_copy = self.active_connections.copy()
        
        for connection in connections_copy:
            try:
                await connection.send_text(message_str)
            except WebSocketDisconnect:
                # Клиент отключился
                logger.info("Клиент отключился во время рассылки")
                self.disconnect(connection)
            except Exception as e:
                # Другие ошибки соединения
                logger.error(f"Ошибка при отправке сообщения клиенту: {e}")
                self.disconnect(connection)
    
    def get_connection_count(self) -> int:
        """Возвращает количество активных соединений"""
        return len(self.active_connections)


# Глобальный экземпляр менеджера соединений
manager = ConnectionManager() 