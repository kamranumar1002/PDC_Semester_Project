# main.py
from pathlib import Path
from audio_processor import AudioProcessor

def main():
    root = Path(__file__).parent
    input_file = str(root / "audiopath.wav")
    output_dir = str(root / "processed")

    processor = AudioProcessor(input_file)
    final_audio_path = processor.process_audio(
        output_folder=output_dir,
        min_silence_len=100,
        silence_thresh=-40
    )

    print("\n🎉 All done!")
    print("Processed audio saved at:", final_audio_path)

if __name__ == "__main__":
    main()