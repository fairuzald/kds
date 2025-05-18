import logging

from app.api.routes.bacteria import router as bacteria_router
from app.api.routes.health import router as health_router
from app.api.routes.predictions import router as predictions_router
from app.core.config import settings
from app.ml.model_service import model_service
from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

logging.basicConfig(level=settings.LOG_LEVEL.upper())
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.PROJECT_NAME, openapi_url="/openapi.json", version="0.1.0")

api_router = APIRouter(prefix=settings.API_V1_STR)


if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(url) for url in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    logger.info(
        "CORS_ORIGINS not set or empty, CORS middleware not configured with specific origins."
    )
    if settings.ENVIRONMENT == "development":
        logger.warning("DEVELOPMENT MODE: Configuring CORS to allow all origins ('*').")
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up application...")
    if settings.ML_MODEL_PRELOAD:
        logger.info(
            "Attempting to preload ML model (this happens when model_service is first imported/used)..."
        )
        if model_service.model and model_service.preprocessor:
            logger.info(
                "ML model appears to be preloaded successfully (model and preprocessor attributes are set)."
            )
        else:
            logger.error(
                "ML model preloading seems to have failed. "
                "The 'model' or 'preprocessor' attribute on the model_service instance is not set. "
                "This is LIKELY DUE TO AN INCOMPATIBLE PICKLE FILE (see _RemainderColsList error). "
                "PLEASE RE-PICKLE THE MODEL with compatible scikit-learn/numpy versions."
            )
    else:
        logger.info(
            "ML model preloading is disabled by settings.ML_MODEL_PRELOAD=False."
        )


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down application...")


api_router.include_router(health_router, prefix="/health", tags=["Health"])
api_router.include_router(
    predictions_router, prefix="/predictions", tags=["Predictions"]
)
api_router.include_router(bacteria_router, prefix="/bacteria", tags=["Bacteria"])

app.include_router(api_router)

logger.info(
    f"Application '{settings.PROJECT_NAME}' started. Environment: {settings.ENVIRONMENT}"
)
logger.info("OpenAPI docs available at /docs (relative to app root).")
logger.info(f"All API endpoints are under '{settings.API_V1_STR}' prefix.")
