'use client';

import { useEffect, useRef, useState, useCallback } from 'react';

interface WebSocketMessage {
  type: string;
  payload?: unknown;
  message?: string;
}

interface UseWebSocketReturn {
  isConnected: boolean;
  connectionError: string | null;
  lastMessage: WebSocketMessage | null;
  sendMessage: (message: string) => void;
  reconnect: () => void;
}

interface UseWebSocketOptions {
  onMessage?: (message: WebSocketMessage) => void;
  onConnect?: () => void;
  onDisconnect?: () => void;
  onError?: (error: Event) => void;
  reconnectAttempts?: number;
  reconnectInterval?: number;
  enableReconnect?: boolean;
}

export function useWebSocket(url: string, options: UseWebSocketOptions = {}): UseWebSocketReturn {
  const [isConnected, setIsConnected] = useState(false);
  const [connectionError, setConnectionError] = useState<string | null>(null);
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);
  
  const websocketRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const reconnectAttemptsRef = useRef(0);
  const maxReconnectAttempts = options.reconnectAttempts || 5;
  const baseReconnectInterval = options.reconnectInterval || 1000;
  const enableReconnect = options.enableReconnect !== false;
  const isManualCloseRef = useRef(false);
  const mountedRef = useRef(true);

  const clearReconnectTimeout = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
  }, []);

  const shouldReconnect = useCallback((closeEvent: CloseEvent) => {
    return mountedRef.current && 
           closeEvent.code !== 1000 && 
           !isManualCloseRef.current &&
           reconnectAttemptsRef.current < maxReconnectAttempts &&
           enableReconnect;
  }, [maxReconnectAttempts, enableReconnect]);

  const getReconnectDelay = useCallback((attemptNumber: number) => {
    return Math.min(Math.pow(2, attemptNumber) * baseReconnectInterval, 30000);
  }, [baseReconnectInterval]);

  const connect = useCallback(() => {
    if (websocketRef.current?.readyState === WebSocket.OPEN || 
        websocketRef.current?.readyState === WebSocket.CONNECTING) {
      return;
    }

    if (!mountedRef.current) {
      return;
    }

    try {
      const ws = new WebSocket(url);
      websocketRef.current = ws;
      isManualCloseRef.current = false;

      ws.onopen = () => {
        if (!mountedRef.current) return;
        
        setIsConnected(true);
        setConnectionError(null);
        reconnectAttemptsRef.current = 0;
        clearReconnectTimeout();
        options.onConnect?.();
      };

      ws.onmessage = (event) => {
        if (!mountedRef.current) return;
        
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          setLastMessage(message);
          options.onMessage?.(message);
        } catch {
          // Ошибка парсинга сообщения
        }
      };

      ws.onclose = (event) => {
        if (!mountedRef.current) return;
        
        setIsConnected(false);
        websocketRef.current = null;
        options.onDisconnect?.();

        if (shouldReconnect(event)) {
          const attempt = reconnectAttemptsRef.current + 1;
          const delay = getReconnectDelay(attempt - 1);
          
          reconnectTimeoutRef.current = setTimeout(() => {
            if (mountedRef.current) {
              reconnectAttemptsRef.current = attempt;
              connect();
            }
          }, delay);
        } else if (reconnectAttemptsRef.current >= maxReconnectAttempts) {
          const errorMsg = `Не удалось переподключиться после ${maxReconnectAttempts} попыток`;
          setConnectionError(errorMsg);
        }
      };

      ws.onerror = () => {
        if (!mountedRef.current) return;
        
        setConnectionError('Ошибка WebSocket соединения');
        options.onError?.(new Event('error'));
      };

    } catch {
      setConnectionError('Не удалось создать WebSocket соединение');
    }
  }, [url, options, shouldReconnect, getReconnectDelay, maxReconnectAttempts, clearReconnectTimeout]);

  const disconnect = useCallback(() => {
    isManualCloseRef.current = true;
    clearReconnectTimeout();

    if (websocketRef.current && websocketRef.current.readyState !== WebSocket.CLOSED) {
      websocketRef.current.close(1000, 'Соединение закрыто пользователем');
    }

    websocketRef.current = null;
    setIsConnected(false);
    reconnectAttemptsRef.current = 0;
  }, [clearReconnectTimeout]);

  const sendMessage = useCallback((message: string) => {
    if (websocketRef.current?.readyState === WebSocket.OPEN) {
      websocketRef.current.send(message);
    }
  }, []);

  const reconnect = useCallback(() => {
    disconnect();
    reconnectAttemptsRef.current = 0;
    setConnectionError(null);
    
    setTimeout(() => {
      if (mountedRef.current) {
        connect();
      }
    }, 1000);
  }, [connect, disconnect]);

  useEffect(() => {
    mountedRef.current = true;
    connect();

    return () => {
      mountedRef.current = false;
      disconnect();
    };
  }, [url]);

  return {
    isConnected,
    connectionError,
    lastMessage,
    sendMessage,
    reconnect,
  };
} 