import os
import requests
from cachetools import TTLCache, cached
from src.utils.logging_config import get_logger

logger = get_logger(__name__)

# simple in-memory TTL cache for API responses
_cache = TTLCache(maxsize=256, ttl=30)


@cached(_cache)
def fetch_live_train_info(train_no: str) -> dict:
    """
    Fetch live train info from a public/live API. This is pluggable; uses env LIVE_API_BASE.
    Caching is applied to reduce external calls.
    """
    base = os.environ.get('LIVE_API_BASE', 'https://rly.example.com/api')
    api_key = os.environ.get('LIVE_API_KEY')
    url = f"{base}/train/{train_no}/status"
    headers = {}
    if api_key:
        headers['Authorization'] = f"Bearer {api_key}"
    try:
        resp = requests.get(url, headers=headers, timeout=8)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        logger.exception('Failed to fetch live train info')
        # return a consistent error payload rather than raising so callers can choose
        return {"error": str(e)}
