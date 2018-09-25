from flask import (Flask, render_template, redirect, request, flash, session)
from datetime import datetime
from model import User, Post, app
import random
from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db
import os
import json
from sqlalchemy import update
import doctest

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ["SERVER_APP_SECRET_KEY"]

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage"""

    if 'user_id' in session:
        user = User.query.get(session["user_id"])
        return render_template("homepage.html", user=user)
    else:
        return render_template("homepage.html")

    return render_template("homepage.html")


@app.route('/login', methods=['POST'])
def check_login():
    """login existing users"""

    user_name = request.form.get("name")
    password = request.form.get("password")

    user = User.query.filter(User.user_name == user_name).first()

    if user:
        password_match = db.session.query(User.password).filter(User.user_name == user_name).first()

        password_match = password_match[0]
        if password == password_match:
            session["user_id"] = user.user_id
            flash(f"Welcome, {user.user_name.title() }!", category='info')
            return redirect(f"/")
        else:
            flash("Login failed. Please double-check your password.", category='warning')
            return redirect("/")
    else:
        flash("Looks like you're not registered.  Please register.", category='warning')
        return redirect("/")


@app.route('/logout')
def logout():
    """Clears user_id from session"""
    if 'user_id' in session:
        del session['user_id']
        flash("Logged out.", category='info')
        return redirect("/")
    else:
        flash("Please login.", category='info')
        return redirect("/")


@app.route('/about')
def tells_about():
    """about me."""

    return render_template("about.html")


@app.route('/register', methods=["POST"])
def register_user():
    """adds user to db"""

    user_name = request.form.get("name").strip().title()
    password = request.form.get("password")

    if user:
        flash("That user_name is already registered.  Please choose another name.", category='warning')
        return redirect('/')
    else:
        user_name = User(user_name=user_name, password=password)
        db.session.add(user_name)
        db.session.commit()
        flash("Thank you for registering.  Please login to get started!", category='success')
        return redirect("/")


@app.route('/display_posts')
def display_posts():
    """displays posts within the selected time-range"""

    # user = User.query.get(session["user_id"])

    #do a db query based on get request to display the specified posts (currently = all).
    posts = db.session.query(Post).order_by(Post.date.desc()).all()

    #user=user
    print(posts)
    return render_template("display_posts.html", posts=posts)


@app.route("/display_posts/<post_id>")
def display_full_post(post_id):
    """displays full post"""

    #get full post object
    post = Post.query.get(post_id)

    return render_template("single_post.html", post=post)


@app.route('/add_post', methods=["POST"])
def add_post():
    """allows user to add a post"""

    date = datetime.now()
    location = request.form.get("location").strip().title()
    title= request.form.get("title")

    if 'user_id' in session:
        user_id = session['user_id']
    else:
        flash("Only the administrator can add posts.")
        return redirect('/display_posts')
    text = request.form.get("text")
    photo = request.form.get("photo")

    post = Post(date=date, location=location, user_id=user_id, title=title, text=text, photo=photo)
    db.session.add(post)
    db.session.commit()
    return redirect('/display_posts')


@app.route('/edit_post', methods=["POST"])
def edit_post():
    """allows user to edit a post"""

    post_id = request.form.get("post_id")

    post = Post.query.get(post_id)

    location = request.form.get("location").title()
    title = request.form.get("title")
    text = request.form.get("text")
    photo = request.form.get("photo")

    if location:
        post.location = location
    else:
        post.location = post.location

    if title:
        post.title = title
    else:
        post.title = post.title

    if text:
        post.text = text
    else:
        post.text = post.text

    if photo:
        post.photo = photo
    else:
        post.photo = post.photo

    db.session.commit()
    return redirect('/display_posts')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug


    # connect_to_db(app)
    connect_to_db(app)


    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
