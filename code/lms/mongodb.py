from pymongo import MongoClient
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class MongoDBClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            mongo_uri = f"mongodb://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@{settings.MONGO_HOST}:{settings.MONGO_PORT}/"
            cls._instance = MongoClient(mongo_uri)
            cls.db = cls._instance[settings.MONGO_DB_NAME]
            logger.info("Connected to MongoDB")
        return cls._instance

    @classmethod
    def get_db(cls):
        if cls._instance is None:
            cls()
        return cls.db

def get_activity_collection():
    return MongoDBClient.get_db()['activity_logs']

def get_analytics_collection():
    return MongoDBClient.get_db()['learning_analytics']