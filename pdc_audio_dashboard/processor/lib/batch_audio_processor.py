# batch_audio_processor.py

import os
from pathlib import Path
from multiprocessing import Pool, cpu_count
from audio_processor import AudioProcessor

def process_file(file_path: str):
    try:
        file_size = os.path.getsize(file_path)
        if file_size < 1000:
            print(f"Skipping {file_path}, file too small.")
            return False, file_path

        processor = AudioProcessor(file_path)
        output_path = processor.process_audio(output_folder="processed")
        print(f"SUCCESS: {file_path} -> {output_path}")
        return True, file_path
    except Exception as e:
        print(f"FAILED: {file_path}, error: {e}")
        return False, file_path


def batch_process(folder_path: str, num_workers: int | None = None):
    if num_workers is None:
        num_workers = max(cpu_count() - 1, 1)

    p = Path(folder_path)
    exts = {".wav", ".mp3", ".flac", ".m4a"}
    audio_files = [str(f) for f in p.iterdir() if f.is_file() and f.suffix.lower() in exts]

    if not audio_files:
        print(f"No audio files found in folder: {folder_path}")
        return

    os.makedirs("processed", exist_ok=True)
    print(f"Processing {len(audio_files)} files using {num_workers} workers...")

    # Tune chunksize to keep workers busy and reduce scheduling overhead
    chunksize = max(1, len(audio_files) // (num_workers * 4))

    success = 0
    failed = 0

    # Limit tasks per child to curb memory bloat
    with Pool(processes=num_workers, maxtasksperchild=10) as pool:
        for ok, fpath in pool.imap_unordered(process_file, audio_files, chunksize=chunksize):
            if ok:
                success += 1
            else:
                failed += 1

    print(f"Done. Success: {success}, Failed: {failed}")


if __name__ == "__main__":
    folder = "input_audio"
    batch_process(folder)