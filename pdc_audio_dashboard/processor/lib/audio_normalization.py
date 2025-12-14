# audio_normalization.py

from pydub import AudioSegment
import pyloudnorm as pyln
import soundfile as sf
import numpy as np

def normalize_peak(audio: AudioSegment, target_dBFS=-1.0):
    """
    Normalize the audio to a target peak dBFS.
    
    :param audio: AudioSegment object
    :param target_dBFS: target peak in dBFS (default -1 dB)
    :return: normalized AudioSegment
    """
    change_in_dBFS = target_dBFS - audio.max_dBFS
    return audio.apply_gain(change_in_dBFS)


def normalize_lufs(input_wav, output_wav, target_lufs=-23.0):
    """
    Normalize the audio to a target LUFS level.
    
    :param input_wav: path to input wav file
    :param output_wav: path to output normalized wav
    :param target_lufs: target loudness in LUFS
    """
    data, rate = sf.read(input_wav)
    
    meter = pyln.Meter(rate)  # create LUFS meter
    loudness = meter.integrated_loudness(data)
    
    # Apply gain to reach target LUFS
    normalized_audio = pyln.normalize.loudness(data, loudness, target_lufs)
    
    # Save normalized audio
    sf.write(output_wav, normalized_audio, rate)
