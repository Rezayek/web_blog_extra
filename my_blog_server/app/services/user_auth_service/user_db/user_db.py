from abc import ABC, abstractmethod

class UserDb(ABC):
    
    @abstractmethod
    def login_db(self):
        pass
    
    @abstractmethod
    def logout_db(self):
        pass
    
    @abstractmethod
    def verify_db(self):
        pass
    
    @abstractmethod
    def reVerify_db(self):
        pass
    
    @abstractmethod
    def create_user_db(self):
        pass
    
    @abstractmethod
    def get_user_db(self):
        pass
    
    @abstractmethod
    def refresh_token_db(self):
        pass
    
    