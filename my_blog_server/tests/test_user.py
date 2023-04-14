import os
import sys
# Get the path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the path of the parent directory to the system path
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)
from requests_toolbelt.multipart.encoder import MultipartEncoder
from app.services.user_auth_service.auth_schemas import UserOut, Token
from app.app_models.db_models import User
from app.config_env import settings
from jose import jwt
import pytest

def test_create_user(client_auth, session):
   # Create a dictionary to hold the form data
    data = {"user_email": "yomyfriendhh@gmail.com", "user_name": "rezayek", "password": "0000"}

    # Open the image file in binary mode and add it to the form data as a file
    profile_img_file = open('test_images/336790892_3346830845568109_6083365218015350012_n.jpg', 'rb')
    files = {'profile_img': ('336790892_3346830845568109_6083365218015350012_n.jpg', profile_img_file)}

    # Send the POST request with the form data
    res = client_auth.post("/auth/create_user", data=data, files=files)
    
    res_dict = res.json()
    session.query(User).filter(User.id == res_dict['id']).update({User.is_verified: True})
    session.commit()
    assert UserOut(**res_dict).email == "yomyfriendhh@gmail.com"
    assert res.status_code == 201
    
def test_login(client_auth, test_user):
     
    res = client_auth.post("/auth/login", data = {"username": test_user['email'], "password":test_user['password']})
    login_res = Token(**res.json())
    payload = jwt.decode(login_res.access_token , settings.secret_key, algorithms = [settings.algorithm])
    id : str = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200



@pytest.mark.parametrize("email, password, status_code",{
    ('dummy_email', 'dummy_email', 403)
 })   
def test_incorrect_login(client_auth, test_user, email, password, status_code):
    res = res = client_auth.post("/auth/login", data = {"username": email, "password":password})
    assert res.status_code == status_code