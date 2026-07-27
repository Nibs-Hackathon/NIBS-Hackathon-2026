# Folder: backend/api/websocket Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `backend/api/websocket`

Contains 1 project file(s) directly in this folder (nested folders have their own inventory files).

## backend/api/websocket/manager.py

**Folder path:** `backend/api/websocket`

**File path:** `backend/api/websocket/manager.py`

```python
"""WebSocket manager for real-time updates."""

import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState


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
        dead = []
        for connection in list(self.active_connections):
            if connection.client_state != WebSocketState.CONNECTED:
                dead.append(connection)
                continue
            try:
                await connection.send_json(message)
            except Exception:
                dead.append(connection)
        for connection in dead:
            self.disconnect(connection)


manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket):
    """Legacy helper endpoint — production uses api.main.websocket_endpoint."""
    await manager.connect(websocket)
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            try:
                await websocket.send_json({"type": "ping"})
            except (WebSocketDisconnect, RuntimeError, OSError):
                break
            try:
                message = await asyncio.wait_for(websocket.receive(), timeout=2.0)
                if message.get("type") == "websocket.disconnect":
                    break
            except asyncio.TimeoutError:
                continue
            except WebSocketDisconnect:
                break
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(websocket)
```
