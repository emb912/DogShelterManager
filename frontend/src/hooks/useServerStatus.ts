import { useEffect, useState, useRef } from "react";
import type { ServerStatus } from "../types";

const WS_URL = "ws://localhost:8000/ws/status";

export const useServerStatus = () => {
  const [serverStatus, setServerStatus] = useState<ServerStatus | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const connect = () => {
      const ws = new WebSocket(WS_URL);
      socketRef.current = ws;

      ws.onopen = () => {
        console.log("Connected to Server Status WebSocket");
        setIsConnected(true);
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.type === "server_status") {
            setServerStatus(data);
          }
        } catch (error) {
          console.error("Error parsing WebSocket message:", error);
        }
      };

      ws.onclose = () => {
        console.log("Disconnected from Server Status WebSocket");
        setIsConnected(false);
        // Reconnect after a delay
        setTimeout(connect, 3000);
      };

      ws.onerror = (error) => {
        console.error("WebSocket error:", error);
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

  // Funkcja do żądania odświeżenia statusu
  const requestStatus = () => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send("get_status");
    }
  };

  return { serverStatus, isConnected, requestStatus };
};
