import { useEffect, useState, useRef } from 'react';
import type { DogStats } from '../types';

const WS_URL = 'ws://localhost:8000/ws/dogs';

export const useSocket = () => {
  const [stats, setStats] = useState<DogStats | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessageTime, setLastMessageTime] = useState<number>(Date.now());
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const connect = () => {
      const ws = new WebSocket(WS_URL);
      socketRef.current = ws;

      ws.onopen = () => {
        console.log('Connected to WebSocket');
        setIsConnected(true);
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          setStats(data);
          setLastMessageTime(Date.now());
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      ws.onclose = () => {
        console.log('Disconnected from WebSocket');
        setIsConnected(false);
        // Reconnect after a delay
        setTimeout(connect, 3000);
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        ws.close();
      };
    };

    connect();

    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, []);

  return { stats, isConnected, lastMessageTime };
};
