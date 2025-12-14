# resample.py

import librosa
import soundfile as sf

def resample_audio(input_path, output_path, target_sr=16000):
    """
    Resample audio to a target sample rate.
    
    Args:
        input_path (str): Path to input WAV file.
        output_path (str): Path to save resampled WAV file.
        target_sr (int): Target sample rate (default 16 kHz for speech).
    
    Returns:
        str: Path to resampled audio file.
    """
    # Load audio with librosa
    y, sr = librosa.load(input_path, sr=None)  # sr=None preserves original rate
    # Resample
    y_resampled = librosa.resample(y, orig_sr=sr, target_sr=target_sr)
    # Save resampled audio
    sf.write(output_path, y_resampled, target_sr)
    print(f"Resampled audio saved to: {output_path}")
    return output_path
