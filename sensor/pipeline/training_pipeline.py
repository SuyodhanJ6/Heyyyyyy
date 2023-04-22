import os, sys

from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig

from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact

from sensor.components.data_validation import DataValidation

from sensor.logger import logging
from sensor.exception import SensorException
from sensor.components.data_ingection import DataIngestion

import pandas as pd 
from sklearn.model_selection import train_test_split


class TrainPipeline:
    def ___init__(self):
        
        self.training_pipeline_config = TrainingPipelineConfig()
        
        
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info(
                "Entered the start_data_ingestion method of TrainPipeline class"
            )
            
            self.data_ingestion_config = DataIngestionConfig
            logging.info("Starting data ingestion")
            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config
            )
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data ingestion completed and artifact: {data_ingestion_artifact}")
            # return data_ingestion_artifact
            return data_ingestion_artifact
        
        except Exception as e:
            raise logging.info(f"this error due to {SensorException(e, sys)}") 
        
    def start_data_validation(self, data_ingestion_artifact : DataIngestionArtifact) -> DataValidationArtifact:
        try:
            # data_validation_config = DataValidationConfig(training_pipeline_config=TrainingPipelineConfig())
            data_validation_config = DataValidationConfig()
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact, 
                                            data_validation_config=data_validation_config)
            data_validation_artifact = data_validation.initialize_data_validation()
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys)
    
    def start_data_transformation(self):
        pass
    
    def start_model_trainer(self):
        pass
    
    def start_model_evaluation(self):
        pass
    
    def start_model_pusher(self):
        pass
            
    def run_data_ingestion_config(self):
        try:
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            
            data_validation_artifact: DataValidationArtifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
        except Exception as e:
            raise SensorException(e, sys)