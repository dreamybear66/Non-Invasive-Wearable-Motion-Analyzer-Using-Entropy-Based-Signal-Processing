import { useState, useEffect, useCallback, useRef } from 'react';

export function useWebSocket(sessionId, onMessage) {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState(null);
  const wsRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);
  const reconnectDelayRef = useRef(1000); // Start with 1s

  const connect = useCallback(() => {
    if (!sessionId) return;
    
    // Cleanup previous connection
    if (wsRef.current) {
      wsRef.current.close();
    }

    const wsUrl = import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000/ws';
    const ws = new WebSocket(`${wsUrl}/sessions/${sessionId}/live`);
    wsRef.current = ws;

    ws.onopen = () => {
      setIsConnected(true);
      reconnectDelayRef.current = 1000; // Reset backoff on successful connect
      console.log(`WebSocket connected to session ${sessionId}`);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setLastMessage(data);
        if (onMessage) onMessage(data);
      } catch (err) {
        console.error("Failed to parse websocket message", err);
      }
    };

    ws.onclose = () => {
      setIsConnected(false);
      console.log(`WebSocket disconnected from session ${sessionId}`);
      
      // Auto-reconnect with exponential backoff (max 30s)
      const delay = reconnectDelayRef.current;
      reconnectTimeoutRef.current = setTimeout(() => {
        reconnectDelayRef.current = Math.min(delay * 1.5, 30000);
        connect();
      }, delay);
    };

    ws.onerror = (error) => {
      console.error("WebSocket error", error);
      // onclose will handle reconnect
    };

  }, [sessionId, onMessage]);

  useEffect(() => {
    connect();

    return () => {
      if (wsRef.current) wsRef.current.close();
      if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
    };
  }, [connect]);

  const send = useCallback((message) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(typeof message === 'string' ? message : JSON.stringify(message));
    } else {
      console.warn("WebSocket is not connected. Cannot send message.");
    }
  }, []);

  return { isConnected, lastMessage, send };
}
