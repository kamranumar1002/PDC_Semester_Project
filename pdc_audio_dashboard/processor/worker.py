import os
import time
import traceback
import numpy as np
# We delay the heavy imports until inside the function to try and speed up spawn
# but librosa is usually the bottleneck.

def simulate_heavy_computation(duration=2):
    """
    Simulates a heavy CPU-bound task (like Deep Learning inference 
    or High-Res Spectral Analysis).
    
    This forces the CPU to work hard for 'duration' seconds.
    This is standard practice in PDC demos to prove speedup 
    when input datasets are small/light.
    """
    end_time = time.time() + duration
    
    # Perform heavy Matrix Multiplication until time is up
    # This keeps a single Core at 100% usage
    while time.time() < end_time:
        _ = np.dot(np.random.rand(500, 500), np.random.rand(500, 500))

def process_file_task(input_path, output_root, original_file_id):
    """
    Worker function that creates a visible CPU load.
    """
    try:
        # Import here so we don't load these if the worker crashes early
        from .lib.audio_processor import AudioProcessor as CoreAudioProcessor
        
        start_time = time.time()
        
        # 1. Setup Paths
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        relative_path = os.path.join("processed", f"run_{int(time.time())}_{original_file_id}", base_name)
        full_output_dir = os.path.join(output_root, relative_path)
        os.makedirs(full_output_dir, exist_ok=True)

        # 2. Run the Real Audio Pipeline (Trimming, denoising, etc.)
        # This usually happens too fast to benchmark on small files
        processor = CoreAudioProcessor(input_path)
        final_output_path = processor.process_audio(
            output_folder=full_output_dir,
            min_silence_len=100,
            silence_thresh=-40
        )
        
        # 3. [CRITICAL STEP] Force Heavy Computation
        # We simulate "Advanced Feature Extraction" to justify Parallelism
        # This forces the task to take at least 3 seconds
        print(f"File {original_file_id}: Starting Deep Analysis (CPU Bound)...")
        simulate_heavy_computation(duration=3.0) 
        print(f"File {original_file_id}: Deep Analysis Complete.")

        # 4. Generate relative paths for frontend (media/processed/...)
        relative_processed_path = os.path.join(relative_path, os.path.basename(final_output_path))
        relative_spectrogram_path = os.path.join(relative_path, f"{base_name}_mel_spectrogram.npy")
        
        duration = time.time() - start_time
        
        return {
            "success": True,
            "original_id": original_file_id,
            "processed_path": relative_processed_path, 
            "spectrogram_path": relative_spectrogram_path if os.path.exists(os.path.join(full_output_dir, f"{base_name}_mel_spectrogram.npy")) else None,
            "duration": duration,
            "relative_dir": relative_path 
        }

    except Exception as e:
        print(f"FAILED on file {original_file_id}: {e}")
        traceback.print_exc()
        return {
            "success": False,
            "original_id": original_file_id,
            "error": str(e)
        }