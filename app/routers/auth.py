from fastapi import Depends,HTTPException,status,APIRouter,Response,Request,BackgroundTasks,Query
from sqlalchemy.orm import Session
from .. import database,schemas,models,utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. limiter import limiter
from app.cache.jwt_blacklist import blacklist_token
from datetime import datetime,UTC
from jose import JWTError,jwt
from app.configs import settings
from app.database import get_db
from app.oauth2 import verify_email_verification_token,create_password_reset_token,verify_password_reset_token
from app.email.service import send_email
from app.email.templates import welcome_email,password_reset_email,password_reset_success_email

router = APIRouter(tags = ["authentication"])

@router.post("/login")
@limiter.limit("5/minute")
def login(request: Request, user_credentials : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email_id==user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Please verify your email before logging in.")
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

@router.get("/auth/verify-email")
def verify_email(token: str = Query(...), background_tasks: BackgroundTasks=None, db: Session = Depends(get_db)):

    email = verify_email_verification_token(token)

    user = db.query(models.User).filter(
        models.User.email_id == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.is_verified:
        return {
            "message": "Email already verified."
        }

    user.is_verified = True

    db.commit()
    db.refresh(user)

    body = welcome_email(user.username)

    background_tasks.add_task(
        send_email,
        recipients=[user.email_id],
        subject="Welcome to RO-KI URL Shortener!",
        body=body
    )

    return {
        "message": "Email verified successfully."
    }


@router.post("/auth/forgot-password")
def forgot_password(
    request: Request,
    background_tasks: BackgroundTasks,
    user: schemas.ForgotPassword,
    db: Session = Depends(get_db)
):

    db_user = db.query(models.User).filter(
        models.User.email_id == user.email_id
    ).first()

    if db_user:
        token = create_password_reset_token(db_user.email_id)

        link = f"{settings.base_url}/auth/reset-password?token={token}"

        body = password_reset_email(
            name=db_user.username,
            reset_link=link
        )

        background_tasks.add_task(
            send_email,
            recipients=[db_user.email_id],
            subject="Reset your password",
            body=body
        )

    return {
        "message": "If an account exists, a password reset link has been sent."
    }


@router.post("/auth/reset-password")
def reset_password(user: schemas.ResetPassword, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):

    email = verify_password_reset_token(user.token)
    db_user = db.query(models.User).filter(
        models.User.email_id == email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db_user.password = utils.hash(user.new_password)
    db.commit()
    body = password_reset_success_email(db_user.username)
    background_tasks.add_task(
    send_email,
    recipients=[db_user.email_id],
    subject="Your password has been changed",
    body=body
    )

    return {"message": "Password reset successful"}