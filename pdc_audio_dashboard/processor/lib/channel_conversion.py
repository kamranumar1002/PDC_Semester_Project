# channel_conversion.py

from pydub import AudioSegment

def convert_to_mono(input_path, output_path):
    """
    Convert audio to mono.
    
    Args:
        input_path (str): Path to input audio file.
        output_path (str): Path to save mono audio.
    
    Returns:
        str: Path to mono audio file.
    """
    audio = AudioSegment.from_file(input_path)
    
    # Convert to mono if not already
    if audio.channels > 1:
        audio = audio.set_channels(1)
    
    audio.export(output_path, format="wav")
    print(f"Mono audio saved to: {output_path}")
    return output_path
