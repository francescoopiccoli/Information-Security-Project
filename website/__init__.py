#this file makes the website folder a python package, so that when we import the websit folder, and wheether is in the init file runs automatically when importing the folder
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_database(app):
        if not path.exists('website/' + DB_NAME):
            db.create_all(app=app)
            print('Created Database!')
            
def create_app(): 
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ciao'  #for securing session data 
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views 
    from .auth import auth 

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Post, Comment   
    
    create_database(app)

    return app

    


 
    