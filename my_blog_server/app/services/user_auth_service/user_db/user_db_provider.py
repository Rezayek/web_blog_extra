from app.services.user_auth_service.user_db.user_db import UserDb
from app.services.user_auth_service.user_db.user_db_services import UserDbServices
from sqlalchemy.orm import Session
from app.app_models.db_models import User, ExpiredToken
from app.services.user_auth_service import auth_schemas
class UserDbProvider(UserDb):
    
    user_db_services = UserDbServices()
    
    def __init__(self):
        pass
    
    def login_db(self, username, password, db: Session):
        return self.user_db_services.login_db(username = username, password = password, db = db)
        
    def logout_db(self, db: Session, expired_tokens: ExpiredToken):
        self.user_db_services.logout_db(expired_tokens = expired_tokens, db = db)
    
    def reVerify_db(self, email, db: Session):
        return self.user_db_services.reVerify_db(email =email, db = db)
    
    def verify_db(self, user:User, db: Session):
        return self.user_db_services.verify_db(user = user, db = db)
      
    def create_user_db(self, user: auth_schemas.UserCreate, db: Session):
        return self.user_db_services.create_user_db(user = user, db = db)
        
    def get_user_db(self, id:int, db: Session):
        return self.user_db_services.get_user_db(id = id, db = db)
    
    def refresh_token_db(self, current_user: User):
        return self.user_db_services.refresh_token_db(current_user = current_user)