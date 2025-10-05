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
PREPROCESSING_OBJECT_FILE_NAME :str = "preprocessing.pkl"

"""
Data Transformation related Constant start with DATA_TRANSFORMATION var name
"""
DATA_TRANSFORMATION_DIR_NAME : str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR : str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR : str ="transformed_object"

## knn imputer class to replace nan values
DATA_TRANSFORMATION_IMPUTER_PARAMS : str ={
        "missing_values" : np.nan,
        "n_neighbors" : 3,
        "weights" : "uniform"
}
