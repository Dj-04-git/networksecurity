from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

import pandas as pd
import numpy as np
import os,sys

from Networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object
from Networksecurity.constant.Training_pipeline import (TARGET_COLUMN,DATA_TRANSFORMATION_IMPUTER_PARAMS)
from Networksecurity.entity.artifact_entity import (DataTransformationArtifact,DataValidationartifact)
from Networksecurity.entity.config_entity import DataTransformationConfig
from Networksecurity.exception.exception import NetworkSecurityException
from Networksecurity.logging.logger import logging

class DataTransFormation:
    def __init__(self,data_validation_artifact:DataValidationartifact,data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact: DataValidationartifact = data_validation_artifact
            self.data_transformation_config : DataTransformationConfig = data_transformation_config

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def get_data_transformer_object(cls)-> Pipeline:
        """
        Initialize KNN imputer object with the parameters specifird in the Training_pipeline.py file and returns A pipeline Object

        args :
            cls : DataTransFormation

        return :
            A Pipeline object
        """
        logging.info("entered_get_transformed_object method of DataTrasnformation Class")
        try:
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"initialize knn imputer with parameters : {DATA_TRANSFORMATION_IMPUTER_PARAMS}")

            processor: Pipeline = Pipeline([("imputer",imputer)])

            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)

        
    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info("Entered into data Transformation initiat method")
        try:
            train_df = DataTransFormation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransFormation.read_data(self.data_validation_artifact.valid_test_file_path)

            ## training Dataset
            input_feature_train_df = train_df.drop(columns=TARGET_COLUMN,axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            ### as there is -1 and 1 to clssify we will replace -1 to 0 for training model
            target_feature_train_df = target_feature_train_df.replace(-1,0)

            ## testing dataset
            input_feature_test_df = train_df.drop(columns=TARGET_COLUMN,axis=1)
            target_feature_test_df = train_df[TARGET_COLUMN]
            ### as there is -1 and 1 to clssify we will replace -1 to 0 for training model
            target_feature_test_df = target_feature_train_df.replace(-1,0)

            ## imputer
            logging.info("Going into Imputer")
            preprocessor = self.get_data_transformer_object()
            transformed_input_feature_train_df = preprocessor.fit_transform(input_feature_train_df)
            transformed_input_feature_test_df = preprocessor.transform(input_feature_test_df)

            ## joining dependent and independent feature
            logging.info("np.c_ is used to join the target with dependent feature for training")

            train_arr = np.c_[transformed_input_feature_train_df,np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_feature_test_df,np.array(target_feature_test_df)]

            ##  save numpy array data to file
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr,)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr,)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor,)

            ## preparing artifacts
            data_trasformation_artifact = DataTransformationArtifact(
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
            )

            return data_trasformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)