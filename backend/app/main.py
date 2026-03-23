from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api.routes import health, game

settings = get_settings()

app = FastAPI(
    title="Chess Tutor API",
    version=settings.app_version,
    debug=settings.debug,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix=settings.api_prefix)
app.include_router(game.router, prefix=settings.api_prefix)


@app.get("/")
async def root():
    return {
        "app": "Chess Tutor",
        "version": settings.app_version,
        "docs": "/docs",
    }
