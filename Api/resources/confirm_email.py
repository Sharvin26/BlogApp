import datetime
import json
from flask import request, render_template, Response
from flask_restful import Resource
from flask_jwt_extended import ( 
    create_access_token, 
    decode_token
)
from mongoengine.errors import ( 
    FieldDoesNotExist, 
    DoesNotExist
)
from jwt.exceptions import ( 
    ExpiredSignatureError, 
    DecodeError, 
    InvalidTokenError
)
from services.mail import send_mail
from repository.models import User
from utils.errors import (
    SchemaValidationError,
    UserDoesnotExistsError,
    EmailAlreadyExistsError,
    BadTokenError,
    ExpiredTokenError,
    InternalServerError
)

CONSTANT_URL = "http://localhost:3000/"

class SendConfirmEmail(Resource):
    def post(self):
        try:
            url = CONSTANT_URL + "confirm_account/"
            email = request.get_json().get('email')
            if not email:
                raise SchemaValidationError
            user = User.objects.get(email=email)
            expires = datetime.timedelta(hours=12)
            confirm_token = create_access_token(str(user.id), expires_delta=expires)
            return send_mail('[ Blog ] Confirm your email',
                            sender='welcome@blog.com',
                            recipients=[user.email],
                            html_body=render_template('confirm_email/confirm_account_send.html',
                                                        url=url + confirm_token))
        except FieldDoesNotExist:
            raise SchemaValidationError
        except DoesNotExist:
            raise UserDoesnotExistsError
        except SchemaValidationError:
            raise SchemaValidationError
        except Exception as e:
            raise InternalServerError

class ConfirmEmail(Resource):
    def post(self):
        try:
            body = request.get_json()
            confirm_token = body.get('confirm_token')
            is_confirmed = body.get('is_confirmed')
            if not confirm_token or not is_confirmed:
                raise SchemaValidationError
            user_id = decode_token(confirm_token)['identity']
            user = User.objects.get(id=user_id)
            check_is_confirmed = json.loads(user.to_json()).get('is_confirmed')
            if check_is_confirmed:
                raise EmailAlreadyExistsError
            user.modify(is_confirmed=is_confirmed)
            user.save()
            return send_mail('[Blog] Account validated successful',
                                sender='welcome@blog.com',
                                recipients=[user.email],
                                html_body=render_template('confirm_email/confirm.html'))
        except SchemaValidationError:
            raise SchemaValidationError
        except EmailAlreadyExistsError:
            raise EmailAlreadyExistsError
        except ExpiredSignatureError:
            raise ExpiredTokenError
        except (DecodeError, InvalidTokenError):
            raise BadTokenError
        except Exception as e:
            raise InternalServerError