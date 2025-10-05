## for testing purpose of data ingestion

import sys
from Networksecurity.components.data_ingestion import DataIngestion
from Networksecurity.components.data_validation import DataValidation
from Networksecurity.components.data_transformation import DataTransFormation
from Networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig
from Networksecurity.entity.config_entity import DataTransformationConfig
from Networksecurity.exception.exception import NetworkSecurityException
from Networksecurity.logging.logger import logging

if __name__=='__main__':
    try:
        training_pipeline = TrainingPipelineConfig()
        data_ingestion_config= DataIngestionConfig(training_pipeline)
        data_ingestion = DataIngestion(data_ingestion_config)

        logging.info("Initiate the data ingestion")

        dataingestionartifact = data_ingestion.Initiate_data_ingestion()
        logging.info("Data initiation completed")
        print(dataingestionartifact)


        data_validation_config = DataValidationConfig(training_pipeline)
        data_validation = DataValidation(dataingestionartifact,data_validation_config)
        logging.info("data Validation Initiated")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("data validation completed")
        print(data_validation_artifact)


        
        data_transformation_config = DataTransformationConfig(training_pipeline)
        data_transformation = DataTransFormation(data_validation_artifact,data_transformation_config)
        logging.info("started Data Transformation")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info("Completed Data Transformation")

        


    except Exception as e:
        raise NetworkSecurityException(e,sys)