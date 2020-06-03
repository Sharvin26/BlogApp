import datetime
from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash

class Blog(db.Document):
    title = db.StringField(required=True)
    body = db.StringField(required=True)
    tag = db.StringField(required=True)
    blog_image_url = db.URLField(required=True)
    published_at = db.DateTimeField(default=datetime.datetime.utcnow)
    added_by = db.ReferenceField('User')

class User(db.Document):
    firstname = db.StringField(required=True)
    lastname = db.StringField(required=True)
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    is_confirmed = db.BooleanField(default=False)
    joined_at = db.DateTimeField(default=datetime.datetime.utcnow)
    profile_picture = db.URLField()
    blogs = db.ListField(db.ReferenceField('Blog', reverse_delete_rule=db.PULL))

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

User.register_delete_rule(Blog, 'added_by', db.CASCADE) 