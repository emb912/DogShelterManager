from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..websocket_manager import manager

router = APIRouter()

@router.websocket("/ws/dogs")
async def dogs_websocket(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            #receive data or wait forever
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
