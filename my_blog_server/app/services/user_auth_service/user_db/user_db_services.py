from .user_db import UserDb
from app.app_models.db_models import User, ExpiredToken
from app.services.user_auth_service import auth_schemas
from app.app_utils import password_hash
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from app.services.user_auth_service import oauth2 
from app.firebase_cloud_store.firebase_manager import FirebaseManager
from app.producers_rabbit.notifier import Notifier
class UserDbServices(UserDb):
    
    def __init__(self):
        self.firebase_store_user = FirebaseManager()
        self.notifier = Notifier()
        pass
    
    def login_db(self, username, password, db: Session):
        user = db.query(User).filter(User.email == username).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

        if not password_hash.verify(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

        if not user.is_verified:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"account is not verified")
    
        return user
    
    def logout_db(self, db: Session, expired_tokens: ExpiredToken):
        try:
            db.add(expired_tokens)
            db.commit()
        except:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
        
    def reVerify_db(self, email: str, db: Session):
        
        
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
        if user.is_verified:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Account already verified")
        
        return user
    
    def verify_db(self, user:User, db: Session):
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=f"Already Verified")

        db.query(User).filter(User.id == user.id).update({User.is_verified: True}) 
        self.firebase_store_user.add_new_user(user = user)
        self.notifier.new_user_notifier(body= user)
        self.notifier.new_user_notifier_subDB(body = user)
        db.commit()

        
        
        return user.user_name
        
    def create_user_db(self, user: auth_schemas.UserCreate, db: Session):
        user.password = password_hash.hash(user.password)
        try:
            new_user = User(**(user.dict()))
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User Already exists")
        
        return new_user
        
    def get_user_db(self, id:int, db: Session):
        user = db.query(User).filter(User.id == id).first()
    
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user id: {id} not found")
        
        return user
    
    
    def refresh_token_db(self, current_user: User):
        
        try:
            
            access_token = oauth2.create_access_token(data={"user_id": current_user.id},)
            return access_token
        
        except:
            raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= f"could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
        