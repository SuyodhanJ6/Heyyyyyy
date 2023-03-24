from sensor.configuration.mongo_db_connection import MongoDBClient

if __name__ == '__main__':
    mondbClient = MongoDBClient()
    print(mondbClient.database.list_collection_names())