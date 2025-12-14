# vad.py
import webrtcvad
import wave
import contextlib
from pydub import AudioSegment

def vad_trim(input_path, output_path, aggressiveness=2):
    """
    Remove non-speech segments using VAD.

    Args:
        input_path (str): Path to input WAV (16kHz mono PCM)
        output_path (str): Path to save VAD-trimmed audio
        aggressiveness (int): 0-3, higher = more aggressive trimming
    """
    # Ensure input is WAV 16kHz mono
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    audio.export(input_path, format="wav")

    vad = webrtcvad.Vad(aggressiveness)

    frames = []
    with contextlib.closing(wave.open(input_path, 'rb')) as wf:
        sample_rate = wf.getframerate()
        n_channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        n_frames = wf.getnframes()
        pcm_data = wf.readframes(n_frames)

        # WebRTC VAD works with 10/20/30ms frames
        frame_duration = 30  # ms
        frame_size = int(sample_rate * frame_duration / 1000) * 2  # 16-bit samples
        for start in range(0, len(pcm_data), frame_size):
            frame = pcm_data[start:start + frame_size]
            if len(frame) < frame_size:
                break
            if vad.is_speech(frame, sample_rate):
                frames.append(frame)

    # Write trimmed audio
    with wave.open(output_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

    print(f"VAD-trimmed audio saved to: {output_path}")
    return output_path
