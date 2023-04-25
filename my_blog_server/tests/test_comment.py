import json

def test_get_post_comments(authorized_client_comment):
    res =  authorized_client_comment.get(f"/comments?id={57}")
    assert res.status_code == 200
    
    res_json = res.json()
    assert res_json[0]["post_id"] == 57

def test_unauthorized_get_post_comments(unauthorized_client_comment):
    res =  unauthorized_client_comment.get(f"/comments?id={57}")
    assert res.status_code == 401
    

def test_get_comment_replies(authorized_client_comment):
    res = authorized_client_comment.get(f"/comments?id={57}&reply_to={1}")
    assert res.status_code == 200
    res_json = res.json()
    assert res_json[0]["post_id"] == 57
    assert res_json[1]["replie_to_id"] == 1

def test_unauthorized_get_comment_replies(unauthorized_client_comment):
    res = unauthorized_client_comment.get(f"/comments?id={57}&reply_to={1}")
    assert res.status_code == 401


def test_add_react_comment(authorized_client_comment):
    sended_data = {
        "post_id":57,
        "comment_id":1,
        "react":1,
        "pre_react":0
    }
    
    res = authorized_client_comment.post("/comments/react", json=sended_data)
    assert res.status_code == 201
    res_json = res.json()
    assert res_json["comment_id"] == 1
    

def test_change_react_comment(authorized_client_comment):
    sended_data = {
        "post_id":57,
        "comment_id":1,
        "react":-1,
        "pre_react":1
    }
    
    res = authorized_client_comment.post("/comments/react", json=sended_data)
    assert res.status_code == 201
    res_json = res.json()
    assert res_json["comment_id"] == 1  


def test_remove_react_comment(authorized_client_comment):
    sended_data = {
        "post_id":57,
        "comment_id":1,
        "react":0,
        "pre_react":-1
    }
    
    res = authorized_client_comment.post("/comments/react", json=sended_data)
    assert res.status_code == 201
    res_json = res.json()
    assert res_json["comment_id"] == 1   
    
    
def test_unauthorized_add_react_comment(unauthorized_client_comment):
    sended_data = {
        "post_id":57,
        "comment_id":1,
        "react":1,
        "pre_react":0
    }
    
    res = unauthorized_client_comment.post("/comments/react",  json=sended_data)
    assert res.status_code == 401

def test_update_comment(authorized_client_comment):
    data = {
        "comment_id":2,
        "content": "updated version forthis comment"
    }
    res = authorized_client_comment.put(f"/comments/{57}", json = data)
    assert res.status_code == 200
    res_json = res.json()
    assert res_json["content"] == "updated version forthis comment"

def test_unauthorized_update_comment(unauthorized_client_comment):
    data = {
        "comment_id":2,
        "content": "updated version forthis comment"
    }
    res = unauthorized_client_comment.put(f"/comments/{57}", json = data)
    
    assert res.status_code == 401