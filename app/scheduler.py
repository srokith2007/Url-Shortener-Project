from apscheduler.schedulers.background import BackgroundScheduler
from app.jobs import cleanup_expired_urls

scheduler = BackgroundScheduler()

scheduler.add_job(
    cleanup_expired_urls,
    trigger="interval",
    hours=1
)