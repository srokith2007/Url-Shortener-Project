from typing import Optional,List
from fastapi import FastAPI,status,Response,HTTPException,Depends,APIRouter,Request
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import engine,get_db
from app import models,schemas
from ..utils import encode_id,decode_id
from fastapi.responses import RedirectResponse
from datetime import datetime,UTC
from .. import oauth2
from .. limiter import limiter
from app.cache.url_cache import get_cached_url, cache_url, delete_cached_url
from app.monitoring.timer import Timer


router = APIRouter(
    prefix = "/urls",
    tags = ["Urls"]
)



@router.get("/{short_code}", status_code=status.HTTP_302_FOUND)
@limiter.limit("10/minute")
def get_url(request: Request, short_code: str, db : Session = Depends(get_db)):
    #url cached in redis
    #Timer() for response time in redis
    with Timer() as redis_timer:
        cached_url = get_cached_url(short_code)
    print(f"Redis Time: {redis_timer.elapsed:.2f} ms")
    if cached_url:
        print("✅ CACHE HIT")
        return RedirectResponse(cached_url)
    print("❌ CACHE MISS")

    #Timer() for response time in database
    with Timer() as db_timer:
        url = db.query(models.Urls).filter(models.Urls.short_code == short_code).first()
    print(f"DB Time: {db_timer.elapsed:.2f} ms")

    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"url {short_code} not found")
    if url.expires_at and url.expires_at < datetime.now(UTC):
        raise HTTPException(status_code=status.HTTP_410_GONE, detail=f"url {short_code} has expired")
    #increment click_count
    url.click_count+=1
    db.commit()
    cache_url(short_code,url.url)  
    return RedirectResponse(url=url.url, status_code=status.HTTP_302_FOUND)

#no need to give user_id in url because it is automatically verified in new_url(owner_id==user_id.id)
@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def create_url(request: Request,entered_url: schemas.Url, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    new_url = models.Urls(owner_id=user_id.id, **entered_url.model_dump())
    url_duplication_check = db.query(models.Urls).filter(models.Urls.url==entered_url.url).first()
    if url_duplication_check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="URL already exists")
    db.add(new_url)
    db.flush()
    db.refresh(new_url)
    new_url.short_code = encode_id(new_url.id)
    db.commit()
    return {"message": "URL created successfully", "url": new_url}


@router.delete("/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("5/minute")
def delete_url(request: Request,short_code: str, db: Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):
    url_query = db.query(models.Urls).filter(models.Urls.short_code == short_code)
    url = url_query.first()
    if url==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"URL {short_code} not found")
    if url.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="warning : trying to delete another user's post.")
    url_query.delete(synchronize_session=False)
    db.commit()
    delete_cached_url(short_code)
    return {"message": f"URL with {short_code} deleted successfully"}
