import base62
from passlib.context import CryptContext

def encode_id(id: int):
    return base62.encode(id)

def decode_id(short_code: str):
    return base62.decode(short_code)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto") 

def hash(password : str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)