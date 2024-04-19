import os
from mysql_connect import mysql_connect
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "who_im_i?"
    
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        mysql_connect # mysql://<username>:<password>@<host>/<dbname>
    SQLALCHEMY_TRACK_MODIFICATIONS = False
#from app import BlogBite