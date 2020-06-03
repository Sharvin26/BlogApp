import json
from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from repository.models import Blog, User
from mongoengine.errors import (
    FieldDoesNotExist,
    ValidationError,
    DoesNotExist,
    InvalidQueryError
)
from utils.errors import ( 
    InternalServerError,
    SchemaValidationError,
    BlogDoesNotExist,
    UserDoesnotExistsError
)

class BlogsApi(Resource):
    def get(self):
        try:
            blogs = Blog.objects().to_json()
            return Response(blogs, mimetype="application/json", status=200)
        except Exception as e:
            raise InternalServerError

    @jwt_required
    def post(self):
        try:
            user_id = get_jwt_identity()
            blog_data = request.get_json()
            user = User.objects.get(id=user_id)
            user_details = json.loads(user.to_json())
            username = user_details.get('username')
            blog = Blog(**blog_data, added_by=user_id, username=username)
            blog.save()
            user.update(push__blogs=blog)
            user.save()
            return Response(blog.to_json(), mimetype="application/json", status=200)
        except DoesNotExist:
            raise UserDoesnotExistsError
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except Exception as e:
            raise InternalServerError

class BlogApi(Resource):
    def get(self, id):
        try:
            blog = Blog.objects.get(id=id)
            return Response(blog.to_json(), mimetype="application/json", status=200)
        except DoesNotExist:
            raise BlogDoesNotExist
        except Exception as e:
            raise InternalServerError

    @jwt_required
    def put(self, id):
        try:
            user_id = get_jwt_identity()
            blog = Blog.objects.get(id=id, added_by=user_id)
            request_data = request.get_json()
            blog.update(**request_data)
            blog = Blog.objects.get(id=id, added_by=user_id)
            return Response(blog.to_json(), mimetype="application/json", status=200)
        except DoesNotExist:
            raise BlogDoesNotExist
        except InvalidQueryError:
            raise SchemaValidationError
        except Exception as e:
            raise InternalServerError
    
    @jwt_required
    def delete(self, id):
        try:
            user_id = get_jwt_identity()
            Blog.objects.get(id=id, added_by=user_id).delete()
            return Response(status=204)
        except DoesNotExist:
            raise BlogDoesNotExist
        except Exception as e:
            raise InternalServerError