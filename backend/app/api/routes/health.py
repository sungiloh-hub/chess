from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def health_check():
    """Health check endpoint to verify the API is running."""
    return {
        "status": "healthy",
        "message": "Backend is running successfully"
    }


@router.get("/ping")
async def ping():
    """Simple ping endpoint."""
    return {"ping": "pong"}
