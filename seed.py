from sqlalchemy import func
from model import User, Post, app
import random
from datetime import datetime
from model import connect_to_db, db
import json


def load_users():
    """loads a test user into the db"""

    user_name = "joe_shmoe"
    password = "jose_schmose"
    user = User(user_name=user_name, password=password)
    db.session.add(user)
    db.session.commit()


def load_posts():
    """load a test post to the db"""

    date = datetime.now()
    location = "Oakland, CA"

    #consider loading text in as a json file that you're parsing in server.py
    text = "test post only"
    photo = "/static/images/cage.jpg"
    user_id = 1

    post=Post(date=date, location=location, text=text, photo=photo, user_id=user_id)
    db.session.add(post)
    db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    load_users()
    load_posts()
