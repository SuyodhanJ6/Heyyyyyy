import os, sys

from sensor.entity.config_entity import (TrainingPipelineConfig, 
                                         DataIngestionConfig, 
                                         DataValidationConfig,
                                         DataTransformationConfig, 
                                         ModelTrainingConfig,
                                         ModelEvaluationConfig,
                                         ModelPusherConfig)

from sensor.entity.artifact_entity import (DataIngestionArtifact, 
                                           DataValidationArtifact, 
                                           DataTransformationArtifact, 
                                           ModelTrainerArtifact,
                                           ModelEvaluationArtifact,
                                           ModelPusherArtifact)

from sensor.components.data_validation import DataValidation

from sensor.logger import logging
from sensor.exception import SensorException
from sensor.components.data_ingection import DataIngestion
from sensor.components.data_transformation import DataTransformation
from sensor.components.mode_evalution import ModelEvalution
from sensor.components.model_trainer import Model_Trainer
from sensor.components.mode_pusher import ModelPusher


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
    
    def start_data_transformation(self, data_validation_artifact : DataValidationArtifact) -> DataTransformationArtifact:
        try:
            data_transformation_config = DataTransformationConfig()
            data_transformation = DataTransformation(
                data_validation_artifact, data_transformation_config)
            
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            
            return data_transformation_artifact

        except Exception as e:
            raise SensorException(e, sys)
    
    def start_model_trainer(self, data_transformation_artifact : DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            model_trainer_config = ModelTrainingConfig()
            model_transformation = Model_Trainer(data_transformation_artifact, 
                                                 model_trainer_config=model_trainer_config)
            model_trainer_artifact  = model_transformation.initialize_model_trainser()

            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys)
    
    def start_model_evaluation(self,
                               data_validation_artifact:DataValidationArtifact,
                               model_trainer_artifact:ModelTrainerArtifact) -> ModelEvaluationArtifact:
        try:
            model_eval_config = ModelEvaluationConfig()
            model_eval = ModelEvalution(model_eval_config, data_validation_artifact, model_trainer_artifact)
            model_eval_artifact = model_eval.intializig_model_evalution()
            return model_eval_artifact

        except Exception as e:
            raise SensorException(e, sys)
    
    def start_model_pusher(self,
                           mode_trainer_artifact:ModelTrainerArtifact):
        try:
            model_pusher_config = ModelPusherConfig()
            model_pusher = ModelPusher(mode_trainer_artifact, model_pusher_config)
            model_pusher_artifact = model_pusher.initialize_model_pusher()

            return model_pusher_artifact
        except Exception as e:
            raise SensorException(e, sys)
            
    def run_data_ingestion_config(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            
            data_validation_artifact= self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)

            data_transformation_artifact = self.start_data_transformation(data_validation_artifact = data_validation_artifact )

            model_trainser_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)

            model_evalution_artifact = self.start_model_evaluation(data_validation_artifact, model_trainser_artifact)

            if not model_evalution_artifact.is_model_accepted:
                raise Exception("Trained model is not better than the best model")

            model_pusher_artifact = self.start_model_pusher(model_trainser_artifact)
        except Exception as e:
            raise SensorException(e, sys)