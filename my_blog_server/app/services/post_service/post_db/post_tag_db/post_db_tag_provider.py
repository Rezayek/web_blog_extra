from app.services.post_service.post_db.post_tag_db.post_db_tag import PostDbTag
from app.services.post_service.post_db.post_tag_db.post_db_tag_service import PostDbTagServices
from app.services.post_service import post_schemas 
from app.app_models.db_models import User, Post



def singleton(class_instance):
    instances = {}
    def get_instance(*args, **kwargs):
        if class_instance not in instances:
            instances[class_instance] = class_instance(*args, **kwargs)
        return instances[class_instance]
    return get_instance

@singleton

class PostDbTagProvider(PostDbTag):
    
    post_db_tag_services = PostDbTagServices()
    
    def __init__(self):
        
        pass
    
    def add_new_user(self, user_data: User):
        return self.post_db_tag_services.add_new_user(user_data = user_data)
    
    def get_all_posts_db(self, tag: str, limit:int, skip:int = 0):
        return self.post_db_tag_services.get_all_posts_db(tag = tag, limit = limit , skip = skip)
    
    def create_post_db(self,new_post: Post, tags: str):
        return self.post_db_tag_services.create_post_db(tags = tags, new_post = new_post)
    
    def get_post_db(self, id: int, tag: str):
        return self.post_db_tag_services.get_post_db(id = id, tag = tag)
    
    def delete_post_db(self, id: int, current_user: User, tags: str):
        return self.post_db_tag_services.delete_post_db(id = id, tags = tags, current_user = current_user)
    
    def update_post_db(self, id: int, current_user: User, post: post_schemas.PostBase, tags: str):
        return self.post_db_tag_services.update_post_db(id = id, current_user = current_user, post = post, tags = tags)