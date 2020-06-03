import json
import requests

CONST_CONFIRM_ACCOUNT_URL = "http://127.0.0.1:5000/api/user/send/confirm"

def get_blogs(user_details, Blog):
    blogs = []
    if user_details['blogs']:
        for blog in user_details['blogs']:
            blog = Blog.objects.get(id=blog["$oid"]).to_json()
            blog = json.loads(blog)
            blogs.append(blog)
    return blogs

def confirm_account(email):
    url = CONST_CONFIRM_ACCOUNT_URL
    body = {
        "email": email
    }
    requests.post(url, json=body)