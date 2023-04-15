import firebase_admin
from firebase_admin import credentials, firestore
from app.config_env import settings
from app.debugger_file import set_up_logger
from app.app_models.db_models import User, Post
from fastapi import status, HTTPException
from app.firebase_cloud_store.firebase_connector import firebase_db
def singleton(class_instance):
    instances = {}
    def get_instance(*args, **kwargs):
        if class_instance not in instances:
            instances[class_instance] = class_instance(*args, **kwargs)
        return instances[class_instance]
    return get_instance


@singleton
class FirebaseManager:
    
    def __init__(self):
        self.user_logger = set_up_logger(file_name= settings.log_fire_user)
        self.post_logger = set_up_logger(file_name= settings.log_fire_post)
        firestore_db = firebase_db
        self.collection_user = firestore_db.collection(u'user')
        self.collection_posts = firestore_db.collection(u'posts')
        
    
    
    def add_new_user(self, user: User):
        
        try:
            
            user_doc =  self.collection_user.document(f'{user.id}')
            user_dict = {
                "id": user.id,
                "email": user.email,
                "user_name": user.user_name,
                "is_verified": user.is_verified,
                "created_at": user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "phone_number": user.phone_number,
                "profile_img": user.profile_img,
            }
            user_doc.set(user_dict)
            self.user_logger.debug(f"Adding user with id: {user.id} to user collection in firebase with document id: {user.id}")
        except Exception as e:
            self.user_logger.debug(f"Failled to add user with id: {user.id} to user collection in firebase error : {e}")
            
    def add_new_post(self, post: Post):
        
        try:
            post_doc =  self.collection_posts.document(str(post.id))
            post_dict = {
                "id": post.id,
                "title": post.title,
                "published": post.published,
                "owner_id": post.owner_id,
                "group_id": post.group_id,
                "tags":post.tags,
                "comments_total":0
            }
            post_doc.set(post_dict)
            post_doc.collection(u'comments').document("0").set({"init_comment": "empty"})
            self.post_logger.debug(f"Adding post with id: {post.id} to post collection in firebase with document id: {post.id}")
        except Exception as e:
            self.post_logger.debug(f"Failled to add post with id: {post.id} to post collection in firebase error : {e}")
           
        
        