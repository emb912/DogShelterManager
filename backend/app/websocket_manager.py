from typing import List
from fastapi import WebSocket

class WebSocketManager:
    """Menedżer połączeń WebSocket.
    
    Zarządza aktywnymi połączeniami WebSocket i umożliwia wysyłanie wiadomości
    broadcast do wszystkich podłączonych klientów.
    
    Attributes:
        active_connections: Lista aktywnych połączeń WebSocket.
    """
    
    def __init__(self) -> None:
        """Inicjalizuje menedżera z pustą listą połączeń."""
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        """Akceptuje i dodaje nowe połączenie WebSocket.
        
        Args:
            websocket: Obiekt WebSocket do podłączenia.
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        """Usuwa połączenie WebSocket z listy aktywnych.
        
        Args:
            websocket: Obiekt WebSocket do odłączenia.
        """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict) -> None:
        """Wysyła wiadomość JSON do wszystkich aktywnych połączeń.
        
        Args:
            message: Słownik z danymi do wysłania jako JSON.
        """
        for connection in self.active_connections:
            await connection.send_json(message)


# Globalna instancja menedżera WebSocket
manager: WebSocketManager = WebSocketManager()
