import logging
import os
from typing import Any, Dict, List, Optional, Tuple

import joblib
import numpy as np
import pandas as pd
from app.core.config import settings
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


class BacteriaModelServiceSingleton:
    _instance: Optional["BacteriaModelServiceSingleton"] = None
    model: Any = None
    preprocessor: Any = None
    feature_names_in_: Optional[List[str]] = None

    def __new__(cls):
        if cls._instance is None:
            logger.info("Creating new BacteriaModelService instance")
            cls._instance = super(BacteriaModelServiceSingleton, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized") or not self._initialized:
            self._load_model_and_preprocessor()
            self._initialized = True

    def _load_model_and_preprocessor(self):
        """Load the trained model and preprocessor."""
        model_path_from_settings = settings.ML_MODEL_PATH

        model_full_path = os.path.join("/app", model_path_from_settings)

        model_paths_to_try = [model_full_path]

        logger.info(f"Attempting to load model from paths: {model_paths_to_try}")

        for path_attempt in model_paths_to_try:
            if os.path.exists(path_attempt):
                try:
                    logger.info(f"Loading model from: {path_attempt}")
                    pipeline = joblib.load(path_attempt)

                    if hasattr(pipeline, "named_steps"):
                        self.preprocessor = pipeline.named_steps.get("preprocessor")
                        self.model = pipeline.named_steps.get("classifier")

                        if not self.preprocessor and hasattr(pipeline, "steps"):
                            steps_dict = {step[0]: step[1] for step in pipeline.steps}
                            self.preprocessor = steps_dict.get("preprocessor")
                            self.model = steps_dict.get("classifier")

                    elif isinstance(pipeline, tuple) and len(pipeline) == 2:
                        self.preprocessor, self.model = pipeline

                    else:
                        logger.warning(
                            f"Pipeline structure at {path_attempt} not standard named_steps. Assuming it's the model directly or needs specific handling."
                        )

                    if self.model and self.preprocessor:
                        logger.info("Model and preprocessor loaded successfully.")
                        if hasattr(self.preprocessor, "feature_names_in_"):
                            self.feature_names_in_ = list(
                                self.preprocessor.feature_names_in_
                            )
                        return
                    else:
                        logger.error(
                            f"Could not extract model or preprocessor from {path_attempt}. Preprocessor: {self.preprocessor is not None}, Model: {self.model is not None}"
                        )

                except Exception as e:
                    logger.error(
                        f"Error loading model from {path_attempt}: {e}", exc_info=True
                    )
            else:
                logger.warning(f"Model file not found at: {path_attempt}")

        logger.error("Failed to load model from any specified path.")

    def _prepare_input_data(self, bacteria_data: Dict[str, Any]) -> pd.DataFrame:
        """Converts input dict to a DataFrame, ensuring correct column order if feature_names_in_ is set."""
        df = pd.DataFrame([bacteria_data])
        if self.feature_names_in_:
            for col in self.feature_names_in_:
                if col not in df.columns:
                    df[col] = np.nan
            df = df[self.feature_names_in_]
        return df

    def preprocess_data(self, bacteria_data: Dict[str, Any]) -> np.ndarray:
        if not self.preprocessor:
            logger.error("Preprocessor not loaded. Cannot preprocess data.")
            raise ValueError("Preprocessor not loaded")

        df_input = self._prepare_input_data(bacteria_data)

        try:
            X_processed = self.preprocessor.transform(df_input)
            return X_processed
        except Exception as e:
            logger.error(f"Error during data preprocessing: {e}", exc_info=True)
            logger.error(f"Input data causing error: {bacteria_data}")
            raise ValueError(f"Error preprocessing data: {e}")

    def predict_pathogenicity(self, bacteria_data: Dict[str, Any]) -> Tuple[int, float]:
        if not self.model:
            logger.error("Model not loaded. Cannot make predictions.")
            raise ValueError("Model not loaded")

        X_processed = self.preprocess_data(bacteria_data)

        try:
            prediction = self.model.predict(X_processed)[0]
            probability = self.model.predict_proba(X_processed)[0]

            pathogen_prob = (
                float(probability[1])
                if len(probability) > 1 and int(self.model.classes_[1]) == 1
                else float(probability[0])
            )

            return int(prediction), pathogen_prob
        except Exception as e:
            logger.error(f"Error during prediction: {e}", exc_info=True)
            raise ValueError(f"Error making prediction: {e}")

    def find_similar_bacteria(
        self,
        input_bacteria_data: Dict[str, Any],
        all_bacteria_dicts: List[Dict[str, Any]],
        n_similar: int = 5,
    ) -> List[Dict[str, Any]]:
        if not self.preprocessor or not all_bacteria_dicts:
            logger.warning(
                "Preprocessor not loaded or no existing bacteria data provided for similarity search."
            )
            return []

        try:
            X_input_processed = self.preprocess_data(input_bacteria_data)

            all_bacteria_df = pd.DataFrame(all_bacteria_dicts)

            if self.feature_names_in_:
                for col in self.feature_names_in_:
                    if col not in all_bacteria_df.columns:
                        all_bacteria_df[col] = np.nan
                all_bacteria_df_ordered = all_bacteria_df[self.feature_names_in_]
            else:
                logger.warning(
                    "feature_names_in_ not available for preprocessor. Column order for all_bacteria_df might be inconsistent."
                )
                all_bacteria_df_ordered = all_bacteria_df

            X_all_processed = self.preprocessor.transform(all_bacteria_df_ordered)

            similarities = cosine_similarity(X_input_processed, X_all_processed)[0]

            bacteria_with_similarity = []
            for i, bact_dict in enumerate(all_bacteria_dicts):
                bact_copy = bact_dict.copy()
                bact_copy["similarity_score"] = float(similarities[i])
                bacteria_with_similarity.append(bact_copy)

            sorted_similar_bacteria = sorted(
                bacteria_with_similarity,
                key=lambda x: x["similarity_score"],
                reverse=True,
            )

            return sorted_similar_bacteria[
                : min(n_similar, len(sorted_similar_bacteria))
            ]

        except Exception as e:
            logger.error(f"Error finding similar bacteria: {e}", exc_info=True)
            return []


model_service = BacteriaModelServiceSingleton()
