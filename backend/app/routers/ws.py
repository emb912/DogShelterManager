from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from ..websocket_manager import manager
from ..database import get_db
from ..crud.dog import get_dog_stats

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
    # Wyślij początkowe statystyki
    await websocket.send_json(get_dog_stats(db))

    try:
        while True:
            await websocket.receive_text()  # utrzymuj połączenie aktywne
    except WebSocketDisconnect:
        manager.disconnect(websocket)

