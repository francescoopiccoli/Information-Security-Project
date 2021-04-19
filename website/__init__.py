#this file makes the website folder a python package, so that when we import the websit folder, and wheether is in the init file runs automatically when importing the folder
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
#DB_NAME = "database.db"

def create_app():

    app = Flask(__name__)
    #app.config['SECRET_KEY'] = ''  #for securing session data 
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'{DB_NAME}' #here goes the URI of the database
    db.init_app(app)

    from .views import views 
    from .auth import auth 

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app
    