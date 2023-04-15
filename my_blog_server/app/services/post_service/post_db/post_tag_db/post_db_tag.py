from abc import ABC, abstractmethod

class PostDbTag(ABC):
    

    @abstractmethod
    def add_new_user(self):
        pass
    
    @abstractmethod
    def get_all_posts_db(self):
        pass
    
    @abstractmethod
    def create_post_db(self):
        pass
    
    @abstractmethod
    def get_post_db(self):
        pass
        
    @abstractmethod
    def delete_post_db(self):
        pass
    
    @abstractmethod
    def update_post_db(self):
        pass
    