import os
import json
from pymongo import MongoClient
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


def _load_from_startup_config():
    cfg_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'startup_config.json')
    try:
        with open(cfg_path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
        return cfg.get('MONGO_URI')
    except Exception:
        return None


def get_mongo_uri():
    uri = os.environ.get('MONGO_URI')
    if uri:
        return uri
    return _load_from_startup_config() or 'mongodb://localhost:27017'


_client = None


def get_client():
    global _client
    if _client is None:
        uri = get_mongo_uri()
        logger.info(f"Connecting to MongoDB: {uri}")
        _client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    return _client


def get_db():
    client = get_client()
    # use database name from env or default
    db_name = os.environ.get('MONGO_DB', 'railway_analytics')
    return client[db_name]
