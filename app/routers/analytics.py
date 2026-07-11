from typing import Optional,List
from fastapi import FastAPI,status,Response,HTTPException,Depends,APIRouter,Request
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import engine,get_db
from app import models,schemas
from datetime import datetime,UTC
from .. import oauth2
from .. limiter import limiter


router = APIRouter(
    prefix = "/analytics",
    tags = ["Analytics"]
)

@router.get("/users/{id}")
@limiter.limit("5/minute")
def get_users_analytics(request: Request, id:int, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    if(current_user.id!=id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to access another user's account.")
    total_urls = db.query(models.Urls).filter(models.Urls.owner_id==id).count()
    total_clicks = (db.query(func.sum(models.Urls.click_count)).filter(models.Urls.owner_id==id).scalar() or 0)
    urls = db.query(models.Urls).filter(models.Urls.owner_id==id).all()
    url_list = []
    for url in urls:
        url_list.append({"short_code " : url.short_code, "click_count " : url.click_count})
    return{"total_urls " : total_urls,
           "total_clicks " : total_clicks,
           "url_details " : url_list}

def get_current_admin(current_user:models.User = Depends(oauth2.get_current_user)):
    if current_user.is_admin==False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="admin access denied")
    return current_user


@router.get("/admin")
@limiter.limit("10/minute")
def get_admin_analytics(request: Request, db: Session = Depends(get_db), admin:models.User = Depends(get_current_admin)):
    total_users = db.query(models.User).count()
    total_urls = db.query(models.Urls).count()
    total_clicks = (db.query(func.sum(models.Urls.click_count)).scalar() or 0)

    return{"total_users": total_users,
           "total_urls": total_urls,
           "total_clicks": total_clicks}