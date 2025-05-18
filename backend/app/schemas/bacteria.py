import math
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_serializer


def serialize_float_to_json_safe(value: Optional[float]) -> Optional[float]:
    if value is None:
        return None
    if math.isfinite(value):
        return value
    return None


class BacteriaBaseSchema(BaseModel):
    bacteria_id: str = Field(max_length=50)
    name: Optional[str] = Field(None, max_length=255)
    superkingdom: Optional[str] = Field(None, max_length=100)
    kingdom: Optional[str] = Field(None, max_length=100)
    phylum: Optional[str] = Field(None, max_length=100)
    class_name: Optional[str] = Field(None, max_length=100)
    order: Optional[str] = Field(None, max_length=100)
    family: Optional[str] = Field(None, max_length=100)
    genus: Optional[str] = Field(None, max_length=100)
    species: Optional[str] = Field(None, max_length=100)
    strain: Optional[str] = Field(None, max_length=255)
    gram_stain: Optional[str] = Field(None, max_length=50)
    shape: Optional[str] = Field(None, max_length=100)
    mobility: Optional[bool] = None
    flagellar_presence: Optional[bool] = None
    number_of_membranes: Optional[str] = Field(None, max_length=50)
    oxygen_preference: Optional[str] = Field(None, max_length=100)
    optimal_temperature: Optional[float] = None
    temperature_range: Optional[str] = Field(None, max_length=100)
    habitat: Optional[str] = Field(None, max_length=500)
    biotic_relationship: Optional[str] = Field(None, max_length=255)
    cell_arrangement: Optional[str] = Field(None, max_length=255)
    sporulation: Optional[bool] = None
    metabolism: Optional[str] = Field(None, max_length=500)
    energy_source: Optional[str] = Field(None, max_length=255)
    is_pathogen: Optional[bool] = None

    @field_serializer("optimal_temperature", when_used="json")
    def serialize_optimal_temp(self, value: Optional[float]):
        return serialize_float_to_json_safe(value)

    model_config = ConfigDict(from_attributes=True)


class BacteriaCreateSchema(BacteriaBaseSchema):
    pass


class BacteriaUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    superkingdom: Optional[str] = Field(None, max_length=100)
    kingdom: Optional[str] = Field(None, max_length=100)
    phylum: Optional[str] = Field(None, max_length=100)
    class_name: Optional[str] = Field(None, max_length=100)
    order: Optional[str] = Field(None, max_length=100)
    family: Optional[str] = Field(None, max_length=100)
    genus: Optional[str] = Field(None, max_length=100)
    species: Optional[str] = Field(None, max_length=100)
    strain: Optional[str] = Field(None, max_length=255)
    gram_stain: Optional[str] = Field(None, max_length=50)
    shape: Optional[str] = Field(None, max_length=100)
    mobility: Optional[bool] = None
    flagellar_presence: Optional[bool] = None
    number_of_membranes: Optional[str] = Field(None, max_length=50)
    oxygen_preference: Optional[str] = Field(None, max_length=100)
    optimal_temperature: Optional[float] = None
    temperature_range: Optional[str] = Field(None, max_length=100)
    habitat: Optional[str] = Field(None, max_length=500)
    biotic_relationship: Optional[str] = Field(None, max_length=255)
    cell_arrangement: Optional[str] = Field(None, max_length=255)
    sporulation: Optional[bool] = None
    metabolism: Optional[str] = Field(None, max_length=500)
    energy_source: Optional[str] = Field(None, max_length=255)
    is_pathogen: Optional[bool] = None

    @field_serializer("optimal_temperature", when_used="json")
    def serialize_optimal_temp_update(self, value: Optional[float]):
        return serialize_float_to_json_safe(value)

    model_config = ConfigDict(from_attributes=True, extra="ignore")


class BacteriaResponseSchema(BacteriaBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class BacteriaPredictionInputSchema(BacteriaBaseSchema):
    pass


class SimilarBacteriaInfoSchema(BacteriaResponseSchema):
    similarity_score: float

    @field_serializer("similarity_score", when_used="json")
    def serialize_similarity(self, value: Optional[float]):
        return serialize_float_to_json_safe(value)


class BacteriaPredictionResponseDataSchema(BaseModel):
    input_bacteria: BacteriaPredictionInputSchema
    is_pathogen_prediction: bool
    pathogen_probability: float
    similar_bacteria: List[SimilarBacteriaInfoSchema] = []

    @field_serializer("pathogen_probability", when_used="json")
    def serialize_patho_prob(self, value: Optional[float]):
        return serialize_float_to_json_safe(value)
