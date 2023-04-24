import os,sys
import pandas as pd 
import shutil

from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import ModelEvaluationArtifact,ModelTrainerArtifact, ModelPusherArtifact
from sensor.entity.config_entity import ModelPusherConfig

class ModelPusher:
    def __init__(self, 
                 mode_trainer_artifact:ModelTrainerArtifact,
                 model_pusher_config:ModelPusherConfig):
        try:
            self.mode_trainer_artifact = mode_trainer_artifact
            self.model_pusher_config = model_pusher_config
        except Exception as e:
            raise SensorException(e, sys)
        
    def initialize_model_pusher(self) -> ModelPusherArtifact:
        try:
            logging.info("I'm Entring into initialize_model_pusher and trained_model_path")
            # trained_model_path = self.model_evaluation_artifact.trained_model_path
            trained_model_path = self.mode_trainer_artifact.trained_model_file_path
            # Creating model pusher to save dir 
            model_file_path = self.model_pusher_config.model_file_path
            os.makedirs(os.path.dirname(model_file_path), exist_ok=True)
            shutil.copy(src=trained_model_path, dst=model_file_path)

            # Saved Model Dir 
            saved_model_dir = self.model_pusher_config.saved_model_dir
            os.makedirs(os.path.dirname(saved_model_dir), exist_ok=True)
            shutil.copy(src=trained_model_path, dst=saved_model_dir)

            model_pusher_artifact = ModelPusherArtifact(saved_model_path=saved_model_dir, model_file_path=model_file_path)
            logging.info(f"Model Pusher Artifact: {model_pusher_artifact}" )
            return model_pusher_artifact

        except Exception as e:
            raise SensorException(e, sys)