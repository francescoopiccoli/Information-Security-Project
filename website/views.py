from flask import Blueprint, render_template
from flask import url_for
from flask import request
from flask_login import login_required, current_user
from .models import Post, User
views = Blueprint('views', __name__)


@views.route('/')
def home():

    #if request.method == 'GET':
    q = request.args.get('q')

    if q:
        posts = Post.query.filter(Post.post_title.contains(q) | Post.post_text.contains(q)).all()
        #in case no resuslts are found, the list of all the posts is shown
        if len(posts) == 0:
            posts = Post.query.all()

    else:
        posts = Post.query.all()
        print(posts)

    userID_username_dict = dict()
    for post in posts:
        userID_username_dict.update({post.user_id: User.query.get(post.user_id).username})
    return render_template("home.html", user=current_user, posts=posts, usernames=userID_username_dict, search_content=q)