from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError,Length , Email, EqualTo, Optional
from app.models import User
from flask_wtf.file import FileField, FileAllowed


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")
    

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")


    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError(
                "this username is taken, please use a different username")
        
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError(
                "this email is taken, please use a different email")

class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    profile_picture = FileField("Update Picture", validators=[FileAllowed(["jpg", "png"])])
    profilebio = StringField("Profile Bio", validators=[Length(min=0, max=140)])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user is not None:
                raise ValidationError(
                    "this username is taken, please use a different username")
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user is not None:
                raise ValidationError(
                    "this email is taken, please use a different email")
            
class PostForm(FlaskForm):
    title = StringField("Title", validators=[Optional()])
    content = StringField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")
