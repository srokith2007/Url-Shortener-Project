from fastapi import Depends,HTTPException,status,APIRouter,Response,Request
from sqlalchemy.orm import Session
from .. import database,schemas,models,utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. limiter import limiter
from app.cache.jwt_blacklist import blacklist_token
from datetime import datetime,UTC
from jose import JWTError,jwt
from app.configs import settings

router = APIRouter(tags = ["authentication"])

@router.post("/login")
@limiter.limit("5/minute")
def login(request: Request, user_credentials : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email_id==user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    access_token = oauth2.create_access_token(data = {"user_id" : user.id})

    return{"access_token":access_token , "token_type":"bearer"}



@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(request: Request, current_user: models.User = Depends(oauth2.get_current_user)):

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )
    try:
        scheme, token = auth_header.split()
        if scheme.lower() != "bearer":
            raise ValueError
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header"
        )

    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    exp = payload["exp"]
    remaining_seconds = exp - int(datetime.now(UTC).timestamp())
    if remaining_seconds > 0:
        blacklist_token(token, remaining_seconds)

    return {"message": "Logged out successfully"}