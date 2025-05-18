from typing import Any, Dict

from app.api.deps import get_db
from app.core.response import StandardResponse, success_response
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as SQLAlchemySession

router = APIRouter()


@router.get("", response_model=StandardResponse[Dict[str, str]])
def health_check_basic():
    return success_response(
        message="Service is healthy", data={"status": "UP", "service": "Backend API"}
    )


@router.get("/details", response_model=StandardResponse[Dict[str, Any]])
def health_check_detailed(db: SQLAlchemySession = Depends(get_db)):
    db_status = "UP"
    db_error = None
    try:
        db.execute("SELECT 1")
    except Exception as e:
        db_status = "DOWN"
        db_error = str(e)

    return success_response(
        message="Detailed health check",
        data={
            "overall_status": "UP" if db_status == "UP" else "DEGRADED",
            "components": {"database": {"status": db_status, "error": db_error}},
        },
    )
