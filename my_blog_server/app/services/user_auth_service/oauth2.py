from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config_env import settings
from app.app_models.db_models import ExpiredToken, User
from app.db_holder_dic.database import get_db
from app.services.user_auth_service.auth_schemas import TokenData, EmailVerificationToken

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS = settings.refresh_token_expire_days

def create_refresh_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    
    return encoded_jwt
    
def create_access_token(data: dict):

    try:
        to_encode = data.copy()
        
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
        
        return encoded_jwt
    except:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= f"could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
        
    
def verify_access_token(token: str, cred_exception):
    try:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        
        id : str = payload.get("user_id")
        
        
        if not id:
            raise cred_exception
        
        token_data = TokenData(id = id)
        
        
    except JWTError:
        raise cred_exception
    
    
    return token_data
   
def get_current_user(token: str = Depends(oauth2_scheme), db: Session =  Depends(get_db)):
    
    cred_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= f"could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    expired_token = db.query(ExpiredToken).filter((ExpiredToken.access_token == token) | (ExpiredToken.refresh_token == token)).first()  
    if expired_token:
        raise cred_exception
    
    token_data = verify_access_token(token, cred_exception)
    user = db.query(User).filter(User.id == token_data.id).first()
    return user

def verify_email_token(token: str, cred_exception):
    try:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        print(payload)
        id : str = payload.get("user_id")
        username = payload.get("user_name")
        if not id or not username  :
            raise cred_exception
         
        token_data = EmailVerificationToken(id = id, username= username)
        
        
    except JWTError:
        raise cred_exception
     
    return token_data

def get_unverified_user(token: str, db: Session =  Depends(get_db)):
    cred_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= f"could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token_data = verify_email_token(token, cred_exception)
    user = db.query(User).filter(User.id == token_data.id).first()
    return user