from flask import Flask
from os import path
import tensorflow as tf
from tensorflow import keras
import os
import numpy as np

# Load speakers nn model
cwd = os.getcwd()
MODEL_NAME = 'speakers_classification.hdf5'
model_path = os.path.join(cwd,'saved_models/')
nn_model = keras.models.load_model(model_path + MODEL_NAME)
# Load classes file, order of speakers is preserved
classes = np.load(model_path + 'classes.npy', allow_pickle=True)

def create_app():
    #name of the file initialize flask
    app = Flask(__name__)

    print(nn_model.summary())

    # register views/routes
    from .views import views

    app.register_blueprint(views, url_prefix='/')
    # app.register_blueprint(app_api.api_prefix, url_prefix='/api')

    return app
