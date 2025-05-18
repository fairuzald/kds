from app.api.deps import get_db
from app.ml.model_service import model_service
from app.models.bacteria import Bacteria
from app.schemas.bacteria import (
    BacteriaPredictionInputSchema,
    BacteriaPredictionResponseDataSchema,
    BacteriaResponseSchema,
    SimilarBacteriaInfoSchema,
)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session as SQLAlchemySession

router = APIRouter()


@router.post("/predict", response_model=BacteriaPredictionResponseDataSchema)
def predict_bacteria_pathogenicity(
    *,
    db: SQLAlchemySession = Depends(get_db),
    bacteria_input: BacteriaPredictionInputSchema,
):
    try:
        prediction_label, probability = model_service.predict_pathogenicity(
            bacteria_input.model_dump()
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}",
        )

    db_bacteria_sample = db.query(Bacteria).limit(1000).all()

    all_bacteria_dicts_for_similarity = []
    if db_bacteria_sample:
        all_bacteria_dicts_for_similarity = [
            BacteriaResponseSchema.model_validate(b).model_dump()
            for b in db_bacteria_sample
        ]

    similar_bacteria_dicts_with_score = model_service.find_similar_bacteria(
        input_bacteria_data=bacteria_input.model_dump(),
        all_bacteria_dicts=all_bacteria_dicts_for_similarity,
        n_similar=5,
    )

    similar_bacteria_response = []
    for sim_bact_dict in similar_bacteria_dicts_with_score:
        try:
            similar_bacteria_response.append(SimilarBacteriaInfoSchema(**sim_bact_dict))
        except Exception as e:
            print(
                f"Error converting similar bacteria to schema: {e}, data: {sim_bact_dict}"
            )

    response_data = BacteriaPredictionResponseDataSchema(
        input_bacteria=bacteria_input,
        is_pathogen_prediction=bool(prediction_label),
        pathogen_probability=float(probability),
        similar_bacteria=similar_bacteria_response,
    )
    return response_data
