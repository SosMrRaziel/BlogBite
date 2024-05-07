from app import BlogBite, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, BlogBite.Model):
    userID = BlogBite.Column(BlogBite.Integer, primary_key = True)
    username = BlogBite.Column(BlogBite.String(24), index = True, unique = True)
    email = BlogBite.Column(BlogBite.String(120), index = True, unique = True)
    password_hash = BlogBite.Column(BlogBite.String(512))
    date_joined = BlogBite.Column(
        BlogBite.DateTime, index = True, default = datetime.utcnow)
    profilebio = BlogBite.Column(BlogBite.String(140))
    profile_picture = BlogBite.Column(
        BlogBite.String(20), nullable = False, default = "default.png")
    last_seen = BlogBite.Column(BlogBite.DateTime, default = datetime.utcnow)
    posts = BlogBite.relationship("Post", backref = "author", lazy = "dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return str(self.userID) # Return userID as string
    

    def __repr__(self):
        return "<User {}>".format(self.username)
    
@login.user_loader
def load_user(id): 
    return User.query.get(int(id))

class Post(BlogBite.Model):
    postID = BlogBite.Column(BlogBite.Integer, primary_key = True)
    title = BlogBite.Column(BlogBite.String(24), nullable = False )
    content = BlogBite.Column(BlogBite.String())
    datepost = BlogBite.Column(
        BlogBite.DateTime, index = True, default = datetime.utcnow)
    # posts_picture = BlogBite.Column(
    #     BlogBite.String(20), nulable = True)    
    user_id = BlogBite.Column(
        BlogBite.Integer, BlogBite.ForeignKey("user.userID"))
    
    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author


    def __repr__(self):
        return "<Post {}>".format(self.content)
