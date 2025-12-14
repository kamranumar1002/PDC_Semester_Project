# clipping.py

import numpy as np
import soundfile as sf
import librosa

def detect_clipping(audio_data, threshold=0.99):
    """
    Detect if audio is clipped.
    Returns True if clipping detected, else False.
    """
    max_val = np.max(np.abs(audio_data))
    return max_val >= threshold

def repair_clipping(input_path, output_path, threshold=0.99):
    """
    Repair clipping by soft-limiting and pre-emphasis.
    """
    # Load audio
    audio_data, sr = librosa.load(input_path, sr=None, mono=False)

    # Soft-limit peaks
    audio_data = np.clip(audio_data, -threshold, threshold)

    # Optional: apply pre-emphasis to improve signal
    audio_data = librosa.effects.preemphasis(audio_data)

    # Save repaired audio
    sf.write(output_path, audio_data.T, sr)  # Transpose if multi-channel
    return output_path

# Add below existing functions
def repair_clipping_array(audio_data, threshold=0.99):
    audio_data = np.clip(audio_data, -threshold, threshold)
    return librosa.effects.preemphasis(audio_data)