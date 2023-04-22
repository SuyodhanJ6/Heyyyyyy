import os 
import sys

from sensor.logger import logging
from pandas import DataFrame
from sensor.exception import SensorException
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.data_access.sensor_data import SensorData
from sensor.constant.training_pipeline import SCHEMA_DROP_COLS, SCHEMA_FILE_PATH
from sensor.utils.main_utils import read_yaml_file

from pandas import DataFrame
import pandas as pd
from sklearn.model_selection import train_test_split

class DataIngestion:
    def __init__(
        self, data_ingestion_config: DataIngestionConfig
    ):
        """

        """
        try:
            self.data_ingestion_config = data_ingestion_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise logging.info(SensorException(e, sys))
        
    def export_data_into_feature_store(self) -> DataFrame:
        try:
            # logging.info(f"Exporting data from mongodb")

            # sensor_data = SensorData()

            # dataframe = sensor_data.export_collection_as_dataframe(
            #     collection_name=self.data_ingestion_config.collection_name
            # )
            logging.info("Consider Local csv file")
            dataframe = pd.read_csv("sensor_data.csv")

            logging.info(f"Shape of dataframe: {dataframe.shape}")
            
            dataframe = dataframe.drop(columns=self._schema_config['drop_columns'])
            logging.info(f"Shape of dataframe: {dataframe.shape}")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            dir_path = os.path.dirname(feature_store_file_path)

            os.makedirs(dir_path, exist_ok=True)

            logging.info(
                f"Saving exported data into feature store file path: {feature_store_file_path}"
            )

            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            logging.info(f"Shape of dataframe: {dataframe.shape}")

            
            return dataframe

        except Exception as e:
            raise SensorException(e, sys)
        
        
            
    def splittings_data_as_train_and_test(self, dataframe : DataFrame) -> None:
        logging.info("Starting the train and test splittings")
        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)

            dir_name = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_name, exist_ok=True)
            
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            
        except Exception as e:
            SensorException(e, sys)
            
    def  initiate_data_ingestion(self):
        """
        Method Name: initiate_data_ingestion
        Description: This method initiate the  data ingestion component of the training pipeline
        
        OutPut     : trainig_set and testig_set
        On Failure : Write an exception log and then raise the exception
        
        version    : 1.0
        
        """
        try:
            dataframe = self.export_data_into_feature_store()
            self.splittings_data_as_train_and_test(dataframe)
            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                test_file_path=self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e, sys) 