import jwt
from fastapi import Depends
from app.routes.users import oauth2_scheme
from typing import Optional
from datetime import datetime, timedelta,timezone



SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: str, expires_delta: Optional[timedelta] = None):
    '''
    This function is use to encode the input data and return jwt token.
    '''
    to_encode = {"data":data}
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def validate_access_token(token = Depends(oauth2_scheme)):
    '''
    This function is use to verify and jwt token to authenticate the user.
    '''
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if data is None:
            raise Exception("Invalid Access Token!")
        
        return data['data']
    
    except Exception:
        raise Exception("Invalid Access Token!")
