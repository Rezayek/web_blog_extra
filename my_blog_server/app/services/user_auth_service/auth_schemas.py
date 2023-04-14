from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
        
class UserCreate(BaseModel):
    email: EmailStr 
    user_name: str 
    password: str 
    profile_img: str 
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class LogoutToken(BaseModel):
    access_token: str
    refresh_token:str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class LoginToken(Token):
    refresh_token:str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
class EmailVerificationToken(TokenData):
    username: Optional[str] = None
    
class EmailSchema(BaseModel):
    email: List[EmailStr]