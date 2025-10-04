from Networksecurity.entity.config_entity import DataValidationConfig
from Networksecurity.entity.artifact_entity import DataIngestionartifact,DataValidationartifact
from Networksecurity.constant.Training_pipeline import SCHEMA_FILE_PATH
from Networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file

from Networksecurity.exception.exception import NetworkSecurityException
from Networksecurity.logging.logger import logging

from scipy.stats import ks_2samp

import pandas as pd
import numpy as np
import os,sys

class DataValidation:
    def __init__(self,ingestion_artifact:DataIngestionartifact,
                data_validation_config:DataValidationConfig):
        try:
            self.ingestion_artifact = ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    # used here static method beacuse this function is used in the same class only
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self._schema_config)
            logging.info(f"requried numbner of columns : {number_of_columns}")
            logging.info(f"Dataframe has columns : {len(dataframe.columns)}")

            if len(dataframe.columns)==number_of_columns:
                return True
            return False

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status = True #assuming no data drift initially
            drift_report ={}

            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1,d2)
                """
                High p-value → distributions are similar
                Low p-value → distributions are different (data drift!)
                """
                if threshold<=is_same_dist.pvalue:
                    is_found = False # no drift
                else:
                    is_found = True # drift detected
                    status = False
                drift_report.update(
                    {column:{
                        "p_value":float(is_same_dist.pvalue),
                        "drift_status" : is_found
                    }})
            
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            # cerate directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)

            write_yaml_file(file_path=drift_report_file_path,content=drift_report)

        except Exception as e:
            raise NetworkSecurityException(e,sys)




    def initiate_data_validation(self)->DataValidationartifact:
        try:

            train_file_path = self.ingestion_artifact.trained_file_path
            test_file_path = self.ingestion_artifact.test_file_path

            # read the data from train and test
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            # Validate number of columns
            status =self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"train dataframe does not contain all columns \n"

            status =self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"test dataframe does not contain all columns \n"
            
            ## check here about numericall columns or not

            ## lets check datadrift
            status = self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,index=False,header=True,
            )

            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path,index=False,header=True,
            )

            data_validation_artifact = DataValidationartifact(
                valiadation_status= status,
                valid_train_file_path=self.ingestion_artifact.trained_file_path,
                valid_test_file_path=self.ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)