import os
import sys
import ast
# Get the path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the path of the parent directory to the system path
parent_dir = os.path.abspath(os.path.join(current_dir, '../../../../..'))
sys.path.append(parent_dir)



from fastapi import status, HTTPException
from app.services.post_service.post_db.post_tag_db.post_db_tag import PostDbTag
from sqlalchemy.orm import Session
from sqlalchemy import or_, cast, String
from sqlalchemy.orm import Session
from app.app_models.db_models import User, Post
from app.services.post_service.post_schemas import PostBase
from app.producers_rabbit.notifier import Notifier
from app.services.post_service.post_db.post_tag_db.post_tag_connectors.database_global_connector import DBConnector




class PostDbTagServices(PostDbTag):
    
    def __init__(self):

        self.notifier = Notifier()
        self.tags = ["action", "new"]

        pass

    
    def add_new_user(self, user_data: User):
        try:
            for tag in self.tags:
                
                with DBConnector(tag = tag) as db:
                    # Create a new instance of User model for each session
                    user = User()
                    # Set attributes on the new instance manually
                    user.id = user_data.id
                    user.email = user_data.email
                    user.password = user_data.password
                    user.user_name = user_data.user_name
                    user.is_verified = user_data.is_verified
                    user.phone_number = user_data.phone_number
                    user.profile_img = user_data.profile_img
                    db.add(user)
                    db.commit()  # Commit changes to the current database

                        
            return True
        except Exception as e :
            print(e)
            return False
        
    
    def get_all_posts_db(self, tag: str, limit:int, skip:int = 0):
        
        results = list()
        with DBConnector(tag = tag) as db:
            
            results = db.query(Post).group_by(Post.id).filter(cast(Post.tags, String).like(f"%{tag}%")).limit(limit).offset(skip).all()
        
        
        return results
    
    def create_post_db(self, tags: str, new_post: Post):
        
        for tag in tags:

            with DBConnector(tag = tag) as db:
            
                try:
                    clone = Post()
                    clone.id = new_post.id
                    clone.title = new_post.title
                    clone.content = new_post.content
                    clone.attached_img = new_post.attached_img
                    clone.published = new_post.published
                    clone.created_at = new_post.created_at
                    clone.owner_id = new_post.owner_id
                    clone.group_id = new_post.group_id
                    clone.tags = new_post.tags
                    db.add(clone)
                    db.commit()
                except:
                    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Service is down")
        
        # return new_post
    
    def get_post_db(self, tag: str, id: int):
        
        with DBConnector(tag = tag) as db:
            
            post = db.query(Post).filter(Post.id == id).first()

            if not post:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {id} not found")
                
            return post
    
    def delete_post_db(self, tags: str, id: int, current_user: User):
        
        for tag in tags:
            
            with DBConnector(tag = tag) as db:
                
                post_query = db.query(Post).filter(Post.id == id)
                post = post_query.first()
                
                if not post:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {id} not found")
                
                if post.owner_id != current_user.id:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized")
                
                post_query.delete(synchronize_session=False)
                db.commit()

        # return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    def update_post_db(self, tags: str, id: int, current_user: User, post: PostBase):
        
        for tag in tags:
                        
            with DBConnector(tag = tag) as db:

                post_query = db.query(Post).filter(Post.id == id)
                post_res = post_query.first()

                if not post_res:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {id} not found")
                
                if post_res.owner_id != current_user.id:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized")
                
                post_query.update(post.dict(), synchronize_session=False)
                db.commit()

        # return post_query.first()
    
    
    