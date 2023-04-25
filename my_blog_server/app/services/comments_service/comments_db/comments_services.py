from app.services.comments_service.comments_db.comments_db import CommentsDb
from google.cloud.firestore_v1.client import Client
from app.services.comments_service import comments_schemas
from typing import Type
from app.app_models.db_models import User
import datetime
from app.firebase_cloud_store.firebase_connector import firebase_db
from google.cloud.firestore import CollectionReference, Query
from typing import List
from fastapi import status, HTTPException
from app.config_env import settings
from app.debugger_file import set_up_logger



class CommentsDbServices(CommentsDb):
    
    firebase_connector: Type[Client] = firebase_db
    logger = set_up_logger(file_name= settings.log_microservice)
    def __init__(self):
        self.posts_collection = self.firebase_connector.collection(u'posts')
        pass
    
    def get_all_comments_db(self, id: int, reply_to:int, limit: int, skip: int) -> List[comments_schemas.Comment]:
        try:
            comments_ref: CollectionReference = self.posts_collection.document(str(id)).collection(u'comments')
            query: Query = comments_ref.where(field_path='replie_to_id', op_string='==', value=reply_to).limit(limit).offset(skip)
            
            if not query:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Comment for the provided id")
            
            comments_list: List[comments_schemas.Comment] = []
            for doc in query.stream():
                data: dict = doc.to_dict()
                data['comment_id'] = doc.id
                comment: comments_schemas.Comment = comments_schemas.Comment.parse_obj(data)
                comments_list.append(comment)

            return comments_list
        except Exception as e:
            self.logger.debug(f"Failled to get comment to comments collection in firebase for post {id} error : {e}")
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Service is down for now please wait")
               

    def create_comments_db(self, id:int, comment_create : comments_schemas.CommentCreate, current_user: User):
        try:
            post_doc = self.posts_collection.document(f'{id}')
            comments_total = post_doc.get().get('comments_total') + 1
            commment_doc = post_doc.collection('comments').document(f'{comments_total}')
            comment_dict = {
                'replie_to_id': comment_create.replie_to_id,
                'user_id': current_user.id,
                'post_id': id,
                'user_name': current_user.user_name,
                'user_profile_img': current_user.profile_img,
                'content': comment_create.content ,
                'created_at': datetime.datetime.now(),
                'is_published': True,
                'replies':0,
                'likes': 0,
                'dislikes': 0,               
            }
            commment_doc.set(comment_dict) 
            commment_doc.collection("reacts").document('0').set({"empty_reaction": "none"})
            post_doc.update({'comments_total': comments_total })
            if(comment_create.replie_to_id != -1):
                reply_to_comment = post_doc.collection('comments').document(f'{comment_create.replie_to_id}')
                reply_to_comment_total = reply_to_comment.get().get('replies') + 1
                reply_to_comment.update({'replies': reply_to_comment_total})
                
            comment_dict_with_id = {**comment_dict, **{'comment_id': comments_total}}
            return comments_schemas.Comment(**comment_dict_with_id)
        
        except Exception as e:
            self.logger.debug(f"Failled to add comment to comments collection in firebase for post {id} error : {e}")
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Service is down for now please wait")
        

    def add_react_db(self, react_create: comments_schemas.ReactCreate, current_user: User ):
        comments_doc = self.posts_collection.document(f'{react_create.post_id}').collection(u'comments').document(f'{react_create.comment_id}')
        react_dict = {"likes": -1, "dislikes": -1}
        current_react = comments_doc.collection("reacts").document(f"{current_user.id}").get().get("react")
        def remove_like():
            
            total_likes =  comments_doc.get().get('likes') - 1
            comments_doc.update({'likes': total_likes})
            react_dict["likes"] = total_likes
        
        def remove_dislike():
            
            total_dislikes =  comments_doc.get().get('dislikes') - 1
            comments_doc.update({'dislikes': total_dislikes})
            react_dict["dislikes"] = total_dislikes
            
        def add_like():
            
            total_likes =  comments_doc.get().get('likes') + 1
            comments_doc.update({'likes': total_likes})
            react_dict["likes"] = total_likes
            
            
        def add_dislike():
            
            total_dislikes =  comments_doc.get().get('dislikes') + 1
            comments_doc.update({'dislikes': total_dislikes})
            react_dict["dislikes"] = total_dislikes
        
        if react_create.pre_react == 1 and react_create.react == -1:  
            if not current_react: 
                raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"way of React is wrong")
            
            if current_react ==  react_create.react:
                raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"way of React is wrong")
            
            add_dislike()
            remove_like()
            
            
        elif react_create.pre_react == -1 and react_create.react == 1: 
            if not current_react: 
                raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"way of React is wrong")
            
            if current_react ==  react_create.react:
                raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"way of React is wrong")
            
            add_like()
            remove_dislike()
        
        
        elif react_create.pre_react == 0 and (react_create.react == 1 or react_create.react == -1) :
            
            
            if current_react == 1 or current_react == -1 :
                raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"way of React is wrong")
            
            elif react_create.react == 1:
                add_like()
                
            elif react_create.react == -1:    
                add_dislike()
            
            
        elif react_create.react == 0:
            if current_react != 0:
                comments_doc.collection("reacts").document(f"{current_user.id}").update({"react": 0})
                if react_create.pre_react == 1 :   
                    remove_like()
                    
                elif react_create.pre_react == -1:    
                    remove_dislike()
                    
            else :
                raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"way of React is wrong")
        else : 
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"way of React is wrong")
        data = {"user_id": current_user.id, "react": react_create.react, "comment_id": react_create.comment_id} 
        comments_doc.collection("reacts").document(f"{current_user.id}").set(data)
        react_out = {**data, **react_dict}
        return comments_schemas.ReactOut(**react_out)
    
    def delete_comments_db(self):
        pass
    

    def update_comments_db(self, id:int, comment_update : comments_schemas.CommentUpdate, current_user: User):
        try:
            commment_doc = self.posts_collection.document(f'{id}').collection('comments').document(f'{comment_update.comment_id}')
            user_id = commment_doc.get().get('user_id')
            if(user_id is not current_user.id):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not allowed to modifier other users comments ")
            
            commment_doc.update({'content': comment_update.content})
            updated_data: dict = commment_doc.get().to_dict()
            updated_data['comment_id'] = commment_doc.id
            return comments_schemas.Comment(**updated_data)
        
        except Exception as e:
            self.logger.debug(f"Failled to update comment to comments collection in firebase for post {id} error : {e}")
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Service is down for now please wait")