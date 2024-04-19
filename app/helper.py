from flask_wtf.file import FileField, FileAllowed
from werkzeug.utils import secure_filename
from flask_login import current_user
from app import app, BlogBite
import os
import secrets

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    final_pic = random_hex + f_ext
    picture_path = os.path.join(
            app.root_path, 'static/images/profile_pics', final_pic)
    print(picture_path)
    form_picture.save(picture_path)
    return final_pic
