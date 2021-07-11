from __future__ import unicode_literals
import youtube_dl
import subprocess
import librosa
import pandas as pd
import numpy as np
import sys
import glob
import os
from . import nn_model


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

    #return list with parts names
    return glob.glob('app/website/downloads/parts/*.wav')


ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'app/website/downloads/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192'
    }],
    'postprocessor_args': [
        '-ar', '16000'
    ],
    'prefer_ffmpeg': True,
    'keepvideo': True
}

def download_audio(file='http://www.youtube.com/watch?v=BaW_jenozKc'):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([file])
    
    return get_name()


def extract_mfcc(row, nr_mfcc):
    signal ,sr = librosa.load(row)
    mfcc_feature = librosa.feature.mfcc(signal, n_mfcc=nr_mfcc, sr=sr, hop_length=256)
    delta_feature = librosa.feature.delta(mfcc_feature)
    
    mfcc_feature = np.mean(mfcc_feature.T,axis=0)
    delta_feature = np.mean(delta_feature.T, axis=0)

    return pd.Series([mfcc_feature, delta_feature])

def predict(clips):
    pred_dict = {}
    for clip in clips:
        tmp = pd.DataFrame()
        tmp[['mfcc', 'delta']] = extract_mfcc(clip,20)
        X_tmp = np.hstack((tmp['mfcc'].to_list(),tmp['delta'].to_list()))
        X_tmp = np.expand_dims(X_tmp, axis=0)
        print(X_tmp.shape)
        y_pred = nn_model.predict(X_tmp)
        pred_dict[clip] = y_pred

    return pred_dict
    
