import logging
import math
import os
import re
import sys

import pandas as pd
from app.db.session import Base, SessionLocal, engine
from app.models.bacteria import (
    Bacteria,
)
from sqlalchemy import func
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.orm import Session

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

CSV_FILE_PATH = "/app/data/mimedb_microbes_v1.csv"


def create_tables(db_engine):
    logger.info("Creating database tables...")
    try:
        Base.metadata.create_all(bind=db_engine)
        logger.info("Database tables created successfully or already exist.")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}", exc_info=True)
        raise


def clean_value(value_from_csv_cell):
    str_value = str(value_from_csv_cell).strip()
    if pd.isna(value_from_csv_cell) or str_value.lower() in [
        "not available",
        "na",
        "n/a",
        "",
        "#n/a",
        "nan",
        "<na>",
        "null",
    ]:
        return None
    return str_value


def clean_boolean(value_from_csv_cell):
    val_str = str(value_from_csv_cell).strip().lower()
    if val_str in [
        "true",
        "yes",
        "1",
        "present",
        "positive",
        "y",
        "pathogenic",
    ]:
        return True
    if val_str in [
        "false",
        "no",
        "0",
        "absent",
        "negative",
        "n",
        "non-pathogenic",
    ]:
        return False
    if clean_value(value_from_csv_cell) is None:
        return None
    logger.debug(f"Unrecognized boolean value '{value_from_csv_cell}', returning None.")
    return None


def clean_float(value_from_csv_cell):
    val_str = clean_value(value_from_csv_cell)
    if val_str is None:
        return None
    try:
        f_value = None
        match = re.search(r"([-+]?\d*\.?\d+([eE][-+]?\d+)?)", val_str)
        if match:
            f_value = float(match.group(1))
        else:
            f_value = float(val_str)

        if math.isfinite(f_value):
            return f_value
        else:
            logger.debug(
                f"Original CSV value '{value_from_csv_cell}', cleaned string '{val_str}', converted to non-finite float ({f_value}), returning None."
            )
            return None
    except ValueError:
        logger.debug(
            f"Could not convert string '{val_str}' (original CSV: '{value_from_csv_cell}') to float, returning None."
        )
        return None


