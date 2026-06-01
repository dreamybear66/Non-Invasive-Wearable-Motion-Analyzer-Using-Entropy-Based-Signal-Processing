from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
from uuid import UUID

class SessionManager:
    def __init__(self):
        # Maps session_id (str) to list of WebSockets
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)

    def disconnect(self, websocket: WebSocket, session_id: str):
        if session_id in self.active_connections:
            if websocket in self.active_connections[session_id]:
                self.active_connections[session_id].remove(websocket)
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]

    async def broadcast_update(self, session_id: str, data: dict):
        if session_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[session_id]:
                try:
                    await connection.send_text(json.dumps(data))
                except Exception:
                    disconnected.append(connection)
                    
            for conn in disconnected:
                self.disconnect(conn, session_id)

live_manager = SessionManager()
