import datetime
from .db import db

class Blog(db.Document):
    title = db.StringField(required=True)
    body = db.StringField(required=True)
    tag = db.StringField(required=True)
    blog_image_url = db.URLField(required=True)
    published_at = db.DateTimeField(default=datetime.datetime.utcnow)