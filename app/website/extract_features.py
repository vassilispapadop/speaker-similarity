import librosa
import pandas as pd
import numpy as np
import sys

from pyAudioAnalysis import ShortTermFeatures as aF
from pyAudioAnalysis import audioBasicIO as aIO

def extract_mfcc(clip, nr_mfcc):
    signal ,sr = librosa.load(clip)
    mfcc_feature = librosa.feature.mfcc(signal, n_mfcc=nr_mfcc, sr=sr, hop_length=256)
    delta_feature = librosa.feature.delta(mfcc_feature)
    
    mfcc_feature = np.mean(mfcc_feature.T,axis=0)
    delta_feature = np.mean(delta_feature.T, axis=0)

    return pd.Series([mfcc_feature, delta_feature])

def zero_crossing_rate(clip, splits):
    # read machine sound
    fs, s = aIO.read_audio_file(clip)
    duration = len(s) / float(fs)
    window = duration / splits
    # extract short term features and plot ZCR and Energy
    [f, fn] = aF.feature_extraction(s, fs, int(fs * window), int(fs * window))
    # print(f'size {f[0].shape}')
    return f[0]