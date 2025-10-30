from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from connection_manager import active_connections
from logger import logger

ws_router = APIRouter()

@ws_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connections."""
    await websocket.accept()
    active_connections.add(websocket)
    logger.info(f"Client connected. Total connections: {len(active_connections)}")

    try:
        while True:
            # Keep listening for incoming messages (optional)
            data = await websocket.receive_text()
            logger.info(f"Received from client: {data}")
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        active_connections.discard(websocket)
        logger.info(f"Client disconnected. Remaining: {len(active_connections)}")