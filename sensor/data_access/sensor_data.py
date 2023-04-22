import os,sys
from typing import Optional
from sensor.logger import logging

import pandas as pd
import numpy as np

from sensor.exception import SensorException
from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.constant.database import DATABASE_NAME

class SensorData:
    """
    This class help to export entire Mongo DB records to pandas data frame.
    """
    
    def __init__(self):
        try:
            logging.info("We are in SensorData class")
            logging.info(f"We got the Database Name")
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise SensorException(e, sys)
        
    def export_collection_as_dataframe(
        self, collection_name: str, database_name: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Method Name : export_collection_as_dataframe
        Description : This method will exports all collections as dataframe
        OutPut      : pd.DataFrame
        OnFailure   : raise and exception
        """ 
        try:
            """
            export entire collectin as dataframe:
            return pd.DataFrame of collection
            """
            if database_name is None:
                collection = self.mongo_client.database[collection_name]

            else:
                collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            df.replace({"na": np.nan}, inplace=True)

            return df

        except Exception as e:
            raise SensorException(e, sys)

