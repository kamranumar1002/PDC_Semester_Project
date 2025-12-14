from pydub import AudioSegment
from pydub.silence import detect_nonsilent

def trim_silence(audio: AudioSegment, min_silence_len=100, silence_thresh=-40):
    nonsilent_ranges = detect_nonsilent(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh
    )

    trimmed_audio = AudioSegment.empty()
    for start, end in nonsilent_ranges:
        trimmed_audio += audio[start:end]

    return trimmed_audio
