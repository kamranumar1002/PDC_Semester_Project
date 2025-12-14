import os
import numpy as np
from scipy.io.wavfile import read, write
from logmmse import logmmse_from_file
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

class AudioProcessor:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        # Convert input audio to WAV format for processing
        self.audio = AudioSegment.from_file(input_file_path)
        self.wav_path = input_file_path.rsplit('.', 1)[0] + "_temp.wav"
        self.audio.export(self.wav_path, format="wav")

    def trim_silence(self, min_silence_len=100, silence_thresh=-40):
        """Remove silent parts and return trimmed audio"""
        nonsilent_ranges = detect_nonsilent(self.audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
        trimmed_audio = AudioSegment.empty()
        for start, end in nonsilent_ranges:
            trimmed_audio += self.audio[start:end]
        return trimmed_audio

    def noise_reduction(self, input_wav_path, output_wav_path):
        """Apply logMMSE noise reduction to WAV audio"""
        fs, _ = read(input_wav_path)
        processed_audio = logmmse_from_file(input_wav_path)

        # Normalize
        processed_audio = processed_audio.astype(np.float32) / np.max(np.abs(processed_audio))
        # Optional: remove very low residual noise
        processed_audio[np.abs(processed_audio) < 0.01] = 0

        # Save output
        write(output_wav_path, fs, processed_audio)
        print(f"Processed audio saved to: {output_wav_path}")

    def process_audio(self, output_folder="output", min_silence_len=100, silence_thresh=-40):
        os.makedirs(output_folder, exist_ok=True)

        print("Trimming silence...")
        trimmed_audio = self.trim_silence(min_silence_len, silence_thresh)
        trimmed_wav_path = os.path.join(output_folder, "trimmed.wav")
        trimmed_audio.export(trimmed_wav_path, format="wav")

        print("Reducing noise...")
        final_output_path = os.path.join(output_folder, "final_output.wav")
        self.noise_reduction(trimmed_wav_path, final_output_path)

        # Cleanup temporary WAV
        if os.path.exists(self.wav_path):
            os.remove(self.wav_path)

        return final_output_path

def main():
    input_file = "/Users/hotelkey/Desktop/demoPDC/audiopath.wav"
    output_dir = "/Users/hotelkey/Desktop/demoPDC/content"
    
    processor = AudioProcessor(input_file)
    final_audio_path = processor.process_audio(output_folder=output_dir, min_silence_len=100, silence_thresh=-40)
    print("All done. Final audio path:", final_audio_path)

if __name__ == "__main__":
    main()
