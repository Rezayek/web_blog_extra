from abc import ABC, abstractmethod

class CommentsDb(ABC):
    
    @abstractmethod
    def get_all_comments_db(self):
        pass
    
    @abstractmethod
    def create_comments_db(self):
        pass
    
    @abstractmethod
    def add_react_db(self):
        pass
    
       
    @abstractmethod
    def delete_comments_db(self):
        pass
    
    @abstractmethod
    def update_comments_db(self):
        pass
    