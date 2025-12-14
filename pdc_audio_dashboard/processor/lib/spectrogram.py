# spectrogram.py

import librosa
import numpy as np

def compute_mel_spectrogram(wav_path, sr=16000, n_mels=128, hop_length=512):
    y, sr = librosa.load(wav_path, sr=sr)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels, hop_length=hop_length)
    S_db = librosa.power_to_db(S, ref=np.max)
    return S_db

def compute_mfcc(wav_path, sr=16000, n_mfcc=13, hop_length=512):
    y, sr = librosa.load(wav_path, sr=sr)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc, hop_length=hop_length)
    return mfccs

def compute_log_mel(wav_path, sr=16000, n_mels=128, hop_length=512):
    y, sr = librosa.load(wav_path, sr=sr)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels, hop_length=hop_length)
    log_S = librosa.power_to_db(S)
    return log_S
