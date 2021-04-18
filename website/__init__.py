#this file makes the website folder a python package, so that when we import the websit folder, and wheether is in the init file runs automatically when importing the folder
from flask import Flask

def create_app():

    app = Flask(__name__)
    #app.config['SECRET_KEY'] = ''  #for securing session data 
    from .views import views 
    from .auth import auth 

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app
    