from app.db_holder_dic.database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, text, ForeignKey, ARRAY
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password =  Column(String, nullable=False)
    user_name =  Column(String, nullable=False)
    is_verified = Column(Boolean, server_default='False', nullable=False)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False, server_default=text('now()'))
    phone_number = Column(String)
    profile_img = Column(String)
    
class ExpiredToken(Base):
    
    __tablename__ = 'expired_tokens'
    
    id = Column(Integer, primary_key=True, nullable=False)
    access_token = Column(String, nullable=False, unique=True)
    refresh_token = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False, server_default=text('now()'))
    
    
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    attached_img = Column(String, nullable=True)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    group_id = Column(String, nullable=True, default="none")
    tags = Column(ARRAY(String), nullable=True, default="none") 
    
    
    owner = relationship("User", lazy='subquery')