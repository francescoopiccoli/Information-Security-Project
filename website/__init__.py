#this file makes the website folder a python package, so that when we import the websit folder, and wheether is in the init file runs automatically when importing the folder
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()
DB_NAME = "database.db"

def create_database(app):
        if not path.exists('website/' + DB_NAME):
            db.create_all(app=app)
            print('Created Database!')
            
def create_app(): 
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '0631188pa0b13ce0c676ader280ba245'  #for securing session data 
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['WTF_CSFR_ENABLED'] =True
    db.init_app(app)

    
    from .views import views 
    from .auth import auth 

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Post, Comment   
    
    create_database(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)
    
    # Don't have csrf tokens expire (they are invalid after logout)
    app.config["WTF_CSRF_TIME_LIMIT"] = None

    # Avoid any further csrf tokens expiration
    app.config["SECURITY_CSRF_COOKIE_REFRESH_EACH_REQUEST"] = False

    # You can't get the cookie until you are logged in.
    app.config["SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS"] = True
    csrf = CSRFProtect()
    csrf.init_app(app)

    #this is telling how we load a user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) #get is similar to filter_by, by defaults its gonna look for the primary key

    return app

    


 
    