from __future__ import unicode_literals
from librosa.feature.spectral import zero_crossing_rate
import youtube_dl
import subprocess
import librosa
import pandas as pd
import numpy as np
import sys
import glob
import os
from . import nn_model, classes, metadata
from .extract_features import extract_mfcc, zero_crossing_rate

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
        '-ar', '16000',
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
        y_pred = nn_model.predict(X_tmp)
        # round probs to 2-decimal places
        y_pred = np.round(y_pred, 2)
        print(f'Matched with speaker: {str(classes[np.argmax(y_pred, axis=1)])}')
        speaker = metadata.loc[metadata['VoxCeleb1 ID'] == classes[np.argmax(y_pred, axis=1)][0]]

        pred_dict[clip.rsplit('/', 1)[-1]] = {'preds': y_pred, 'speaker': speaker['VGGFace1 ID'].values[0]}

    return pred_dict
    
