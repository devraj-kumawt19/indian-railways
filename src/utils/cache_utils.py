from cachetools import TTLCache

# Simple shared TTL cache for API responses and lookups
cache = TTLCache(maxsize=1024, ttl=300)

def get_cache():
    return cache
