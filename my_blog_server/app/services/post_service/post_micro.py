import os
import sys
# Get the path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the path of the parent directory to the system path
parent_dir = os.path.abspath(os.path.join(current_dir, '../../..'))
sys.path.append(parent_dir)
from typing import List, Optional
from app.services.user_auth_service import oauth2
from app.app_models.db_models import User
from app.services.post_service import post_schemas 
from app.db_holder_dic.database import get_db
from sqlalchemy.orm import Session
from fastapi import Form, UploadFile, status, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.post_service.post_db.post_db_provider import PostDbProvider
from fastapi.responses import FileResponse
from click import File
import shutil
import os
from app.config_env import settings


post_db_service = PostDbProvider()


posts_service = FastAPI()

# add CORS middleware to allow cross-origin requests
posts_service.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@posts_service.get("/posts", response_model = List[post_schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: User =  Depends(oauth2.get_current_user), limit:int = 10, skip:int = 0, search:Optional[str] = ""):
    return post_db_service.get_all_posts_db(db = db, limit= limit, skip= skip, search= search )


@posts_service.post("/posts", status_code=status.HTTP_201_CREATED, response_model=post_schemas.PostResponse)
def create_posts(
    title: str = Form(...),
    content: str = Form(...),
    post_img: UploadFile = File(None),
    tags: str = Form(None),
    db: Session = Depends(get_db), 
    current_user: User =  Depends(oauth2.get_current_user),
    timeout: int = 60
    ):
    
    post =  post_schemas.PostBase(title= title, content=content, attached_img = post_img.filename if post_img.filename else "", tags =  tags.split(",") if tags is not None else []) 
    result =  post_db_service.create_post_db(post = post, current_user= current_user, db = db )
    if post_img.filename !="":
        # Create the images directory if it doesn't exist
        if not os.path.exists('posts_images'):
            os.mkdir('posts_images')

        # Save the uploaded image
        image_path = f"posts_images/{post_img.filename}"
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(post_img.file, buffer)
        
    return result


@posts_service.get("/posts/{id}", response_model=post_schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: User =  Depends(oauth2.get_current_user)):
    return post_db_service.get_post_db(id = id, db = db)


@posts_service.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: User =  Depends(oauth2.get_current_user)):
    return post_db_service.delete_post_db(id = id, current_user= current_user, db= db)


@posts_service.put("/posts/{id}", response_model=post_schemas.PostResponse)
def update_post(
    id: int, 
    title: str = Form(...),
    content: str = Form(...),
    post_img: UploadFile = File(None),
    tags: str = Form(None),
    db: Session = Depends(get_db),
    current_user: User =  Depends(oauth2.get_current_user)
    ):
    
    post = post_schemas.PostBase(title= title, content= content, attached_img = post_img.filename, tags = tags.split(",") if tags is not None else [])
    
    result = post_db_service.update_post_db(id = id, current_user= current_user, post = post, db= db)
    
    if(post_img is not None):
        # Create the images directory if it doesn't exist
        if not os.path.exists('posts_images'):
            os.mkdir('posts_images')

        # Save the uploaded image
        image_path = f"posts_images/{post_img.filename}"
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(post_img.file, buffer)
        
    return result

@posts_service.get("/posts/images/{filename}")
async def get_profile_img(filename: str, current_user: User =  Depends(oauth2.get_current_user)):
    return FileResponse(f"posts_images/{filename}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("post_micro:posts_service", host=f"{settings.posts_service_host}", port=settings.posts_service_port, reload= True)