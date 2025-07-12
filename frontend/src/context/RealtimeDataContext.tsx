'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode, useCallback, useMemo } from 'react';
import { useWebSocket } from '@/hooks/useWebSocket';
import { ProductVariantDetail } from '@/types';

interface WebSocketMessage {
  type: string;
  payload?: unknown;
  message?: string;
}

interface RealtimeDataContextType {
  // WebSocket состояние
  isWebSocketConnected: boolean;
  webSocketError: string | null;
  
  // Real-time данные
  updatedVariants: Map<number, ProductVariantDetail>;
  
  // Методы
  getUpdatedVariant: (variantId: number) => ProductVariantDetail | null;
  reconnectWebSocket: () => void;
}

const RealtimeDataContext = createContext<RealtimeDataContextType | undefined>(undefined);

interface RealtimeDataProviderProps {
  children: ReactNode;
}

export function RealtimeDataProvider({ children }: RealtimeDataProviderProps) {
  const [updatedVariants, setUpdatedVariants] = useState<Map<number, ProductVariantDetail>>(new Map());
  
  // Получаем WebSocket URL из переменных окружения или формируем динамически
  const getWebSocketUrl = () => {
    // Сначала пробуем использовать явно заданный WS URL
    if (process.env.NEXT_PUBLIC_WS_URL) {
      console.log('🔗 Используется явный WebSocket URL:', process.env.NEXT_PUBLIC_WS_URL);
      return process.env.NEXT_PUBLIC_WS_URL;
    }
    
    // Если WS URL не задан, формируем на основе API URL
    const apiUrl = process.env.NEXT_PUBLIC_API_URL;
    if (apiUrl) {
      // Преобразуем http/https в ws/wss
      const wsUrl = apiUrl.replace(/^http/, 'ws') + '/ws/updates';
      console.log('🔗 Автоматически сформированный WebSocket URL:', wsUrl);
      return wsUrl;
    }
    
    // Fallback для локальной разработки
    console.log('🔗 Используется fallback WebSocket URL для локальной разработки');
    return 'ws://localhost:8000/ws/updates';
  };
  
  const wsUrl = getWebSocketUrl();
  
  // Мемоизируем обработчики чтобы предотвратить пересоздание WebSocket соединения
  const handleWebSocketMessage = useCallback((message: WebSocketMessage) => {
    console.log('📥 Real-time сообщение:', message.type);
    switch (message.type) {
      case 'CONNECTION_ESTABLISHED':
        console.log('🎉 WebSocket соединение установлено');
        break;
        
      case 'PING':
        // Отвечаем на ping сообщения для поддержания соединения
        console.log('🏓 Получен PING, отправляем PONG');
        // Браузер автоматически отвечает на WebSocket ping/pong, 
        // но можно добавить дополнительную логику если нужно
        break;
        
      case 'PRODUCT_VARIANT_UPDATE':
        if (message.payload) {
          const variant = message.payload as ProductVariantDetail;
          console.log(`📦 Обновление варианта ID ${variant.id}: цена ${variant.price}, компаний ${variant.total_companies}`);
          
          // Обновляем состояние с новыми данными варианта
          setUpdatedVariants(prev => {
            const newMap = new Map(prev);
            newMap.set(variant.id, variant);
            return newMap;
          });
        }
        break;
        
      default:
        console.log('⚠️ Неизвестный тип WebSocket сообщения:', message.type);
        break;
    }
  }, []);

  const onConnect = useCallback(() => {
    console.log('✅ Real-time контекст: WebSocket подключен');
  }, []);

  const onDisconnect = useCallback(() => {
    console.log('❌ Real-time контекст: WebSocket отключен');
  }, []);

  // Мемоизируем options объект
  const websocketOptions = useMemo(() => ({
    onMessage: handleWebSocketMessage,
    onConnect,
    onDisconnect,
    reconnectAttempts: 5,
    reconnectInterval: 1000,
    enableReconnect: true,
  }), [handleWebSocketMessage, onConnect, onDisconnect]);
  
  const {
    isConnected: isWebSocketConnected,
    connectionError: webSocketError,
    lastMessage,
    reconnect: reconnectWebSocket,
  } = useWebSocket(wsUrl, websocketOptions);

  const getUpdatedVariant = (variantId: number): ProductVariantDetail | null => {
    return updatedVariants.get(variantId) || null;
  };

  useEffect(() => {
    if (lastMessage) {
      handleWebSocketMessage(lastMessage);
    }
  }, [lastMessage, handleWebSocketMessage]);

  const contextValue: RealtimeDataContextType = {
    isWebSocketConnected,
    webSocketError,
    updatedVariants,
    getUpdatedVariant,
    reconnectWebSocket,
  };

  return (
    <RealtimeDataContext.Provider value={contextValue}>
      {children}
    </RealtimeDataContext.Provider>
  );
}

export function useRealtimeData(): RealtimeDataContextType {
  const context = useContext(RealtimeDataContext);
  if (context === undefined) {
    throw new Error('useRealtimeData должен использоваться внутри RealtimeDataProvider');
  }
  return context;
}

// Хук для получения актуальных данных варианта с real-time обновлениями
export function useVariantWithRealtime(initialVariant: ProductVariantDetail): ProductVariantDetail {
  const { getUpdatedVariant } = useRealtimeData();
  const [currentVariant, setCurrentVariant] = useState<ProductVariantDetail>(initialVariant);

  useEffect(() => {
    // Проверяем есть ли обновленная версия варианта
    const updatedVariant = getUpdatedVariant(initialVariant.id);
    if (updatedVariant) {
      console.log(`🔄 Применение real-time обновления для варианта ${updatedVariant.id}: ${initialVariant.price} → ${updatedVariant.price}`);
      setCurrentVariant(updatedVariant);
    } else {
      setCurrentVariant(initialVariant);
    }
  }, [initialVariant, getUpdatedVariant, currentVariant.price, currentVariant.total_companies]);

  return currentVariant;
} 