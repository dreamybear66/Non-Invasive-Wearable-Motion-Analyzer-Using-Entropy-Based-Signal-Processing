from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.api.sessions import router as sessions_router
from app.api.data_ingestion import router as data_ingestion_router
from app.api.signals import router as signals_router
from app.api.ws import router as ws_router
from app.api.entropy import router as entropy_router
from app.core.redis import init_redis, close_redis

app = FastAPI(title="Sports EL Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_redis()

@app.on_event("shutdown")
async def shutdown_event():
    await close_redis()

app.include_router(sessions_router, prefix="/api/v1/sessions", tags=["Sessions"])
app.include_router(data_ingestion_router, prefix="/api/v1/sessions", tags=["Ingestion"])
app.include_router(signals_router, prefix="/api/v1/sessions", tags=["Signals"])
app.include_router(entropy_router, prefix="/api/v1/sessions", tags=["Entropy"])
app.include_router(ws_router, prefix="/ws", tags=["Websocket"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
