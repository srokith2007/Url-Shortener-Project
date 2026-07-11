from datetime import datetime,UTC
from .database import SessionLocal
from app import models

def cleanup_expired_urls():
    db = SessionLocal()

    try:
        db.query(models.Urls).filter(models.Urls.expires_at < datetime.now(UTC)).delete(synchronize_session=False)
        db.commit()
        print("Expired URLs deleted.")
    finally:
        db.close()
