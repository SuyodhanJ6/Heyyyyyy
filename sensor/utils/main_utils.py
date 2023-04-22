import os, sys

from sensor.exception import SensorException
from sensor.logger import logging

import yaml

def read_yaml_file(file_path: str) -> dict:
    """
    Method Name : read_yaml_file
    Description : Reads a YAML file and parses it into a dictionary.
    OutPut      : dict: The dictionary parsed from the YAML file.
    On Failure  : Raise an exception
    """
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise SensorException(e, sys)
    


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    """
    Method Name : write_yaml_file
    Description : Writes a YAML file
    OutPut      : dict: The dictionary parsed from the YAML file
    On Failure  : Raise an exception
    """
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as file:
            yaml.dump(content, file)

    except Exception as e:
        raise SensorException(e, sys)
    
    
    