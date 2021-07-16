from __future__ import unicode_literals
from librosa.feature.spectral import zero_crossing_rate
import youtube_dl
import subprocess
import pandas as pd
import numpy as np
import glob
import os
from . import nn_model, gmm_model, classes, metadata
from .extract_features import extract_mfcc, zero_crossing_rate, DEFAULT_SAMPLE_RATE

# Number of splits
audio_splits= 13

# return the newly created .wav file in the directory
def get_name(path='app/website/downloads/*.wav'):
    list_of_files = glob.glob(path) # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def create_segments(path, segment_duration):
    # remove previous wav files
    
    # Get a list of all the file paths that ends with .txt from in specified directory
    fileList = glob.glob('app/website/downloads/parts/*.wav')
    # Iterate over the list of filepaths & remove each file.
    for filePath in fileList:
        try:
            os.remove(filePath)
        except:
            print("Error while deleting file : ", filePath)

    cmd_string = f'ffmpeg -i "{path}" -f segment -segment_time {segment_duration} -c copy app/website/downloads/parts/output%09d.wav'
    subprocess.call(cmd_string, shell=True)

    #return list with parts names, order by creation/modification time
    return sorted(glob.glob('app/website/downloads/parts/*.wav'), key=os.path.getmtime)


ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'app/website/downloads/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192'
    }],
    'postprocessor_args': [
        '-ar', str(DEFAULT_SAMPLE_RATE),
        '-ac', '1'
    ],
    'prefer_ffmpeg': True,
    'keepvideo': False
}

def download_audio(file='http://www.youtube.com/watch?v=BaW_jenozKc'):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([file])
    
    return get_name()

def predict(clips):
    pred_dict = {}
    for clip in clips:
        tmp = pd.DataFrame()
        tmp[['mfcc', 'delta']] = extract_mfcc(clip, audio_splits)
        tmp[['zcr']] = zero_crossing_rate(clip, audio_splits)
        
        X_tmp = np.hstack((tmp['mfcc'].to_list(),tmp['delta'].to_list(), tmp['zcr'].to_list()))
        X_tmp = np.expand_dims(X_tmp, axis=0)
        # predict
        y_pred_nn = nn_model.predict(X_tmp)
        # round probs to 2-decimal places
        y_pred_nn = np.round(y_pred_nn, 2)
        # print(f'Predicting clip: {clip}')
        matched_speaker_nn = metadata.loc[metadata['VoxCeleb1 ID'] == classes[np.argmax(y_pred_nn, axis=1)][0]]

        y_pred_gmm = gmm_model.predict(X_tmp)
        matched_speaker_gmm = metadata.loc[metadata['VoxCeleb1 ID'] == classes[y_pred_gmm][0]]

        print(f'NN matched with speaker: {str(classes[np.argmax(y_pred_nn, axis=1)])}\
            GMM matched with speaker: {str(classes[y_pred_gmm[0]])} ')

        pred_dict[clip.rsplit('/', 1)[-1]] = {'y_pred_nn': y_pred_nn, 
                                             'matched_speaker_nn': matched_speaker_nn['VGGFace1 ID'].values[0],
                                              'y_pred_gmm':y_pred_gmm,
                                             'matched_speaker_gmm':matched_speaker_gmm['VGGFace1 ID'].values[0]}

    return pred_dict
    
