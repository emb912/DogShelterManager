from typing import List
from fastapi import WebSocket
from datetime import datetime
from threading import Lock


class WebSocketManager:
    """Menedżer połączeń WebSocket.
    
    Zarządza aktywnymi połączeniami WebSocket i umożliwia wysyłanie wiadomości
    broadcast do wszystkich podłączonych klientów.
    
    Attributes:
        active_connections: Lista aktywnych połączeń WebSocket.
        status_connections: Lista połączeń dla statusu serwera.
        started_at: Czas uruchomienia menedżera.
        last_activity: Czas ostatniej aktywności.
    """
    
    def __init__(self) -> None:
        """Inicjalizuje menedżera z pustą listą połączeń."""
        self.active_connections: List[WebSocket] = []
        self.status_connections: List[WebSocket] = []
        self.started_at: str = datetime.now().isoformat()
        self.last_activity: str | None = None
        # Zmienna współdzielona server_status uzywana przez wszystkie requesty + blokada do synchronizacji
        self._status_lock = Lock()
        self.server_status: dict = {
            "status": "running",
            "started_at": self.started_at,
            "last_activity": self.last_activity,
        }

    async def connect(self, websocket: WebSocket) -> None:
        """Akceptuje i dodaje nowe połączenie WebSocket.
        
        Args:
            websocket: Obiekt WebSocket do podłączenia.
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    async def connect_status(self, websocket: WebSocket) -> None:
        """Akceptuje i dodaje nowe połączenie WebSocket dla statusu.
        
        Args:
            websocket: Obiekt WebSocket do podłączenia.
        """
        await websocket.accept()
        self.status_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        """Usuwa połączenie WebSocket z listy aktywnych.
        
        Args:
            websocket: Obiekt WebSocket do odłączenia.
        """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    def disconnect_status(self, websocket: WebSocket) -> None:
        """Usuwa połączenie WebSocket z listy statusu.
        
        Args:
            websocket: Obiekt WebSocket do odłączenia.
        """
        if websocket in self.status_connections:
            self.status_connections.remove(websocket)

    async def broadcast(self, message: dict) -> None:
        """Wysyła wiadomość JSON do wszystkich aktywnych połączeń.
        
        Args:
            message: Słownik z danymi do wysłania jako JSON.
        """
        # Aktualizuje współdzielony server_status z użyciem blokady
        with self._status_lock:
            self.last_activity = datetime.now().isoformat()
            self.server_status["last_activity"] = self.last_activity

        # Wysyła główną wiadomość do wszystkich klientów statystyk
        for connection in list(self.active_connections):
            await connection.send_json(message)

        # Po każdej zmianie wysyła aktualny status do klientów statusu
        await self.broadcast_status()

    async def broadcast_status(self) -> None:
        """Wysyła aktualny status serwera do wszystkich połączeń statusowych."""
        status_message = {"type": "server_status", **self.get_status()}
        for connection in list(self.status_connections):
            try:
                await connection.send_json(status_message)
            except Exception:
                pass  # Ignoruj błędy wysylki

    def get_status(self) -> dict:
        """Zwraca kopię aktualnego server_status z użyciem blokady."""
        with self._status_lock:
            return dict(self.server_status)


# Globalna instancja menedżera WebSocket
manager: WebSocketManager = WebSocketManager()