def populate_from_csv(db: Session):
    logger.info(f"Attempting to populate database from CSV: {CSV_FILE_PATH}")
    if not os.path.exists(CSV_FILE_PATH):
        logger.error(f"CSV file not found at {CSV_FILE_PATH}. Skipping population.")
        return

    try:
        df = pd.read_csv(
            CSV_FILE_PATH, low_memory=False, dtype=str, keep_default_na=False
        )
        logger.info(f"Loaded CSV with {len(df)} rows.")
    except Exception as e:
        logger.error(f"Error reading CSV file {CSV_FILE_PATH}: {e}", exc_info=True)
        return

    column_mapping = {
        "microbe_id": "bacteria_id",
        "name": "name",
        "superkingdom": "superkingdom",
        "kingdom": "kingdom",
        "phylum": "phylum",
        "klass": "class_name",
        "order": "order",
        "family": "family",
        "genus": "genus",
        "species": "species",
        "strain": "strain",
        "gram": "gram_stain",
        "shape": "shape",
        "mobility": "mobility",
        "flagella_presence": "flagellar_presence",
        "number_of_membranes": "number_of_membranes",
        "oxygen_requirement": "oxygen_preference",
        "optimal_temperature": "optimal_temperature",
        "temperature_range": "temperature_range",
        "habitat": "habitat",
        "biotic_relationship": "biotic_relationship",
        "cell_arrangement": "cell_arrangement",
        "sporulation": "sporulation",
        "metabolism": "metabolism",
        "energy_source": "energy_source",
        "human_pathogen": "is_pathogen",
    }

    bacteria_to_insert = []
    processed_rows_count = 0
    skipped_duplicates_in_csv_count = 0
    successfully_inserted_count = 0
    error_during_insert_count = 0
    seen_bacteria_ids_in_csv = set()

    logger.debug(f"Original DataFrame columns from CSV: {df.columns.tolist()}")
    valid_model_keys = {column.name for column in Bacteria.__table__.columns}
    logger.debug(f"Valid Bacteria model attribute names: {valid_model_keys}")

    for index, row_series in df.iterrows():
        processed_rows_count += 1

        raw_bacteria_id_from_csv = row_series.get("microbe_id", "")
        bacteria_id = clean_value(raw_bacteria_id_from_csv)

        if not bacteria_id:
            if processed_rows_count < 20:
                logger.warning(
                    f"Skipping CSV row {index + 2} due to missing/invalid bacteria_id (from CSV 'microbe_id', raw: '{raw_bacteria_id_from_csv}')."
                )
            elif processed_rows_count == 20:
                logger.warning(
                    "Further 'missing bacteria_id' warnings will be suppressed for this run."
                )
            continue

        if bacteria_id in seen_bacteria_ids_in_csv:
            logger.warning(
                f"Skipping CSV row {index + 2} - duplicate bacteria_id '{bacteria_id}' within CSV file."
            )
            skipped_duplicates_in_csv_count += 1
            continue
        seen_bacteria_ids_in_csv.add(bacteria_id)

        current_bacteria_data = {"bacteria_id": bacteria_id}

        for csv_col_name, model_attr_key in column_mapping.items():
            if model_attr_key == "bacteria_id":
                continue

            if csv_col_name not in df.columns:
                if index < 5:
                    logger.debug(
                        f"Row {index + 2}, bacteria_id {bacteria_id}: CSV column '{csv_col_name}' for model attribute '{model_attr_key}' not found. Will be None."
                    )
                current_bacteria_data[model_attr_key] = None
                continue

            raw_value_from_csv = row_series.get(csv_col_name, "")

            if model_attr_key in [
                "mobility",
                "flagellar_presence",
                "sporulation",
                "is_pathogen",
            ]:
                current_bacteria_data[model_attr_key] = clean_boolean(
                    raw_value_from_csv
                )
            elif model_attr_key == "optimal_temperature":
                current_bacteria_data[model_attr_key] = clean_float(raw_value_from_csv)
            elif model_attr_key == "gram_stain":
                cleaned_val = clean_value(raw_value_from_csv)
                if cleaned_val:
                    if "positive" in cleaned_val.lower():
                        current_bacteria_data[model_attr_key] = "Positive"
                    elif "negative" in cleaned_val.lower():
                        current_bacteria_data[model_attr_key] = "Negative"
                    elif "variable" in cleaned_val.lower():
                        current_bacteria_data[model_attr_key] = "Variable"
                    else:
                        current_bacteria_data[model_attr_key] = cleaned_val
                else:
                    current_bacteria_data[model_attr_key] = None
            else:
                current_bacteria_data[model_attr_key] = clean_value(raw_value_from_csv)

        filtered_data_for_model = {
            k: v for k, v in current_bacteria_data.items() if k in valid_model_keys
        }

        if successfully_inserted_count == 0 and index < 5:
            logger.debug(
                f"Row {index + 2} (bacteria_id: {bacteria_id}): Prepared data for DB: {filtered_data_for_model}"
            )

        bacteria_to_insert.append(filtered_data_for_model)

        if len(bacteria_to_insert) >= 500:
            logger.info(
                f"Attempting to commit batch of {len(bacteria_to_insert)} records..."
            )
            try:
                db.execute(Bacteria.__table__.insert(), bacteria_to_insert)
                db.commit()
                successfully_inserted_count += len(bacteria_to_insert)
                logger.info(
                    f"Committed batch. Total inserted so far: {successfully_inserted_count}"
                )
            except (IntegrityError, DataError) as e:
                db.rollback()
                logger.error(
                    f"Error during batch insert: {e}. This batch of {len(bacteria_to_insert)} records will be skipped."
                )
                error_during_insert_count += len(bacteria_to_insert)
            except Exception as e:
                db.rollback()
                logger.error(f"Unexpected error committing batch: {e}", exc_info=True)
                error_during_insert_count += len(bacteria_to_insert)
            bacteria_to_insert = []

    if bacteria_to_insert:
        logger.info(
            f"Attempting to commit final batch of {len(bacteria_to_insert)} records..."
        )
        try:
            db.execute(Bacteria.__table__.insert(), bacteria_to_insert)
            db.commit()
            successfully_inserted_count += len(bacteria_to_insert)
            logger.info(
                f"Committed final batch. Total inserted: {successfully_inserted_count}"
            )
        except (IntegrityError, DataError) as e:
            db.rollback()
            logger.error(
                f"Error during final batch insert: {e}. This batch of {len(bacteria_to_insert)} records will be skipped."
            )
            error_during_insert_count += len(bacteria_to_insert)
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error committing final batch: {e}", exc_info=True)
            error_during_insert_count += len(bacteria_to_insert)

    logger.info(
        f"CSV Population Summary: \n"
        f"  Total CSV rows processed: {processed_rows_count}\n"
        f"  Successfully inserted into DB: {successfully_inserted_count}\n"
        f"  Skipped (duplicates within CSV file): {skipped_duplicates_in_csv_count}\n"
        f"  Skipped (DB insert errors/data issues for batches): {error_during_insert_count}"
    )


def init_initial_data():
    db: Session = SessionLocal()
    try:
        create_tables(engine)

        bacteria_count = db.query(func.count(Bacteria.id)).scalar()
        if bacteria_count == 0:
            logger.info("Bacteria table is empty. Proceeding with CSV population.")
            populate_from_csv(db)
        else:
            logger.info(
                f"Bacteria table already contains {bacteria_count} records. CSV population skipped."
            )
            logger.info(
                "To re-populate from CSV, ensure the 'bacteria' table is empty (e.g., by running `make clean` which removes volumes, then `make up` and `make init-db`)."
            )

    except Exception as e:
        logger.error(f"An error occurred during initial data setup: {e}", exc_info=True)
    finally:
        db.close()


if __name__ == "__main__":
    logger.info("Starting database initialization process (from app.db.init_db)...")
    init_initial_data()
    logger.info("Database initialization process completed.")
