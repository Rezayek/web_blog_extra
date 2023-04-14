from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

class PostBase(BaseModel):
    title: str
    content: str
    attached_img: str = "none"
    published: bool = True  
    group_id: str = "none"
    tags: List[str] = []
    
class UserOut(BaseModel):
    id: int
    user_name: str
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id:int
    
    owner: UserOut
    
    class Config:
        orm_mode = True
        