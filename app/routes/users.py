from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from app.database import get_db
from app.schema import User
from app.models import Users

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")
from app.utils.jwt_auth import create_access_token #to avoid circular import

@router.post("/register/v1")
def userRegister(body: User,db: Session = Depends(get_db)):
    '''
    This endpoint is use to register a new user.
    '''
    if db.query(Users).filter_by(username=body.username).first():
        raise HTTPException(status_code=409,detail="user already present!")
    
    user_obj = Users(username=body.username, hash_password=pwd_context.hash(body.password))
    db.add(user_obj)
    db.commit()
    return {"status":True,"message":"registration successful!"}

@router.post("/login/v1")
def userLogin(body: User,db: Session = Depends(get_db)):
    '''
    This endpoint is use to get the user loggedin and obtain jwt token which user can use to access other protected endpoints.
    '''
    user_obj = db.query(Users).filter_by(username=body.username).first()
    if not user_obj:
        raise HTTPException(status_code=400,detail="No user found!")
    
    if not pwd_context.verify(body.password,user_obj.hash_password):
        raise HTTPException(status_code=400,detail="Invalid password entered!")
    
    access_token = create_access_token(data=user_obj.username)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = user_obj = db.query(Users).filter_by(username=form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = access_token = create_access_token(data=user_obj.username)
    return {"access_token":access_token, "token_type":"bearer"}

