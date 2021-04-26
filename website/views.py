from flask import Blueprint, render_template
from flask import url_for
from flask_login import login_required, current_user
from .models import Post
views = Blueprint('views', __name__)

@views.route('/')
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)
