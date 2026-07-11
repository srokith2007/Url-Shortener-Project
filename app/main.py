from fastapi import FastAPI
from .database import engine
from . import models
from .routers import urls,users,auth,analytics
from contextlib import asynccontextmanager
from .scheduler import scheduler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from .limiter import limiter
from app.redis_client import redis_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()

    yield

    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)
#models.Base.metadata.create_all(bind=engine)

app.include_router(urls.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(analytics.router)

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.add_middleware(SlowAPIMiddleware)

print(redis_client.ping())