from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from ..websocket_manager import manager
from ..database import get_db
from ..crud.dog import get_dog_stats

router = APIRouter()

@router.websocket("/ws/dogs")
async def dogs_websocket(websocket: WebSocket, db: Session = Depends(get_db)):
    await manager.connect(websocket)
    # Send initial stats
    await websocket.send_json(get_dog_stats(db))

    try:
        while True:
            await websocket.receive_text()  # keep alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)

