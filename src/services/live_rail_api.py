import os
import requests
from src.utils.cache_utils import cache
from src.utils.logging_config import get_logger

logger = get_logger("live_rail_api")

BASE = os.getenv("LIVE_RAIL_BASE", "https://api.irail.be")
API_KEY = os.getenv("LIVE_RAIL_KEY", "")


def fetch_train_status(train_number: str) -> dict:
    """Fetch live train status from external provider. Results are cached briefly."""
    key = f"train_status:{train_number}"
    if key in cache:
        logger.debug("Cache hit for %s", key)
        return cache[key]

    url = f"{BASE}/trains/{train_number}"
    params = {"api_key": API_KEY} if API_KEY else {}
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        cache[key] = data
        return data
    except Exception as e:
        logger.exception("Failed to fetch live train status for %s: %s", train_number, e)
        raise
