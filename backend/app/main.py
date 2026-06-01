"""
Sports EL — FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title="Sports EL API",
    description="Non-Invasive Athletic Fatigue Detection via Entropy-Based Motion Signal Analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
async def health_check():
    """Service health check endpoint."""
    return {
        "status": "ok",
        "service": "Sports EL API",
        "version": "1.0.0",
    }


# TODO Phase 4: Register API routers
# from app.api import sessions, athletes, auth, entropy, reports
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
# app.include_router(sessions.router, prefix="/api/v1/sessions", tags=["Sessions"])
# app.include_router(athletes.router, prefix="/api/v1/athletes", tags=["Athletes"])
# app.include_router(entropy.router, prefix="/api/v1", tags=["Entropy"])
# app.include_router(reports.router, prefix="/api/v1", tags=["Reports"])
