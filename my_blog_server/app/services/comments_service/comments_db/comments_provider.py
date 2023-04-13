
from app.services.comments_service.comments_db.comments_db import CommentsDb
from app.services.comments_service.comments_db.comments_services import CommentsDbServices
from google.cloud.firestore_v1.client import Client
from app.services.comments_service import comments_schemas
from typing import Type
from app.app_models.db_models import User
class CommentsDbProvider(CommentsDb):
    
    commentsDbServices = CommentsDbServices()
    
    def __init__(self):
        
        pass
    
    def get_all_comments_db(self, id:int, reply_to:int, limit:int, skip:int):
        return self.commentsDbServices.get_all_comments_db(id = id, reply_to = reply_to, limit = limit, skip = skip)
    

    def create_comments_db(self, id:int, comment_create : comments_schemas.CommentCreate, current_user: User):
        return self.commentsDbServices.create_comments_db(id = id, comment_create = comment_create, current_user = current_user)
    

    def add_react_db(self, react_create: comments_schemas.ReactCreate, current_user: User ):
        return self.commentsDbServices.add_react_db(react_create= react_create, current_user= current_user )     

    def delete_comments_db(self):
        return self.commentsDbServices.delete_comments_db()
    

    def update_comments_db(self, id:int, comment_update : comments_schemas.CommentUpdate, current_user: User):
        return self.commentsDbServices.update_comments_db(id = id, comment_update = comment_update, current_user = current_user)