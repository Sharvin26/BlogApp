from flask import Flask
from flask_restful import Api
from repository.db import initialize_db
from utils.errors import errors

app = Flask(__name__)

from resources.urls import initialize_urls

api = Api(app, errors=errors)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/BlogApp'
}

initialize_db(app)

initialize_urls(api)