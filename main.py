from sensor.pipeline.training_pipeline import TrainPipeline
from sensor.exception import SensorException
from sensor.logger import logging
import sys
if __name__ == '__main__':
    try:
        training_pipeline = TrainPipeline()
        training_pipeline.run_data_ingestion_config()
        
    except Exception as e:
        raise logging.info(SensorException(e, sys))
