
from typing import Optional
from app.services.post_service.post_db.post_db import PostDb
from app.services.post_service.post_db.post_db_services import PostDbServices
from sqlalchemy.orm import Session
from app.app_models.db_models import User
from app.services.post_service import post_schemas 


class PostDbProvider(PostDb):
    
    post_db_services = PostDbServices()
    
    def __init__(self):
        
        pass
    
    def get_all_posts_db(self, db: Session, limit:int, skip:int = 0, search:Optional[str] = ""):
        return self.post_db_services.get_all_posts_db(db = db, limit = limit , skip = skip, search = search)
    
    def create_post_db(self, post: post_schemas.PostBase, current_user: User, db: Session):
        return self.post_db_services.create_post_db(post = post, current_user = current_user, db = db )
    
    def get_post_db(self, id: int, db: Session):
        return self.post_db_services.get_post_db(id = id, db = db)
    
    def delete_post_db(self, id: int, current_user: User, db: Session):
        return self.post_db_services.delete_post_db(id = id, db = db, current_user = current_user)
    
    def update_post_db(self, id: int, current_user: User, post: post_schemas.PostBase, db: Session):
        return self.post_db_services.update_post_db(id = id, current_user = current_user, post = post, db = db)