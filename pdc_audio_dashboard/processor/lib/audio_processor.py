# audio_processor.py

import os
import numpy as np
from pydub import AudioSegment
from .trim_silence import trim_silence
from .noise_reduction import noise_reduction
from .audio_normalization import normalize_peak
from .resample import resample_audio
from .channel_conversion import convert_to_mono
# from vad import vad_trim  # VAD commented out
from .audio_filter import apply_filter
from .clipping import repair_clipping
from .spectrogram import compute_mel_spectrogram, compute_mfcc, compute_log_mel
from .hum_reduction import remove_hum
import noisereduce as nr
from pydub import effects
import librosa
import soundfile as sf


def enhance_voice(input_path, output_path, sr=16000, gain_db=6):
    """
    Enhance speech in noisy audio:
    - Mild noise reduction
    - Apply gain / compression
    """
    # Load audio
    y, sr = librosa.load(input_path, sr=sr)

    # Estimate noise from first 0.5 sec
    noise_clip = y[:int(0.5*sr)]

    # Mild noise reduction
    reduced = nr.reduce_noise(y=y, y_noise=noise_clip, sr=sr, prop_decrease=0.8)

    # Save temporarily
    temp_path = output_path.rsplit('.', 1)[0] + "_tmp.wav"
    sf.write(temp_path, reduced, sr)

    # Apply gain / compression with pydub
    audio = AudioSegment.from_file(temp_path)
    compressed = effects.compress_dynamic_range(audio, threshold=-20.0, ratio=3.0)
    boosted = compressed.apply_gain(gain_db)

    boosted.export(output_path, format="wav")
    os.remove(temp_path)


class AudioProcessor:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.audio = AudioSegment.from_file(input_file_path)

    def process_audio(
        self,
        output_folder="processed",
        min_silence_len=100,
        silence_thresh=-40,
        target_sr=16000,
        hum_freq=50.0
    ):
        os.makedirs(output_folder, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(self.input_file_path))[0]

        # Step 1: Trim silence
        trimmed_audio = trim_silence(self.audio, min_silence_len, silence_thresh)
        trimmed_wav_path = os.path.join(output_folder, f"{base_name}_trimmed.wav")
        trimmed_audio.export(trimmed_wav_path, format="wav")

        # Step 2: Noise reduction
        noise_reduced_path = os.path.join(output_folder, f"{base_name}_noise_reduced.wav")
        noise_reduction(trimmed_wav_path, noise_reduced_path)

        # Step 3: Sample rate conversion
        resampled_path = os.path.join(output_folder, f"{base_name}_resampled.wav")
        resample_audio(noise_reduced_path, resampled_path, target_sr=target_sr)

        # Step 4: Channel conversion
        mono_path = os.path.join(output_folder, f"{base_name}_mono.wav")
        convert_to_mono(resampled_path, mono_path)

        # Step 5: Clipping Detection & Repair
        clipping_path = os.path.join(output_folder, f"{base_name}_clipping.wav")
        repair_clipping(mono_path, clipping_path)

        # Step 6: Voice-centered bandpass filter
        voice_filtered_path = os.path.join(output_folder, f"{base_name}_voice_filtered.wav")
        apply_filter(clipping_path, voice_filtered_path, filter_type='bandpass', low_cut=80, high_cut=3500)

        # Step 7: Hum removal
        hum_removed_path = os.path.join(output_folder, f"{base_name}_hum_removed.wav")
        remove_hum(voice_filtered_path, hum_removed_path, hum_freq=hum_freq, Q=30.0)

        # Step 8: Voice enhancement
        enhanced_path = os.path.join(output_folder, f"{base_name}_voice_enhanced.wav")
        enhance_voice(hum_removed_path, enhanced_path, gain_db=6)

        # Step 9: Normalization
        normalized_audio = AudioSegment.from_file(enhanced_path)
        normalized_audio = normalize_peak(normalized_audio)
        normalized_path = os.path.join(output_folder, f"{base_name}_final_output.wav")
        normalized_audio.export(normalized_path, format="wav")

        # Step 10: Spectrogram features
        # Replace spectrogram section with array-based computation to avoid re-read
        y, sr = librosa.load(normalized_path, sr=16000, mono=True)
        mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, hop_length=512)
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        mfcc_feat = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=512)
        log_mel_spec = librosa.power_to_db(mel_spec)

        np.save(os.path.join(output_folder, f"{base_name}_mel_spectrogram.npy"), mel_spec_db)
        np.save(os.path.join(output_folder, f"{base_name}_mfcc.npy"), mfcc_feat)
        np.save(os.path.join(output_folder, f"{base_name}_log_mel.npy"), log_mel_spec)

        # Cleanup intermediate files
        for f in [trimmed_wav_path, noise_reduced_path, resampled_path,
                  mono_path, clipping_path, voice_filtered_path, hum_removed_path, enhanced_path]:
            if os.path.exists(f):
                os.remove(f)

        return normalized_path
