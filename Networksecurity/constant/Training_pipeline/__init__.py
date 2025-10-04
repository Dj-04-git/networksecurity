import os
import sys
import pandas as pd
import numpy as np

"""
Defining common constant variable for training pipeline 
"""

TARGET_COLUMN = "Result"
PIPELINE_NAME : str = "Networksecurity"
ARTIFACT_DIR : str = "Artifact"
FILE_NAME : str = "phishingData.csv"

TRAIN_FILE_NAME : str = "train.csv"
TEST_FILE_NAME : str = "test.csv"

SCHEMA_FILE_PATH :str = os.path.join("data_schema","schema.yaml")

"""
Data ingestion related constatnt start with DATA_INGESTION VAR NAME
"""

DATA_INGESTION_COLLECTION_NAME = "Network"
DATA_INGESTION_DATABASE_NAME = "Network_Security_ETL"
DATA_INGESTION_DIR_NAME : str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR : str = "feature_store"
DATA_INGESTION_INGESTED_DIR : str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO : float = 0.2

"""
Data validation Related constant start with DATA_VALIDATION var name
"""
DATA_VALIDATION_DIR_NAME : str = "data_validation"
DATA_VALIDATION_VALID_DIR : str = "validated"
DATA_VALIDATION_INVALID_DIR : str = "Invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR : str = "Drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME : str = "Drift_report.yaml"
