from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

class MongoConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            uri = str(os.getenv("MONGODB_URI"))
            cls._instance.client = MongoClient(uri)
        return cls._instance

    def __init__(self, db_name, collection):
        self.db = self.client[db_name]
        self.collection = self.db[collection]

    def close_connection(self):
        self.client.close()
