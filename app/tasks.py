import asyncio
from datetime import datetime, timedelta

from app.connection_manager import active_connections
from app.events import shutdown_event
from app.logger import logger

GRACEFUL_SHUTDOWN_TIMEOUT = 30 * 60  # 30 minutes


async def notify_all(message: str):
    """Broadcast message to all connected clients."""
    if not active_connections:
        return
    disconnected = []
    for ws in list(active_connections):
        try:
            await ws.send_text(message)
        except Exception:
            disconnected.append(ws)
    for ws in disconnected:
        active_connections.discard(ws)


async def periodic_notifications():
    """Send periodic test notifications."""
    while not shutdown_event.is_set():
        await asyncio.sleep(10)
        await notify_all("🔔 Test notification from server")


async def wait_for_shutdown():
    """Wait for all clients to disconnect or for timeout."""
    deadline = datetime.utcnow() + timedelta(seconds=GRACEFUL_SHUTDOWN_TIMEOUT)

    while datetime.utcnow() < deadline:
        if not active_connections:
            logger.info("✅ All WebSocket clients disconnected. Shutting down now.")
            break

        remaining_time = int((deadline - datetime.utcnow()).total_seconds())
        logger.info(
            f"Waiting for {len(active_connections)} clients to disconnect. "
            f"Time left: {remaining_time}s"
        )
        await asyncio.sleep(5)
    else:
        logger.warning("⏰ Graceful shutdown timeout reached. Forcing shutdown.")

    # Stop the server
    import os
    os._exit(0)  # Force stop
