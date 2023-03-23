import pymongo
from sensor.constant.database import DATABASE_NAME
import certifi
ca = certifi.where()

class MongoDBClient:
    client = None
    def __init__(self, database_name = DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_client = "mongodb+srv://Prashant:Prashant@cluster0.v7zxaoi.mongodb.net/mydb?retryWrites=true&w=majority"
                MongoDBClient.client = pymongo.MongoDBClient(mongo_db_client, tlsCAFile=ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
        except Exception as e:
            raise e