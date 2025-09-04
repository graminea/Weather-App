from pymongo import MongoClient
from pymongo import server_api

class Database:
    def __init__(self, uri="mongodb+srv://graminea:QNxiFdsrjWY1kXKM@gramineacluster.jywhero.mongodb.net/?retryWrites=true&w=majority&appName=gramineaCluster", db_name="userdata_weather_app"):
        self.client = MongoClient(uri ,serverSelectionTimeoutMS=5000)
        if not self.client.admin.command("ping"):
            raise RuntimeError(f"Could not connect to DB")
            #a = a
        self.db = self.client[db_name]
    
    def get_collection(self, collection_name):
        return self.db[collection_name]

    def insert_one(self, collection_name, document):
        return self.get_collection(collection_name).insert_one(document)

    def find_one(self, collection_name, query):
        return self.get_collection(collection_name).find_one(query)

    def find_many(self, collection_name, query):
        return self.get_collection(collection_name).find(query)

    def update_one(self, collection_name, query, update_values, upsert=False):
        return self.get_collection(collection_name).update_one(query, {'$set' : update_values}, upsert=upsert)

    def delete_one(self, collection_name, query):
        return self.get_collection(collection_name).delete_one(query)
