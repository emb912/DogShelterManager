from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from ..websocket_manager import manager
from ..database import get_db
from ..crud.dog import get_dog_stats
from ..crud.cat import get_cat_stats

router = APIRouter()


@router.websocket("/ws/dogs")
async def dogs_websocket(websocket: WebSocket, db: Session = Depends(get_db)) -> None:
    """Endpoint WebSocket do wysyłania statystyk psów w schronisku w czasie rzeczywistym.
    
    Podłącza klienta do WebSocket i wysyła początkowe statystyki,
    następnie utrzymuje połączenie aktywne dla przyszłych aktualizacji.
    
    Args:
        websocket: Połączenie WebSocket z klientem.
        db: Sesja bazy danych (dependency injection).
        
    Note:
        Połączenie jest automatycznie zamykane przy rozłączeniu klienta.
        Klient otrzymuje aktualizacje statystyk przy każdej operacji CRUD.
    """
    await manager.connect(websocket)
    # początkowe statystyki
    await websocket.send_json({"type": "dog_stats", **get_dog_stats(db)})

    try:
        while True:
            await websocket.receive_text()  # połączenie aktywne
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.websocket("/ws/cats")
async def cats_websocket(websocket: WebSocket, db: Session = Depends(get_db)) -> None:
    """Endpoint WebSocket do wysyłania statystyk kotów w schronisku w czasie rzeczywistym.
    
    Podłącza klienta do WebSocket i wysyła początkowe statystyki kotów,
    następnie utrzymuje połączenie aktywne dla przyszłych aktualizacji.
    
    Args:
        websocket: Połączenie WebSocket z klientem.
        db: Sesja bazy danych (dependency injection).
        
    Note:
        Połączenie jest automatycznie zamykane przy rozłączeniu klienta.
        Klient otrzymuje aktualizacje statystyk przy każdej operacji CRUD.
    """
    await manager.connect(websocket)
    # początkowe statystyki kotów
    await websocket.send_json({"type": "cat_stats", **get_cat_stats(db)})

    try:
        while True:
            await websocket.receive_text()  # połączenie aktywne
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.websocket("/ws/status")
async def status_websocket(websocket: WebSocket) -> None:
    """Endpoint WebSocket do wysyłania statusu serwera w czasie rzeczywistym.
    
    Podłącza klienta do WebSocket i wysyła aktualny status serwera.
    
    Args:
        websocket: Połączenie WebSocket z klientem.
        
    Note:
        Połączenie jest automatycznie zamykane przy rozłączeniu klienta.
    """
    await manager.connect_status(websocket)
    # początkowy status serwera
    await websocket.send_json({"type": "server_status", **manager.get_status()})

    try:
        while True:
            await websocket.receive_text()  # połączenie aktywne
    except WebSocketDisconnect:
        manager.disconnect_status(websocket)

