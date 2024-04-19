from app import app, BlogBite
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, UpdateAccountForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
# from werkzeug.urls import url_parse
from urllib.parse import urlparse as url_parse
from app.helper import save_picture
from datetime import datetime


@app.route("/")
@app.route("/index", methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    # posts = Post.query.all()
    posts = Post.query.order_by(Post.datepost.desc()).all()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data, author = current_user)
        BlogBite.session.add(post)
        BlogBite.session.commit()
        flash("Post added!")
        return redirect(url_for("index"))
    return render_template("index.html", title = "Home", form = form, posts = posts)

@app.route("/register", methods = ["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit(): # if the form is submitted
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        BlogBite.session.add(user)
        BlogBite.session.commit()
        flash("you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title = "Register", form = form)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        BlogBite.session.commit()

@app.route("/login", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit(): # if the form is submitted
        user = User.query.filter_by(username = form.username.data).first()
        # if the user is not found or the password is incorrect
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember = form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")        
        return redirect(url_for("index"))
    return render_template("login.html", title = "Sign In", form =  form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/profile/<username>", methods = ["GET", "POST"])
@login_required
def profile(username):
    user = User.query.filter_by(username = username).first_or_404()
    profile_picture = url_for("static", filename = "images/profile_pics/" + user.profile_picture)

    
    user = User.query.filter_by(username = username).first_or_404()
    posts = Post.query.order_by(Post.datepost.desc()).all()
    update_form = UpdateAccountForm()
    if update_form.validate_on_submit():
        if update_form.profile_picture.data:
            picture_file = save_picture(update_form.profile_picture.data)
            print(picture_file)
            current_user.profile_picture = picture_file
        current_user.username = update_form.username.data
        current_user.email = update_form.email.data
        current_user.profilebio = update_form.profilebio.data
        BlogBite.session.commit()
        flash("Your account is updated!")
        return redirect(url_for("profile", username = current_user.username))
    
    elif request.method == "GET":
        update_form.username.data = current_user.username
        update_form.email.data = current_user.email
        update_form.profilebio.data = current_user.profilebio
    return render_template("profile.html", user = user, posts = posts, update_form = update_form, profile_picture = profile_picture, title = username)
