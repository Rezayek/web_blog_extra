from abc import ABC, abstractmethod

class PostDb(ABC):
    
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
    