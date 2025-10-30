import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.events import shutdown_event
from app.logger import logger
from app.router import ws_router
from app.tasks import periodic_notifications
from app.utils import setup_signal_handlers

app = FastAPI(title="FastAPI WebSocket Server with Graceful Shutdown")

app.include_router(ws_router)
# Allow cross-origin for easy testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    logger.info("Server starting up...")

    # Background task to send test notifications every 10s
    asyncio.create_task(periodic_notifications())


@app.on_event("shutdown")
async def on_shutdown():
    """Triggered when FastAPI receives a shutdown signal."""
    logger.info("Shutdown event received. Initiating graceful shutdown.")
    shutdown_event.set()


setup_signal_handlers()
