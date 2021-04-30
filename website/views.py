from flask import Blueprint, render_template
from flask import url_for
from flask_login import login_required, current_user
from .models import Post, User
views = Blueprint('views', __name__)


@views.route('/')
def home():
    posts = Post.query.all()
    userID_username_dict = dict()
    for post in posts:
        userID_username_dict.update({post.user_id: User.query.get(post.user_id).username})
    return render_template("home.html", user=current_user, posts=posts, usernames=userID_username_dict)
