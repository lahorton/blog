from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

def connect_to_db(app, database='postgresql:///blog'):
    """Connect database to Flask app."""

    #Configure to use the PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = database
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

app = Flask(__name__)

if __name__ == "__main__":
    """If run interactively will allow you to work with db directly"""

    # from server import app
    connect_to_db(app)
    print("Connected to DB.")


class User(db.Model):
    """user information"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(25), nullable=False)

    posts = db.relationship("Post")

    def __repr__(self):
        """show info about the user"""

        return """<user_id = {}, user_name = {}""".format(self.user_id, self.user_name)


class Post(db.Model):
    """holds blog posts"""

    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100), nullable=True)
    text = db.Column(db.String(5000), nullable=True)
    photo = db.Column(db.String(600), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    user = db.relationship("User")

    def __repr__(self):
        """show info about the post"""

        return """<post_id = {}, date = {}, location = {}>""".format(self.post_id, self.date, self.location)

