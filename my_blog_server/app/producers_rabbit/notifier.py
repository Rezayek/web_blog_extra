import os
import sys
# Get the path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the path of the parent directory to the system path
parent_dir = os.path.abspath(os.path.join(current_dir, '../../../..'))
sys.path.append(parent_dir)
from .producer import producer_post, producer_user, producer_user_sub
from app.debugger_file import set_up_logger
from app.config_env import settings
from app.app_models.db_models import User, Post


def singleton(class_instance):
    instances = {}
    def get_instance(*args, **kwargs):
        if class_instance not in instances:
            instances[class_instance] = class_instance(*args, **kwargs)
        return instances[class_instance]
    return get_instance

@singleton
class Notifier:
    def __init__(self):
        self.user_log = set_up_logger(file_name= settings.log_user_producer) 
        self.post_log = set_up_logger(file_name= settings.log_post_producer) 
        
    
    
    def new_user_notifier(self, body: User):
        producer_user(body= {"id": body.id , "user_name": body.user_name })
        self.user_log.debug(f"/*sending new user to group and vote micro-services with id: {body.id}")
    
    def new_post_notifier(self, body: Post):
        producer_post(body= {"id": body.id, "title": body.title})
        self.post_log.debug(f"sending new post to vote and recomendation micro-services with id: {body.id}")
        
    def new_user_notifier_subDB(self, body: User):
        producer_user_sub(
            body = {
                "id": body.id, 
                "email": body.email, 
                "password": body.password, 
                "user_name": body.user_name, 
                "is_verified": body.is_verified,
                "phone_number": body.phone_number,
                "profile_img": body.profile_img
                }
            )
        self.user_log.debug(f"/*/*sending new user to post micro-services with id: {body.id}")
