from .. redis_client import redis_client

def get_cached_url(short_code: str):
    return redis_client.get(short_code)

def cache_url(short_code: str, long_url: str):
    redis_client.set(short_code, long_url, ex=3600)  # Cache for 1 hour

def delete_cached_url(short_code: str):
    redis_client.delete(short_code)


