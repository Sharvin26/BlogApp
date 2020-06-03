import json

def get_blogs(user_details, Blog):
    blogs = []
    if user_details['blogs']:
        for blog in user_details['blogs']:
            blog = Blog.objects.get(id=blog["$oid"]).to_json()
            blog = json.loads(blog)
            blogs.append(blog)
    return blogs