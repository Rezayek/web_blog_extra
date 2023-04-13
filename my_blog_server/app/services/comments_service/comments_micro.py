import os
import sys
# Get the path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the path of the parent directory to the system path
parent_dir = os.path.abspath(os.path.join(current_dir, '../../..'))
sys.path.append(parent_dir)


from typing import List
from app.services.user_auth_service.oauth2 import get_current_user
from app.app_models.db_models import User
from app.services.comments_service.comments_schemas import Comment, CommentCreate, ReactCreate, ReactOut, CommentUpdate
from fastapi import status, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .comments_db.comments_provider import CommentsDbProvider
from app.config_env import settings
comments_db_provider = CommentsDbProvider()



comments_service = FastAPI()

# add CORS middleware to allow cross-origin requests
comments_service.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@comments_service.post("/comments/react", status_code=status.HTTP_201_CREATED, response_model=ReactOut)
def create_comment(react_create : ReactCreate, current_user: User =  Depends(get_current_user), timeout: int = 60):
    return comments_db_provider.add_react_db(react_create = react_create, current_user = current_user)

@comments_service.get("/comments/", response_model = List[Comment])
def get_comments(id: int, reply_to:int = -1, current_user: User =  Depends(get_current_user), limit:int = 10, skip:int = 0):
    return comments_db_provider.get_all_comments_db(id = id, reply_to=reply_to, limit = limit, skip = skip)


@comments_service.post("/comments/{id}", status_code=status.HTTP_201_CREATED, response_model=Comment)
def create_comment(id: int, comment_create : CommentCreate, current_user: User =  Depends(get_current_user), timeout: int = 60):
    return comments_db_provider.create_comments_db(id = id, comment_create = comment_create, current_user = current_user)

@comments_service.put("/comments/{id}", response_model=Comment)
def update_comment(id: int, comment_update: CommentUpdate, current_user: User =  Depends(get_current_user), timeout: int = 60):
    return comments_db_provider.update_comments_db(id = id, comment_update= comment_update, current_user= current_user )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("comments_micro:comments_service", host=f"{settings.comments_service_host}", port=settings.comments_service_port, reload= True)
    #uvicorn.run(auth_service, host="localhost", port=8001)