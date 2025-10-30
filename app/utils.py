import asyncio
import signal
from datetime import datetime

from app.logger import logger
from app.tasks import wait_for_shutdown

shutdown_initiated_at: datetime | None = None


def start_graceful_shutdown():
    """Start shutdown timer and wait for connections to close."""
    global shutdown_initiated_at
    if shutdown_initiated_at is not None:
        return  # Prevent duplicate triggers
    shutdown_initiated_at = datetime.utcnow()
    asyncio.create_task(wait_for_shutdown())


# Handle multiple workers (graceful shutdown per worker)
def setup_signal_handlers():
    loop = asyncio.get_event_loop()

    def handle_signal(*_):
        logger.warning("Received shutdown signal (SIGTERM/SIGINT)")
        start_graceful_shutdown()

    for sig in (signal.SIGTERM, signal.SIGINT):
        try:
            loop.add_signal_handler(sig, handle_signal)
        except NotImplementedError:
            # Windows compatibility
            signal.signal(sig, lambda *_: asyncio.create_task(handle_signal()))
