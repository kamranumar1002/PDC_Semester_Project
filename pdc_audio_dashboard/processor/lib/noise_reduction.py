import numpy as np
from scipy.io.wavfile import read, write
from logmmse import logmmse_from_file

def noise_reduction(input_wav_path, output_wav_path):
    fs, _ = read(input_wav_path)
    processed_audio = logmmse_from_file(input_wav_path)

    processed_audio = processed_audio.astype(np.float32)
    processed_audio /= np.max(np.abs(processed_audio))

    processed_audio[np.abs(processed_audio) < 0.01] = 0

    write(output_wav_path, fs, processed_audio)
    print(f"Noise-reduced audio saved to: {output_wav_path}")
