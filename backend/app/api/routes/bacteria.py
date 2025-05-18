import logging
from typing import Optional

from app.api.deps import get_db
from app.core.response import PaginatedResponseStructure, paginated_response
from app.models.bacteria import Bacteria
from app.schemas.bacteria import (
    BacteriaCreateSchema,
    BacteriaResponseSchema,
    BacteriaUpdateSchema,
)
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_
from sqlalchemy.orm import Session as SQLAlchemySession

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "", response_model=BacteriaResponseSchema, status_code=status.HTTP_201_CREATED
)
def create_bacteria_entry(
    *, db: SQLAlchemySession = Depends(get_db), bacteria_in: BacteriaCreateSchema
):
    existing_bacteria = (
        db.query(Bacteria)
        .filter(Bacteria.bacteria_id == bacteria_in.bacteria_id)
        .first()
    )
    if existing_bacteria:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Bacteria with ID {bacteria_in.bacteria_id} already exists.",
        )

    bacteria_dict = bacteria_in.model_dump(exclude_unset=True)
    db_bacteria = Bacteria(**bacteria_dict)

    try:
        db.add(db_bacteria)
        db.commit()
        db.refresh(db_bacteria)
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating bacteria entry: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )
    return db_bacteria


@router.get("/{bacteria_obj_id}", response_model=BacteriaResponseSchema)
def get_bacteria_by_db_id(
    bacteria_obj_id: int, db: SQLAlchemySession = Depends(get_db)
):
    bacteria = db.query(Bacteria).filter(Bacteria.id == bacteria_obj_id).first()
    if not bacteria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bacteria (by DB ID) not found",
        )
    return bacteria


@router.get("/search/id/{bacteria_unique_id}", response_model=BacteriaResponseSchema)
def get_bacteria_by_unique_id(
    bacteria_unique_id: str, db: SQLAlchemySession = Depends(get_db)
):
    bacteria = (
        db.query(Bacteria).filter(Bacteria.bacteria_id == bacteria_unique_id).first()
    )
    if not bacteria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bacteria (by unique bacteria_id) not found",
        )
    return bacteria


@router.get("", response_model=PaginatedResponseStructure[BacteriaResponseSchema])
def list_bacteria(
    db: SQLAlchemySession = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(
        None,
        min_length=2,
        description="Search term (min 2 chars) for name, species, genus, or bacteria_id",
    ),
    is_pathogen: Optional[bool] = Query(
        None, description="Filter by pathogenicity status"
    ),
    gram_stain: Optional[str] = Query(
        None, description="Filter by Gram stain (e.g., 'Positive', 'Negative')"
    ),
):
    query = db.query(Bacteria)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Bacteria.name.ilike(search_term),
                Bacteria.species.ilike(search_term),
                Bacteria.genus.ilike(search_term),
                Bacteria.bacteria_id.ilike(search_term),
            )
        )
    if is_pathogen is not None:
        query = query.filter(Bacteria.is_pathogen == is_pathogen)

    if gram_stain:
        query = query.filter(func.lower(Bacteria.gram_stain) == func.lower(gram_stain))

    try:
        total_items = query.count()
    except Exception as e:
        logger.error(f"Error counting items in list_bacteria: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="Error processing request during count"
        )

    offset = (page - 1) * page_size
    try:
        bacteria_list_orm = (
            query.order_by(Bacteria.id).offset(offset).limit(page_size).all()
        )
    except Exception as e:
        logger.error(f"Error fetching items in list_bacteria: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="Error processing request during fetch"
        )

    return paginated_response(
        data=bacteria_list_orm,
        total_items=total_items,
        page=page,
        page_size=page_size,
        message="Bacteria retrieved successfully",
    )


@router.put("/{bacteria_obj_id}", response_model=BacteriaResponseSchema)
def update_bacteria_entry(
    bacteria_obj_id: int,
    *,
    db: SQLAlchemySession = Depends(get_db),
    bacteria_in: BacteriaUpdateSchema,
):
    db_bacteria = db.query(Bacteria).filter(Bacteria.id == bacteria_obj_id).first()
    if not db_bacteria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bacteria not found"
        )

    update_data = bacteria_in.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No update data provided"
        )

    for field, value in update_data.items():
        setattr(db_bacteria, field, value)

    try:
        db.add(db_bacteria)
        db.commit()
        db.refresh(db_bacteria)
    except Exception as e:
        db.rollback()
        logger.error(
            f"Error updating bacteria entry {bacteria_obj_id}: {e}", exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error on update: {str(e)}",
        )
    return db_bacteria


@router.delete("/{bacteria_obj_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bacteria_entry(
    bacteria_obj_id: int, db: SQLAlchemySession = Depends(get_db)
):
    db_bacteria = db.query(Bacteria).filter(Bacteria.id == bacteria_obj_id).first()
    if not db_bacteria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bacteria not found"
        )

    try:
        db.delete(db_bacteria)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(
            f"Error deleting bacteria entry {bacteria_obj_id}: {e}", exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error on delete: {str(e)}",
        )
    return None
