from pymongo import MongoClient
import os
from src.utils.logging_config import get_logger

logger = get_logger("mongo_client")


def get_mongo_client():
    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        # trigger server selection now
        client.server_info()
        return client
    except Exception as e:
        logger.exception("Failed to connect to MongoDB: %s", e)
        raise


def get_db(name: str = None):
    client = get_mongo_client()
    dbname = name or os.getenv("MONGO_DB", "railway")
    return client[dbname]
