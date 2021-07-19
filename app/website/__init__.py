from flask import Flask
from os import path
import tensorflow as tf
from tensorflow import keras
import os
import numpy as np
import pandas as pd
import pickle

# Dir with saved models
cwd = os.getcwd()
saved_models_path = os.path.join(cwd,'saved_models/')

# Load Deep Neural Network model
NN_MODEL_NAME = 'speakers_classification.hdf5'
nn_model = keras.models.load_model(saved_models_path + NN_MODEL_NAME)

# Load Gaussian Mixture Models
gmm_files = [os.path.join('saved_models/gmm/',fname) for fname in 
              os.listdir('saved_models/gmm/') if fname.endswith('.sav')]

#Load the Gaussian gender Models
gmm_models = [pickle.load(open(fname,'rb')) for fname in gmm_files]


# Load classes file, order of speakers is preserved
classes = np.load(saved_models_path + 'classes.npy', allow_pickle=True)

# Load metadata csv file to map id to actual person
csv_path = os.path.join(cwd, 'vox_dev_wav/')
metadata = pd.read_csv(csv_path + 'vox1_meta.csv', sep='\t')
metadata = metadata.drop(['Gender',	'Nationality',	'Set'], axis=1)
metadata = metadata[metadata['VoxCeleb1 ID'].isin(classes)]


def create_app():
    #name of the file initialize flask
    app = Flask(__name__)

    print(nn_model.summary())
    print(f'Classes are: {classes}')
    print(f'Current speakers shape: {metadata.shape}')

    # register views/routes
    from .views import views

    app.register_blueprint(views, url_prefix='/')
    # app.register_blueprint(app_api.api_prefix, url_prefix='/api')

    return app
