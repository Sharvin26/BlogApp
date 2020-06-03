import re
import datetime
import json
from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import ( 
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    jwt_optional
)
from threading import Thread
from repository.models import User, Blog
from utils.helper import get_blogs, confirm_account
from utils.token_manager import generate_tokens, refresh_a_token
from mongoengine.errors import ( 
    ValidationError,
    FieldDoesNotExist,
    DoesNotExist,
    NotUniqueError
)
from utils.errors import (
    SchemaValidationError,
    FieldAlreadyExistsError,
    PasswordValidationFailed,
    UnauthorizedError,
    UserDoesnotExistsError,
    NotAllowed,
    InternalServerError
)

class SignUpApi(Resource):
    def post(self):
        try:
            user_data = request.get_json()
            user = User(**user_data)
            password_regex = r'^.*(?=.{8,10})(?=.*[a-zA-Z])(?=.*?[A-Z])(?=.*\d)[a-zA-Z0-9!@£$%^&*()_+={}?:~\[\]]+$'
            if not re.match(password_regex, user.password):
                raise PasswordValidationFailed
            user.hash_password()
            user.save()
            Thread(target=confirm_account, 
                            args=(user_data.get('email'),)).start()
            return generate_tokens(user), 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise FieldAlreadyExistsError
        except PasswordValidationFailed:
            raise PasswordValidationFailed
        except Exception as e:
            raise InternalServerError


class RefreshAccessTokenApi(Resource):
    @jwt_refresh_token_required
    def post(self):
        try:
            current_user = get_jwt_identity()
            return refresh_a_token(current_user), 200
        except Exception as e:
            raise InternalServerError


class LoginApi(Resource):
    def post(self):
        try:
            user_data = request.get_json()
            user = User.objects.get(email=user_data.get('email'))
            authorized = user.check_password(user_data.get('password'))
            if not authorized:
                raise UnauthorizedError
            return generate_tokens(user), 200
        except ( UnauthorizedError, DoesNotExist):
            raise UnauthorizedError
        except Exception as e:
            raise InternalServerError


class GetUserDetailsApi(Resource):
    @jwt_optional
    def get(self, username=None):
        try:
            if username:
                user = User.objects.get(username=username)
                user_details = json.loads(user.to_json())
                del user_details['email']
                del user_details['is_confirmed']
            else:
                user_id = get_jwt_identity()
                user = User.objects.get(id=user_id)
                user_details = json.loads(user.to_json())
            del user_details['password']
            blogs = get_blogs(user_details, Blog)
            user_details['blogs'] = blogs
            return user_details
        except DoesNotExist:
            raise UserDoesnotExistsError
        except Exception as e:
            raise InternalServerError

    @jwt_required
    def put(self):
        try:
            request_data = request.get_json()
            if request_data.get("username") or request_data.get("email") :
                raise NotAllowed
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            user.update(**request_data)
            user = User.objects.get(id=user_id)
            user_details = json.loads(user.to_json())
            del user_details['password']
            blogs = get_blogs(user_details, Blog)
            user_details['blogs'] = blogs
            return user_details
        except NotAllowed:
            raise NotAllowed
        except DoesNotExist:
            raise UserDoesnotExistsError
        except Exception as e:
            raise InternalServerError