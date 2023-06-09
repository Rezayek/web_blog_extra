
from fastapi import status, HTTPException, Response
from typing import Optional
from app.services.post_service.post_db.post_db import PostDb
from sqlalchemy.orm import Session
from sqlalchemy import or_, cast, String
from app.app_models.db_models import User, Post
from app.services.post_service.post_schemas import PostBase
from app.firebase_cloud_store.firebase_manager import FirebaseManager
from app.producers_rabbit.notifier import Notifier
from app.services.post_service.post_db.post_tag_db.post_db_tag_provider import PostDbTagProvider 
class PostDbServices(PostDb):
    
    def __init__(self):
        self.firebase_store_post = FirebaseManager()
        self.notifier = Notifier()
        self.post_db_tag_provider = PostDbTagProvider() 
        pass
    
    def get_all_posts_db(self, db: Session, limit:int, skip:int = 0, search:Optional[str] = ""):
        
        # results = db.query(Post).group_by(Post.id).filter(or_(Post.title.contains(search), cast(Post.tags, String).like(f"%{search}%"))).limit(limit).offset(skip).all()
        results = list()
        if search != "":
            tag_search = self.post_db_tag_provider.get_all_posts_db(tag = search, limit= limit, skip = skip)
            results.extend(tag_search)
        else: 
            results = db.query(Post).group_by(Post.id).filter(Post.title.contains(search), cast(Post.tags, String).like(f"%{search}%")).limit(limit).offset(skip).all()
        
        return results
    
    def create_post_db(self, post: PostBase, current_user: User, db: Session):
        
        try:
            new_added_post = Post(owner_id = current_user.id, **post.dict())
            
            db.add(new_added_post)
            
            
            # post_sub = Post(owner_id = current_user.id, **post.dict())
            # post_sub.id = new_added_post.id

            db.commit()
            db.refresh(new_added_post)
            self.post_db_tag_provider.create_post_db(new_post = new_added_post, tags = new_added_post.tags)
            self.firebase_store_post.add_new_post(post = new_added_post)
            self.notifier.new_post_notifier(body= new_added_post)
            
        except:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Service is down")
        
        return new_added_post
    
    def get_post_db(self, id: int, db: Session):
        
        post = db.query(Post).filter(Post.id == id).first()

        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {id} not found")
            
        return post
    
    def delete_post_db(self, id: int, current_user: User, db: Session):
        
        post_query = db.query(Post).filter(Post.id == id)
        post = post_query.first()
        
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {id} not found")
        
        if post.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized")
        
        post_query.delete(synchronize_session=False)
        
        if post.tags != []:
            self.post_db_tag_provider.delete_post_db(id = id, current_user= current_user, tags = post.tags )
            
        db.commit()
        
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    def update_post_db(self, id: int, current_user: User, post: PostBase, db: Session):
        
        post_query = db.query(Post).filter(Post.id == id)
        post_res = post_query.first()

        if not post_res:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {id} not found")
        
        if post_res.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized")

        post_query.update(post.dict(), synchronize_session=False)
        

        self.post_db_tag_provider.update_post_db(id = id, current_user = current_user, post = post, tags = post.tags)
        
        db.commit()
        
        return post_query.first()
    