"""WebSocket manager for real-time updates."""

import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime
import json


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass


manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    
    try:
        while True:
            # Send mock updates
            await websocket.send_json({
                "type": "update",
                "data": {
                    "assets": [
                        {"id": "1", "name": "Pump A-01", "health": 95, "status": "Running"},
                        {"id": "2", "name": "Compressor C-12", "health": 82, "status": "Running"},
                    ],
                    "incidents": [],
                    "notifications": [
                        {
                            "id": "1",
                            "title": "System Online",
                            "message": "All systems operational",
                            "severity": "info",
                            "timestamp": datetime.now().isoformat()
                        }
                    ],
                    "timestamp": datetime.now().isoformat()
                }
            })
            
            await asyncio.sleep(2)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)