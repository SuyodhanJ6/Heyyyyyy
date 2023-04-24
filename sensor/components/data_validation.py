import json
import sys,os
from pandas import DataFrame
import pandas as pd 
from scipy.stats import ks_2samp

from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sensor.entity.config_entity import DataValidationConfig
from sensor.utils.main_utils import read_yaml_file, write_yaml_file

from sensor.exception import SensorException
from sensor.logger import logging


class DataValidation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig,
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e, sys)
        
    
    @staticmethod
    def read_data(file_path:str):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e, sys)
        
    def validate_number_of_columns(self, dataframe: DataFrame) -> bool:
        """
        Method Name : validate_number_of_columns
        Description : Validates the number of columns in the input DataFrame against the expected number of columns
                        defined in the schema configuration.
        OutPut      : None
        On Failure  : ValueError: If the number of columns in the input DataFrame does not match the expected number
                        of columns defined in the schema configuration.
        """
        try:
            number_of_columns = len(self._schema_config["columns"])
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Data frame has columns: {len(dataframe.columns)}")
            if len(dataframe.columns)==number_of_columns:
                return True
            return False
        except Exception as e:
            raise SensorException(e,sys)
        
        
    def is_numerical_column_exist(self, df: DataFrame) -> bool:
        """
        Method Name  : is_numerical_column_exist
        Description  : This function check numerical column is present in dataframe or not.
        OutPut       : bool (True if all column presents else False)
        On Failure   : raise and exception 
        """
        try:
            dataframe_columns = df.columns

            status = True

            missing_numerical_columns = []

            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    status = False

                    missing_numerical_columns.append(column)

            logging.info(f"Missing numerical column: {missing_numerical_columns}")

            return status

        except Exception as e:
            raise SensorException(e, sys) from e
        
    def drop_columns(self, dataframe: DataFrame):
        """
        """
        try:
            logging.info("Entering in drop_columns function")
            drop_columns_schema = self._schema_config['drop_columns']
            logging.info(f"drop_columns_schema {drop_columns_schema}")
            dataframe_columns = dataframe.columns
            logging.info(f"dataframe_columns {dataframe_columns}")
            for column in self._schema_config['drop_columns']:
                if column  in dataframe_columns:
                    dataframe.drop(column, inplace=True)
                    
            dir_name = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_name, exist_ok=True)
                    
        except Exception as e:
            SensorException(e, sys)
       
    def missing_value(self, train_file_path: str, test_file_path: str)-> DataFrame:
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)
        
    
    def detect_dataset_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold: float = 0.05) -> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1, d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({
                    column: {
                        "p_value": float(is_same_dist.pvalue),
                        "drift_status": is_found
                    }
                })
            
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            
            # Create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)
            
            return status
        
        except Exception as e:
            raise SensorException(e, sys)


    def initialize_data_validation(self):
        """
        
        """
        try:
            error_message = ""
            ## Train and test file path 
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path  = self.data_ingestion_artifact.test_file_path
            
            ## Reading dataframe from train_file_path and test_file_path
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe  = DataValidation.read_data(test_file_path)
                
            
            # Valid Numerical Column
            status = self.is_numerical_column_exist(train_dataframe)
            logging.info(f"Valid Numerical Column : {status}")
            if not status:
                error_message = f"{error_message} TrainData Frame does not contain all numerical columns."
                
            status = self.is_numerical_column_exist(test_dataframe)
            if not status:
                error_message = f"{error_message} TestData Frame does not contain all numerical columns."
                
            # Valid Number of Columns
            status = self.validate_number_of_columns(dataframe=train_dataframe)    
            if not status:
                error_message = f"{error_message} TrainData Frame does not contain all Columns vai Schema File."
                
            status = self.validate_number_of_columns(dataframe=test_dataframe)    
            if not status:
                error_message = f"{error_message} TestData Frame does not contain all Columns vai Schema File."
            
            
            if len(error_message) > 0:
                raise Exception(error_message)
            # Check data drift 
            status = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")

            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys)