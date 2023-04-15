import os
import sys
# Get the path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the path of the parent directory to the system path
parent_dir = os.path.abspath(os.path.join(current_dir, '../../..'))
sys.path.append(parent_dir)

from click import File
from fastapi import Form, UploadFile, status, Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from app.services.user_auth_service import auth_schemas, oauth2, email_serder
from app.db_holder_dic.database import get_db
from app.app_models.db_models  import User, ExpiredToken
from app.services.user_auth_service.user_db.user_db_provider import UserDbProvider
from app.config_env import settings

import shutil
import os

user_db_provider = UserDbProvider()

auth_service = FastAPI()

# add CORS middleware to allow cross-origin requests
auth_service.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@auth_service.post('/auth/login', response_model= auth_schemas.LoginToken)
async def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = user_db_provider.login_db(username = user_cred.username, password = user_cred.password, db = db)

    # create Token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    refresh_token = oauth2.create_refresh_token(data={"user_id": user.id})
    
    return  auth_schemas.LoginToken(access_token= access_token, token_type= "bearer", refresh_token= refresh_token)

@auth_service.post('/auth/logout', status_code=status.HTTP_200_OK)
async def logout(tokens: auth_schemas.LogoutToken, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user) ):
    
    user_db_provider.logout_db(expired_tokens= ExpiredToken(**tokens.dict()), db = db)
    
    return {"message": "logged out"}

@auth_service.post('/auth/refresh_token', response_model= auth_schemas.Token)
async def refresh_token(current_user: User = Depends(oauth2.get_current_user)):
    
    access_token = user_db_provider.refresh_token_db(current_user)

    return  auth_schemas.Token(access_token= access_token, token_type= "bearer")

@auth_service.post('/auth/reverify')
async def demand_verification(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = user_db_provider.reVerify_db(email = user_cred.username, db = db)

    await email_serder.send_email(auth_schemas.EmailSchema(email=[user.email]), instance=user)
    
    return {"message": "Check your email to verify your account"}


templates = Jinja2Templates(directory="app/templates")

@auth_service.get('/auth/verification/', response_class=HTMLResponse)
def email_verification(request: Request, user: User = Depends(oauth2.get_unverified_user), db: Session = Depends(get_db), timeout: int = 45):
    
    
    user_name = user_db_provider.verify_db(user = user, db = db)
    if user_name:
    
        return templates.TemplateResponse("verification.html", {"request": request, "user_name": user_name})
    
    return {"message": "verification link expired"}
   

@auth_service.post("/auth/create_user", status_code=status.HTTP_201_CREATED, response_model= auth_schemas.UserOut)
async def create_suser(
    user_email: str = Form(...),
    user_name: str = Form(...),
    password: str = Form(...),
    profile_img: UploadFile = File(None),
    db: Session = Depends(get_db),
    timeout: int = 60
    ):
    
            
    user = auth_schemas.UserCreate(email= user_email, user_name= user_name, password= password, profile_img= profile_img.filename)
    new_user = user_db_provider.create_user_db(user = user , db = db)
    
    if(profile_img.filename != ""):
        # Create the images directory if it doesn't exist
        if not os.path.exists('images'):
            os.mkdir('images')

        # Save the uploaded image
        image_path = f"images/{profile_img.filename}"
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(profile_img.file, buffer)
    
    await email_serder.send_email(auth_schemas.EmailSchema(email = [user.email]), instance= new_user)
    
    return new_user

@auth_service.get("/auth/profile/{filename}")
async def get_profile_img(filename: str, current_user: User =  Depends(oauth2.get_current_user)):
    return FileResponse(f"images/{filename}")

@auth_service.get("/auth/get_user/{id}", response_model= auth_schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), current_user: User =  Depends(oauth2.get_current_user)):
    
    user = user_db_provider.get_user_db(id = id, db = db)
    
    return user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("auth_micro:auth_service", host=f"{settings.auth_service_host}", port=settings.auth_service_port, reload= True)
    #uvicorn.run(auth_service, host="localhost", port=8001)