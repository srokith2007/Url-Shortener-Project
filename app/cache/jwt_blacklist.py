from app.redis_client import redis_client


def blacklist_token(token: str, ttl: int):
    redis_client.set(f"blacklist:{token}", 1, ex=ttl)

def is_blacklisted(token: str) -> bool:
    return redis_client.exists(f"blacklist:{token}") == 1