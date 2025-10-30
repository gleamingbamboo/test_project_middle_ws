## 🧩 Overview

#### This project implements a FastAPI WebSocket server that supports:

- Real-time notifications to connected clients

- Connection tracking

- Graceful shutdown: waits for all clients to disconnect or forces shutdown after 30 minutes

## 🛠️ Setup Instructions 

### 1️⃣ Prerequisites

- Python 3.10+

- uv installed

`pip install uv`


or (recommended)

`curl -LsSf https://astral.sh/uv/install.sh | sh`

### 2️⃣ Install Dependencies

Use uv sync to create and populate your virtual environment from pyproject.toml and uv.lock:

`uv sync`


This will install all required dependencies (FastAPI, Uvicorn, etc.) into .venv/.
### 2. Run the server
`uvicorn main:app --host 0.0.0.0 --port 8000`


(Optional) For multi-worker mode:

`uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2`


#### ⚠️ Graceful shutdown logic runs per worker, so each worker will manage its own WebSocket connections independently.

🔌 Test the WebSocket Endpoint

You can test the WebSocket using:

- A browser console

- wscat CLI tool

- A custom HTML client

#### Example using `wscat`

`npm install -g wscat`

`wscat -c ws://localhost:8000/ws`


You’ll receive a message every 10 seconds:

` 🔔 Test notification from server `


You can also send messages, and the server will echo them back.

### 🧨 Graceful Shutdown Logic Explained

#### When the server receives a SIGTERM or SIGINT:

#### 1. It logs the shutdown initiation.

#### 2. Starts a timer for 30 minutes.

#### 3. Continues running until:

#### - All WebSocket clients disconnect, or

#### - The 30-minute timeout expires.

#### 4. Logs progress every 5 seconds.

#### 5. If clients remain after 30 minutes, the server forces shutdown.

#### This ensures:

#### - No active clients are abruptly disconnected (if possible).

#### - The server won’t hang forever in shutdown mode.