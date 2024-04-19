from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
# from werkzeug.utils import secure_filename
# import os


app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object(Config)

UPLOAD_FOLDER = "static/images/profile_pics"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"jpg", "png", "jpeg"}
# app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS

BlogBite = SQLAlchemy(app)
Migrate = Migrate(app, BlogBite)
login = LoginManager(app)
# redirect to login page if user is not logged in
login.login_view = "login"

from app import routes, models

__all__ = ['app', 'BlogBite'] # export app and db to other modules
