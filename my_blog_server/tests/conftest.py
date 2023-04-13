import os
import sys
# Get the path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the path of the parent directory to the system path
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config_env import settings
from app.db_holder_dic.database import get_db, Base
from app.services.user_auth_service.auth_micro import auth_service
from app.services.post_service.post_micro import posts_service
from app.services.comments_service.comments_micro import comments_service
from app.services.user_auth_service.oauth2 import create_access_token
from app.app_models.db_models import User, Post
import pytest

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

testingSessionLocal = sessionmaker(autocommit = False, autoflush= False, bind= engine)


Base.metadata.create_all(bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = testingSessionLocal()
    try:
        yield db
    finally:
        db.close()
               
@pytest.fixture()
def client_auth(session):

    
    
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
            
    auth_service.dependency_overrides[get_db] =   override_get_db 
    
    yield TestClient(auth_service)
    
@pytest.fixture()
def client_post(session):

    
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
            
    posts_service.dependency_overrides[get_db] =   override_get_db 
    
    yield TestClient(posts_service)
    
@pytest.fixture()
def client_comment():
    yield TestClient(comments_service)

@pytest.fixture
def test_user(client_auth, session):
    # Create a dictionary to hold the form data
    data = {"user_email": "yomyfriendhh@gmail.com", "user_name": "rezayek", "password": "0000"}

    # Open the image file in binary mode and add it to the form data as a file
    profile_img_file = open('test_images/336790892_3346830845568109_6083365218015350012_n.jpg', 'rb')
    files = {'profile_img': ('336790892_3346830845568109_6083365218015350012_n.jpg', profile_img_file)}

    # Send the POST request with the form data
    res = client_auth.post("/auth/create_user", data=data, files=files)
    new_user = res.json()
    session.query(User).filter(User.id == new_user['id']).update({User.is_verified: True})
    session.commit()
    
    assert res.status_code == 201
    
    new_user['password'] = data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client_auth, token):
    client_auth.headers = {
        **client_auth.headers,
        "Authorization": f"Bearer {token}"
    }
    
    return client_auth

@pytest.fixture
def authorized_client_post(client_post, token):
    client_post.headers = {
        **client_post.headers,
        "Authorization": f"Bearer {token}"
    }
    
    return client_post

@pytest.fixture
def unauthorized_client_post(client_post):
    client_post.headers = {
        **client_post.headers,
        "Authorization": f"Bearer sdgsdgqdgqsdbsdqgnzerngezbtnetjsykyjte h  "
    }
    
    return client_post

@pytest.fixture
def authorized_client_comment(client_comment, token):
    client_comment.headers = {
        **client_comment.headers,
        "Authorization": f"Bearer {token}"
    }
    
    return client_comment

@pytest.fixture
def unauthorized_client_comment(client_comment, token):
    client_comment.headers = {
        **client_comment.headers,
        "Authorization": f"Bearer ffffffffffffffffffffffffff"
    }
    
    return client_comment

@pytest.fixture
def test_post(test_user, session):
    posts_data = [
        
            {
                "title":"post 1 ",
                "content": "content content content ",
                "owner_id": test_user['id'],
                "tags": ["action", "horror"],
                "group_id": "none",
                "attached_img": "B-removebg-preview.png",
                
            },
            
            {
                "title":"post 2 ",
                "content": "content content content content content ",
                "owner_id": test_user['id'],
                "tags": ["youtube", "news"],
                "group_id": "none",
                "attached_img": "B-removebg-preview.png",
            }
        
    ]
    
    def create_post_model(post):
        return Post(**post)
    
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    session.query(Post).all()
    
    return posts

@pytest.fixture
def test_add_comments(test_post, test_user):
    pass

@pytest.fixture
def test_image():
    # Open the image file in binary mode and add it to the form data as a file
    profile_img_file = open('test_images/336790892_3346830845568109_6083365218015350012_n.jpg', 'rb')
    files = {'post_img': ('336790892_3346830845568109_6083365218015350012_n.jpg', profile_img_file)}
    return files