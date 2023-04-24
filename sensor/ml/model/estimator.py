from sensor.constant.training_pipeline import *
import os
import datetime

class TargetValueMapping:
    def __init__(self):
        
        self.neg: int = 0

        self.pos: int = 1

    def to_dict(self):
        return self.__dict__

    def reverse_mapping(self):
        mapping_response = self.to_dict()

        return dict(zip(mapping_response.values(), mapping_response.keys()))
    

class SensorModel:

    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise e
    
    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise e
        

class ModelResolver:
    def __init__(self, model_dir:str = SAVED_MODEL_DIR):
        self.model_dir = model_dir
    
    def get_best_model_path(self):
        # Get all saved model files in the directory
        model_files = os.listdir(self.model_dir)
        model_files = [f for f in model_files if f.endswith('.pkl')]

        if not model_files:
            return None

        # Sort the model files by their modification time
        model_files = sorted(model_files, key=lambda f: os.path.getmtime(os.path.join(self.model_dir, f)), reverse=True)

        # Get the most recently modified model file
        best_model_path = os.path.join(self.model_dir, model_files[0])
        
        # Add a timestamp to the filename
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        best_model_path_with_timestamp = f"{best_model_path[:-4]}_{timestamp}.pkl"
        
        return best_model_path_with_timestamp

    def is_model_exits(self):
        try:
            # First check the folder is avilable or not 
            if not os.path.exists(self.model_dir):
                return False

            # Check if the model file exists
            model_files = os.listdir(self.model_dir)
            model_files = [f for f in model_files if f.endswith('.pkl')]
            if not model_files:
                return False
            
            timestamp = os.listdir(self.model_dir)
            if len(timestamp) == 0:
                return False
            return True 
        except Exception as e:
            raise e