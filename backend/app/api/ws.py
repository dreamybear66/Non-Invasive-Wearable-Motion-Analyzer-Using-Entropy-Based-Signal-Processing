from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.live_stream import live_manager

router = APIRouter()

@router.websocket("/sessions/{session_id}/live")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await live_manager.connect(websocket, session_id)
    try:
        while True:
            # Wait for any message from the client (e.g. ping)
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        live_manager.disconnect(websocket, session_id)
