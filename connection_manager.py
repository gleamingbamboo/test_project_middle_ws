from fastapi import WebSocket

# Track connected WebSocket clients
active_connections: set[WebSocket] = set()
