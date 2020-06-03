from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from repository.db import initialize_db
from utils.errors import errors

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "odKKwdIIY7odzesfVImtTj"

# app.config['MAIL_SERVER'] = 'localhost'
# app.config['MAIL_PORT'] = '1025'
# app.config['MAIL_USERNAME'] = 'welcome@blog.com'
# app.config['MAIL_PASSWORD'] = ''

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = '465'
app.config['MAIL_USERNAME'] = '<Add-your-gmail-email-here>'
app.config['MAIL_PASSWORD'] = '<Add-your-password-here>'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

from resources.urls import initialize_urls

class Api(Api):
    def error_router(self, original_handler, e):
        error_type = type(e).__name__.split(".")[-1] 
        if self._has_fr_route() and error_type in list(errors) + ['UnprocessableEntity']:
            try:
                return self.handle_error(e)
            except Exception:
                pass
        return original_handler(e)

api = Api(app, errors=errors)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/BlogApp'
}

initialize_db(app)

initialize_urls(api)