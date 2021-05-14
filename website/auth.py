from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Post, Comment
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
import random
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True) #remember that the user is logged in, stored in the flask session data, unless webserver restarts or user clears its browser history, he is remembered
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)


@auth.route("/sign-up", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        fullname = request.form.get('fullname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category="error")
        elif len(email)< 4:
            flash('Email must be greater than 4 characters', category="error")
        elif len(fullname) < 2:
            flash('Fullname must be greater than 2 characters', category="error")
        elif password1 != password2:
            flash('Passwords don\'t match', category="error")
        elif len(password1) < 5:
            flash('Passwords must be at least 5 characters', category="error")
        else:
            u = User(email=email, username=fullname, password=generate_password_hash(password1, 'sha256')) #in the secure application we should hash the password with the werkzeug package
            db.session.add(u)
            db.session.commit()
            login_user(u, remember=True) #remember that the user is logged in, stored in the flask session data, unless webserver restarts or user clears its browser history, he is remembered
            flash('Account created!', category="success")
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)

@auth.route("/logout")
@login_required #using this decorator, we cannot access this page unless the user is logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    images = ['https://images.prismic.io/www-static/499858ce-04e8-4c5b-9329-a735976b3cf5_App-Platform-bg.png?auto=compress,format', 'https://cdn.dribbble.com/users/464226/screenshots/15086644/media/ead429c865cbd3576e81e1e8c6e132cd.png?compress=1&resize=800x600', 'https://assets.digitalocean.com/labs/images/community_bg.png', 'https://cdn.dribbble.com/users/464226/screenshots/15101536/media/52b328437eb2849bf7dbc2da0da11d6f.png?compress=1&resize=800x600', 'https://cdn.dribbble.com/users/464226/screenshots/14507703/media/ec1b31df01640a6bacfc1ef6e4d637b0.png?compress=1&resize=800x600', 'https://cdn.dribbble.com/users/464226/screenshots/14490629/media/591178cb7994be86d4812b3dbc884efd.png?compress=1&resize=800x600', 'https://cdn.dribbble.com/users/464226/screenshots/9362946/media/f6fdc2aa6f57eb25efed72dc3f9a1ccd.png?compress=1&resize=800x600', 'https://cdn.dribbble.com/users/741168/screenshots/5380170/connected_city_-_part_3_digitalocean_4x.png?compress=1&resize=1600x1200']
    post_image = images[random.randint(0,len(images)-1)]
    if request.method == 'POST':
        post_title = request.form.get('title')
        post_text = request.form.get('post')

        if len(post_text) < 1:
            flash('post content is too short', category='error')
        elif len(post_title) < 1:
            flash('title is too short', category='error')
        else:
            new_post = Post(post_date=datetime.now(), post_title=post_title, post_text=post_text, post_image=post_image, user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('Post added', category='success')
            return redirect(url_for('views.home'))

        
    return render_template("create.html", user=current_user)


@auth.route("/profile")
@login_required
def profile():
    #to show the total number of comments, create a dictionary which is [postId : totalCOmments]
    postID_totalComments_dict = dict()
    postID_LastComment_dict = dict()
    for post in current_user.posts:
        totalComments = 0
        for comment in post.comments:
            totalComments += 1
        if len(post.comments) > 0:
            lastComment = post.comments[-1]
        #to show the last activity, create a dictionary which is {postid: [lastCmmentText, lastCommentTime, lastCommnetUSername]}
            postID_LastComment_dict.update({post.id : [lastComment.comment_text, lastComment.comment_time, User.query.get(lastComment.user_id).username]})
        postID_totalComments_dict.update({post.id: totalComments}) 
    print(postID_LastComment_dict)



    return render_template("profile.html", user=current_user, totalCommentXPost=postID_totalComments_dict, lastActivityInfo=postID_LastComment_dict)

@auth.route("/post")
@auth.route('/post/<int:postid>', methods=['GET', 'POST'])
def post(postid=None):

    post_id = request.args.get('post', postid)
    post=Post.query.get(post_id)
    totalComments = 0
    userID_username_dict = dict()

    if(post):
        for comment in post.comments:
            totalComments += 1
            userID_username_dict.update({comment.user_id: User.query.get(comment.user_id).username}) 

        if request.method == 'POST':
            comment_text = request.form.get('post')

            if len(comment_text) < 1:
                flash('comment cannot be empty', category='error')
            else:
                new_comment = Comment(comment_time=datetime.now(), comment_text=comment_text, post_id=post_id, user_id=current_user.id)
                db.session.add(new_comment)
                db.session.commit()
                if userID_username_dict.get(new_comment.user_id) == None:
                    userID_username_dict.update({new_comment.user_id: User.query.get(new_comment.user_id).username}) 
                
                flash('Comment added', category='success')

        return render_template("post.html", user=current_user, post=post, usernames=userID_username_dict, post_creator=User.query.get(post.user_id).username)
    else:
        return redirect(url_for('views.home'))

@login_required
@auth.route('/post/deletePost/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    if request.method == 'POST':
        post = Post.query.get(post_id)
        if post:
            #first delete all the comments associated to the post
            for c in post.comments:
                comment = Comment.query.get(c.id)
                db.session.delete(comment)
                db.session.commit()

            db.session.delete(post)
            db.session.commit()
            flash('Post deleted', category='success')
        else:
            flash('An error occurred', category='error')

    return redirect(url_for('views.home'))


@login_required
@auth.route('/post/deleteComment/<int:comment_id>', methods=['GET', 'POST'])
def delete_comment(comment_id):
    
    comment = Comment.query.get(comment_id)
    post_id = comment.post_id

    if request.method == 'POST':
        if comment:
            db.session.delete(comment)
            db.session.commit()
            flash('Comment deleted', category='success')
        else:
            flash('An error occurred', category='error')
            
    return redirect("/post/" + str(post_id))
