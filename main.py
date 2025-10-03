## for testing purpose of data ingestion

import sys
from Networksecurity.components.data_ingestion import DataIngestion
from Networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
from Networksecurity.exception.exception import NetworkSecurityException
from Networksecurity.logging.logger import logging

if __name__=='__main__':
    try:
        training_pipeline = TrainingPipelineConfig()
        data_ingestion_config= DataIngestionConfig(training_pipeline)
        data_ingestion = DataIngestion(data_ingestion_config)

        logging.info("Initiate the data ingestion")

        dataingestionartifact = data_ingestion.Initiate_data_ingestion()

        print(dataingestionartifact)
    except Exception as e:
        raise NetworkSecurityException(e,sys)