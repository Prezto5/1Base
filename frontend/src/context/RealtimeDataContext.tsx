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
  
  // Получаем WebSocket URL из переменных окружения
  const wsUrl = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/ws/updates';
  
  // Мемоизируем обработчики чтобы предотвратить пересоздание WebSocket соединения
  const handleWebSocketMessage = useCallback((message: WebSocketMessage) => {
    switch (message.type) {
      case 'CONNECTION_ESTABLISHED':
        // Соединение установлено
        break;
        
      case 'PRODUCT_VARIANT_UPDATE':
        if (message.payload) {
          // Обновляем состояние с новыми данными варианта
          setUpdatedVariants(prev => {
            const newMap = new Map(prev);
            newMap.set((message.payload as ProductVariantDetail).id, message.payload as ProductVariantDetail);
            return newMap;
          });
        }
        break;
        
      default:
        // Неизвестный тип сообщения
        break;
    }
  }, []);

  const onConnect = useCallback(() => {
    // WebSocket подключен
  }, []);

  const onDisconnect = useCallback(() => {
    // WebSocket отключен
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
      setCurrentVariant(updatedVariant);
    } else {
      setCurrentVariant(initialVariant);
    }
  }, [initialVariant, getUpdatedVariant, currentVariant.price, currentVariant.total_companies]);

  return currentVariant;
} 