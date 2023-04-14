from pydantic import BaseModel
from datetime import datetime

class Comment(BaseModel):
    comment_id: int
    replie_to_id: int = -1
    user_id: int
    post_id: int
    user_name: str
    user_profile_img: str
    content: str
    created_at: datetime
    is_published: bool = True
    replies:int = 0
    dislikes:int = -1
    likes:int = -1
    
    
class CommentCreate(BaseModel):
    replie_to_id: int = -1
    content: str
    
class CommentUpdate(BaseModel):
    comment_id: int
    content: str
    
class ReactCreate(BaseModel):
    post_id: int
    comment_id: int
    react: int
    pre_react: int
    
class ReactOut(BaseModel):
    user_id: int
    comment_id: int
    react: int
    likes: int = -1
    dislikes: int = -1
    