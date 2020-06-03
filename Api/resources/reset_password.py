import datetime
from flask import request, render_template
from flask_restful import Resource
from flask_jwt_extended import ( 
    create_access_token,
    decode_token
)
from repository.models import User
from services.mail import send_mail
from jwt.exceptions import (
    ExpiredSignatureError, 
    DecodeError,
    InvalidTokenError
)
from mongoengine.errors import ( 
    FieldDoesNotExist, 
    DoesNotExist
)
from utils.errors import (
    UserDoesnotExistsError,
    SchemaValidationError,
    ExpiredTokenError,
    BadTokenError,
    InternalServerError
)


CONSTANT_URL = "http://localhost:3000/"

class ForgetPassword(Resource):
    def post(self):
        try:
            url = CONSTANT_URL + "reset/"
            email = request.get_json().get('email')
            if not email:
                raise SchemaValidationError
            user = User.objects.get(email=email)
            expires = datetime.timedelta(minutes=10)
            reset_token = create_access_token(str(user.id), expires_delta=expires)
            return send_mail('[BlogApp] Reset Your Password',
                              sender='support@blog.com',
                              recipients=[user.email],
                              html_body=render_template('reset_password/forget_password.html',
                                                        url=url + reset_token))
        except DoesNotExist:
            raise UserDoesnotExistsError
        except SchemaValidationError:
            raise SchemaValidationError
        except Exception as e:
            raise InternalServerError

class ResetPassword(Resource):
    def post(self):
        try:
            body = request.get_json()
            reset_token = body.get('reset_token')
            password = body.get('password')
            if not reset_token or not password:
                raise SchemaValidationError
            user_id = decode_token(reset_token)['identity']
            user = User.objects.get(id=user_id)
            user.modify(password=password)
            user.hash_password()
            user.save()
            return send_mail('[BlogApp] Password reset successful',
                    sender='support@blog.com',
                    recipients=[user.email],
                    html_body=render_template('reset_password/reset_password_success.html'))
        except SchemaValidationError:
            raise SchemaValidationError
        except ExpiredSignatureError:
            raise ExpiredTokenError
        except (DecodeError, InvalidTokenError):
            raise BadTokenError
        except Exception as e:
            raise InternalServerError