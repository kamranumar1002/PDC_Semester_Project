# hum_reduction.py
import numpy as np
from scipy.signal import iirnotch, filtfilt
import soundfile as sf

def remove_hum(input_path, output_path, hum_freq=50.0, Q=30.0):
    """
    Remove electrical hum (50/60 Hz) from audio using a notch filter.
    
    Parameters:
        input_path (str): Path to input WAV
        output_path (str): Path to save cleaned WAV
        hum_freq (float): Frequency to remove (50 or 60 Hz)
        Q (float): Quality factor, higher = narrower notch
    """
    data, sr = sf.read(input_path)
    
    # Handle stereo
    if len(data.shape) == 2:
        data = data.mean(axis=1)  # convert to mono

    # Design notch filter
    b, a = iirnotch(w0=hum_freq/(sr/2), Q=Q)
    filtered = filtfilt(b, a, data)

    # Save
    sf.write(output_path, filtered, sr)
    print(f"Hum removed: {output_path}")

# Add below existing functions
def remove_hum_array(data, sr, hum_freq=50.0, Q=30.0):
    if data.ndim > 1:
        data = data.mean(axis=1)
    b, a = iirnotch(w0=hum_freq/(sr/2), Q=Q)
    return filtfilt(b, a, data)
