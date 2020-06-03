from flask import Response, request
from flask_restful import Resource

from repository.models import Blog

from mongoengine.errors import (
    FieldDoesNotExist,
    ValidationError,
    DoesNotExist,
    InvalidQueryError
)

from utils.errors import ( 
    InternalServerError,
    SchemaValidationError,
    BlogDoesNotExist
)

class BlogsApi(Resource):
    def get(self):
        try:
            blogs = Blog.objects().to_json()
            return Response(blogs, mimetype="application/json", status=200)
        except Exception as e:
            raise InternalServerError

    def post(self):
        try:
            blog_data = request.get_json()
            blog = Blog(**blog_data)
            blog.save()
            return Response(blog.to_json(), mimetype="application/json", status=200)
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

    def put(self, id):
        try:
            blog_data = request.get_json()
            Blog.objects.get(id=id).update(**blog_data)
            return Response(status=200)
        except DoesNotExist:
            raise BlogDoesNotExist
        except InvalidQueryError:
            raise SchemaValidationError
        except Exception as e:
            raise InternalServerError
    
    def delete(self, id):
        try:
            Blog.objects.get(id=id).delete()
            return Response(status=204)
        except DoesNotExist:
            raise BlogDoesNotExist
        except Exception as e:
            raise InternalServerError