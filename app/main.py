from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import FastAPI
import asyncio
import uvicorn

from api import images_api, stream_api, tracks_api
from core.library_auto import *
from core.library_scan import *
from infra.database import *
from infra.path_handler import *
from infra.setup_logger import *

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await directory_create()
        await connect_database()
        await db.execute("PRAGMA journal_mode=WAL;")
        
        asyncio.create_task(check_db_data())
        asyncio.create_task(event_watcher())

    except KeyboardInterrupt:
        for task in asyncio.all_tasks():
            task.cancel()

    yield
    for task in asyncio.all_tasks():
        task.cancel()
    await disconnect_database()

app = FastAPI(
    debug=True,
    title="Tamaya",
    version="0.1.3a",
    lifespan=lifespan
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(images_api.router, prefix="/api")
app.include_router(stream_api.router, prefix="/api")
app.include_router(tracks_api.router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=2843,
        log_level="debug",
        log_config=None,
        reload=True
    )