from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Post, Comment
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
from sqlalchemy import text


auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        with db.engine.connect() as connection:
            sql = text('SELECT * FROM user WHERE email=\'' + email + "\'") # ' OR 1=1    WHERE email=\'' OR 1=1 OR '       '; DROP TABLE post; SELECT * FROM user where 1=1 OR email='
            print(sql)
            raw_user = connection.execute(sql)
            raw_user = raw_user.mappings().all()
            print(raw_user)

            user = User()
            user.id = raw_user[0].get('id')
            user.email = raw_user[0].get('email')
            user.password = raw_user[0].get('password')
            user.username = raw_user[0].get('username')

        if user:
            if user.password == password:
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
            u = User(email=email, username=fullname, password=password1) #in the secure application we should hash the password with the werkzeug package
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
    if request.method == 'POST':
        post_title = request.form.get('title')
        post_image = request.form.get('picture')
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
                db.session.add(new_comment) #INSERT INTO comment VALUES();
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
