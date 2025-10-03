## Flow
"""
1. Data fetch from MongoDB database
2. Creating Feature Store(inside artifact) Having the dataset fetched from Db
3. Train Test Split i.e spliiting of the dataset
4. inside Ingested folder store the test and train data(inside artifact)
"""
import sys
import os
import pandas as pd
import numpy as np
import pymongo
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv

from Networksecurity.exception.exception import NetworkSecurityException
from Networksecurity.logging.logger import logging

## configuration Of data ingestion
from Networksecurity.entity.config_entity import DataIngestionConfig
from Networksecurity.entity.artifact_entity import DataIngestionartifact

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    ## 1. function for collecting the data from the mongodb doc to dataframe
    def export_collection_as_dataframe(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))

            ## to drop column of id created by mongodb
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"],axis=1)

            ##replace nan values 
            df.replace({"na" : np.nan},inplace=True)

            ## return dataframe
            return df
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
## 2. Data red from the mongodb now storing it to the artifact
    def export_data_to_feature_store(self,datafrme:pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            #createing the folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            datafrme.to_csv(feature_store_file_path,index=False,header=True)
            return datafrme
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    ## 3 and 4. spliting the data and storing
    def splitting_data(self,dataframe: pd.DataFrame):
        try:
            train_set,test_set = train_test_split(
                dataframe,test_size=self.data_ingestion_config.train_test_split_ratio,random_state=42
            )
            logging.info("Train Test split done")

            logging.info("exited from method Splitting_data of data ingestion class")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)

            logging.info("Exporting data to Train and test file under ingested under artifact")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path,index=False,header=True
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path,index=False,header=True
            )

            logging.info("exported train and test file path")

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def Initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_to_feature_store(dataframe)
            self.splitting_data(dataframe)
            dataingestionartifact = DataIngestionartifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path= self.data_ingestion_config.testing_file_path
                )
            
            return dataingestionartifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

