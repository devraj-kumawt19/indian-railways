"""Services package."""
# Try to import cache manager if it exists
try:
    from src.services.cache_manager import CacheManager
    __all__ = ['CacheManager']
except ImportError:
    __all__ = []