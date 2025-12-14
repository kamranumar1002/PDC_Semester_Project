import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter

def butter_filter(data, sr, cutoff, btype='low', order=5):
    nyq = 0.5 * sr

    # Ensure cutoff is less than Nyquist
    if isinstance(cutoff, list):
        normal_cutoff = [min(f / nyq, 0.999) for f in cutoff]
    else:
        normal_cutoff = min(cutoff / nyq, 0.999)

    b, a = butter(order, normal_cutoff, btype=btype, analog=False)

    # Handle multi-channel audio by filtering each channel
    if data.ndim == 1:
        filtered = lfilter(b, a, data)
    else:
        filtered = np.zeros_like(data)
        for ch in range(data.shape[1]):
            filtered[:, ch] = lfilter(b, a, data[:, ch])
    return filtered

def apply_filter(input_path, output_path, filter_type='bandpass', low_cut=80, high_cut=8000):
    data, sr = sf.read(input_path)
    
    if high_cut >= sr / 2:
        print(f"Warning: high_cut ({high_cut}) >= Nyquist ({sr/2}), reducing to Nyquist-1 Hz")
        high_cut = sr / 2 - 1

    if filter_type == 'low':
        filtered_data = butter_filter(data, sr, high_cut, btype='low')
    elif filter_type == 'high':
        filtered_data = butter_filter(data, sr, low_cut, btype='high')
    elif filter_type == 'bandpass':
        filtered_data = butter_filter(data, sr, [low_cut, high_cut], btype='band')
    else:
        raise ValueError("Invalid filter type")

    sf.write(output_path, filtered_data, sr)
    print(f"Filtered audio saved to: {output_path}")

# Add below existing functions
def apply_filter_array(data, sr, filter_type='bandpass', low_cut=80, high_cut=8000):
    if high_cut >= sr / 2:
        high_cut = sr / 2 - 1
    if filter_type == 'low':
        return butter_filter(data, sr, high_cut, btype='low')
    elif filter_type == 'high':
        return butter_filter(data, sr, low_cut, btype='high')
    elif filter_type == 'bandpass':
        return butter_filter(data, sr, [low_cut, high_cut], btype='band')
    else:
        raise ValueError("Invalid filter type")