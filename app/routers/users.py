from fastapi import FastAPI,status,Response,HTTPException,Depends,APIRouter,Request
from typing import List
from app import models,schemas,utils
from ..database import engine,get_db
from sqlalchemy.orm import Session
from .. import oauth2
from .. limiter import limiter
router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

#register user
@router.post("/register",status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
@limiter.limit("5/minute")
def create_user(request: Request, user:schemas.UserCreate, db : Session = Depends(get_db)):

    new_user = models.User(**user.model_dump())
    user_duplication_check_username = db.query(models.User).filter(models.User.username==user.username).first()
    if user_duplication_check_username:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username already exists")
    user_duplication_check_email_id = db.query(models.User).filter(models.User.email_id==user.email_id).first()
    if user_duplication_check_email_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email_id already exists")
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    print(new_user)
    db.add( new_user)
    db.commit()
    db.refresh( new_user)
    return  new_user




#get user info
@router.get("/{id}", response_model=schemas.UserOut)    
@limiter.limit("5/minute")                  
def get_user(request: Request, id:int, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):

    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found with this id")
    if current_user.id != id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to access another user's account."
        )
    return user

#get urls created by user
@router.get("/{id}/urls", response_model=List[schemas.UrlOut])
@limiter.limit("5/minute")
def get_user_urls(request: Request, id:int, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found with this id")
    if current_user.id != id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to access another user's account."
        )
    urls = db.query(models.Urls).filter(models.Urls.owner_id==id).all()
    if not urls:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no urls found for this user")
    return urls

#delete user using id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("5/minute")
def delete_user(request: Request, id:int, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).filter(models.User.id==id)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found with this id")
    if current_user.id != id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to delete another user's account."
        )
    user_query.delete(synchronize_session=False)
    db.commit()
    return {"message": f"user with {id} deleted successfully"}