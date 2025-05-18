from app.api.routes import bacteria, health, predictions
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(bacteria.router, prefix="/bacteria", tags=["bacteria"])
api_router.include_router(
    predictions.router, prefix="/predictions", tags=["predictions"]
)
