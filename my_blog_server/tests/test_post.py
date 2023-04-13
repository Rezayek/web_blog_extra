import os
import sys
# Get the path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the path of the parent directory to the system path
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)
import pytest
from app.services.post_service.post_schemas import PostBase, PostResponse

def test_get_all_posts(authorized_client_post, test_post):
    res = authorized_client_post.get("/posts")
    
    def validate(post):
        return PostResponse(**post)
    
    
    post_list = list(map(validate,res.json()))
    print(post_list)
    assert len(res.json()) == len(test_post)
    assert res.status_code == 200
    assert post_list[0].owner_id== test_post[0].owner_id
       
def test_get_post(authorized_client_post, test_post):

    print(test_post)
    res = authorized_client_post.get(f"/posts/{test_post[0].owner_id}") 
    post = PostResponse(**res.json())
    
    assert post.owner.id == test_post[0].owner_id
    assert post.content == test_post[0].content
    
def test_unauthorized_user_get_all_posts(unauthorized_client_post, test_post):
    res = unauthorized_client_post.get("/posts")
    assert res.status_code == 401
    
def test_unauthorized_user_get_post(unauthorized_client_post, test_post):
    res = unauthorized_client_post.get(f"/posts/{test_post[0].owner_id}")
    assert res.status_code == 401
    
def test_get_post_not_exist(authorized_client_post, test_post):
    res = authorized_client_post.get(f"/posts/8000000")
    assert res.status_code == 404
       
@pytest.mark.parametrize("title, content, published",
    [
        
            ("post 1 ",
            "content content content ",
            True)
                
        ,
        
            ("post 2 ",
            "content content content ",
            True)
                
        ,
        
            ("post 2 ",
            "content content content ",
            True)
                
        ,
    ])      
def test_create_post(authorized_client_post, test_user, test_image, title, content, published):
    
    
    res = authorized_client_post.post("/posts/", data = {"title": title, "content": content, "tags": "", "published": published}, files = test_image)
    created_post = PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.owner_id == test_user['id']
    
def test_create_post_default_published(authorized_client_post, test_user, test_image):
    
    
    res = authorized_client_post.post(f"/posts/", data = {"title": "post", "content": "content", "tags": ""}, files = test_image)
    created_post = PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']
       
def test_unauthorized_user_create_post(unauthorized_client_post, test_post, test_image):
    res = unauthorized_client_post.post(f"/posts/", data = {"title": "title", "content": "content"}, files = test_image)
    assert res.status_code == 401
    
def test_delete_post(authorized_client_post, test_user, test_post):
    res = authorized_client_post.delete(f"/posts/{test_post[0].id}")
    assert res.status_code == 204
      
def test_unauthorized_user_delete_post(unauthorized_client_post, test_user, test_post):
    res = unauthorized_client_post.delete(f"/posts/{test_post[0].id}")
    assert res.status_code == 401
    
def test_delete_post_not_exists(authorized_client_post, test_user, test_post):
    res = authorized_client_post.delete(f"/posts/80000000")
    assert res.status_code == 404
    
def test_update_post(authorized_client_post, test_user, test_post, test_image):
    data = {
        "title": "update",
        "content": "content update",
        "id": test_post[0].id,
        "tags": "news,anime"
    }
    
    res = authorized_client_post.put(f"/posts/{test_post[0].id}", data = data, files = test_image)
    
    updated_post = PostResponse(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    
def test_unauthorized_user_update_post(unauthorized_client_post, test_user, test_post, test_image):
    res = unauthorized_client_post.put(f"/posts/{test_post[0].id}")
    assert res.status_code == 401
    
def test_update_post_not_exists(authorized_client, test_user, test_post, test_image):
    
    data = {
        "title": "update",
        "content": "content update",
        "id": 50,
        "tags": "news,anime"
    }
    res = authorized_client.put(f"/posts/700000", data = data, files = test_image)
    assert res.status_code == 404