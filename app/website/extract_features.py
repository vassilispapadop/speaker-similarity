import librosa
import pandas as pd
import numpy as np
import sys
import scipy.signal as sps

from pyAudioAnalysis import ShortTermFeatures as aF
from pyAudioAnalysis import audioBasicIO as aIO
import soundfile as sf

DEFAULT_SAMPLE_RATE = 16000

def download_sample(signal, sr, new_sr):
    # Resample data
    number_of_samples = round(len(signal) * float(new_sr) / sr)
    signal = sps.resample(signal, number_of_samples)
    return signal

def get_audio_info(path):
    f = sf.SoundFile(path)
    sr = int(f.samplerate)
    duration = len(f) / f.samplerate
    
    return pd.Series([sr, duration])

def extract_mfcc(clip, nr_mfcc):
    signal ,sr = librosa.load(clip, sr=DEFAULT_SAMPLE_RATE) # downsample all clips to 16KHz
    mfcc_feature = librosa.feature.mfcc(signal, n_mfcc=nr_mfcc, sr=sr, hop_length=256)
    delta_feature = librosa.feature.delta(mfcc_feature)
    
    mfcc_feature = np.mean(mfcc_feature.T,axis=0)
    delta_feature = np.mean(delta_feature.T, axis=0)

    return pd.Series([mfcc_feature, delta_feature])

def zero_crossing_rate(clip, splits):
    # read machine sound
    fs, s = aIO.read_audio_file(clip)

    # re-sample in case sample rate is different than default
    # usually when we process recording
    if fs != DEFAULT_SAMPLE_RATE:
        print(f'Resampling clip: {clip} with rate: {fs}')
        s = download_sample(s,fs, DEFAULT_SAMPLE_RATE)

    duration = len(s) / float(DEFAULT_SAMPLE_RATE)
    window = duration / splits
    # extract short term features and plot ZCR and Energy, get only one channel
    [f, fn] = aF.feature_extraction(s, DEFAULT_SAMPLE_RATE, int(DEFAULT_SAMPLE_RATE * window), int(DEFAULT_SAMPLE_RATE * window))
    # print(f'size {f[0].shape}')
    return f[0]