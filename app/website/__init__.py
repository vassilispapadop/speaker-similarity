from flask import Flask
from os import path

def create_app():
    #name of the file initialize flask
    app = Flask(__name__)
    # register views/routes
    from .views import views

    app.register_blueprint(views, url_prefix='/')
    # app.register_blueprint(app_api.api_prefix, url_prefix='/api')


    return app
