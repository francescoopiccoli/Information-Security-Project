#database stuff
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    posts = db.relationship('Post') # every time we create a post, add to a list the post_id and the associated user
    comments = db.relationship('Comment') # every time we create a post, add to a list the post_id and the associated user


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_date = db.Column(db.DateTime(timezone=True), default=func.now())
    post_title = db.Column(db.String(200))
    post_text = db.Column(db.String(20000))
    post_image = db.Column(db.String(500)) #url
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment') # every time we create a post, add to a list the post_id and the associated post (?)


class Comment(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    comment_text = db.Column(db.String(10000))
    comment_time = db.Column(db.DateTime(timezone=True), default=func.now()) 
