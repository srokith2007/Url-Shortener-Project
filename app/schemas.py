from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic import ConfigDict

class Url(BaseModel):
    url : str
    model_config = ConfigDict(form_attributes=True)

class UrlOut(BaseModel):
    id: int
    url: str
    short_code: str

class UserCreate(BaseModel):
    username : str
    email_id : EmailStr
    password : str

    model_config = ConfigDict(
        from_attributes=True
    )

class UserOut(BaseModel):
    id:int
    username:str
    email_id:EmailStr

    model_config = ConfigDict(
        from_attributes=True
    )

#class UserLogin(BaseModel):
    #email_id : EmailStr
    #password : str

#class Token(BaseModel):
    #access_token : str
    #token_type : str

class TokenData(BaseModel):
    id : Optional[int]