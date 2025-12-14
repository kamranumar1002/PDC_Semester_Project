import os
import time
import psutil
import concurrent.futures
from django.conf import settings
from django.utils import timezone
from .models import ProcessedResult
from .worker import process_file_task  # Import from the clean file

class ExperimentRunner:
    """Orchestrates the Serial vs Parallel execution."""

    def __init__(self, experiment_obj):
        self.experiment = experiment_obj
        self.batch = experiment_obj.batch
        self.files = self.batch.files.all()

    def run(self):
        self.experiment.status = 'PROCESSING'
        self.experiment.start_time = timezone.now()
        
        # Capture CPU usage baseline
        psutil.cpu_percent(interval=None) 
        
        self.experiment.save()

        # Prepare arguments (Must be simple types: strings, ints)
        # We do NOT pass model instances to the worker
        tasks = []
        for audio_file in self.files:
            input_path = audio_file.file.path
            output_root = str(settings.MEDIA_ROOT) # Pass as string
            file_id = audio_file.id
            tasks.append((input_path, output_root, file_id))

        results = []
        start_perf = time.perf_counter()

        try:
            if self.experiment.mode == 'SERIAL':
                self.experiment.cpu_cores_used = 1
                for task_args in tasks:
                    # Unpack arguments manually for direct call
                    res = process_file_task(*task_args)
                    results.append(res)
                    
            elif self.experiment.mode == 'PARALLEL':
                # Determine max workers
                core_count = os.cpu_count() or 4
                self.experiment.cpu_cores_used = core_count
                
                # Use ProcessPoolExecutor for robust Windows handling
                with concurrent.futures.ProcessPoolExecutor(max_workers=core_count) as executor:
                    # Submit all tasks
                    future_to_file = {
                        executor.submit(process_file_task, t[0], t[1], t[2]): t 
                        for t in tasks
                    }
                    
                    # Collect results as they finish
                    for future in concurrent.futures.as_completed(future_to_file):
                        try:
                            data = future.result()
                            results.append(data)
                        except Exception as exc:
                            print(f"Worker generated an exception: {exc}")

        except Exception as e:
            print(f"Critical Experiment Error: {e}")
            self.experiment.status = 'FAILED'
            self.experiment.save()
            return

        end_perf = time.perf_counter()

        # Save Metrics
        self.experiment.end_time = timezone.now()
        self.experiment.duration_seconds = end_perf - start_perf
        self.experiment.status = 'COMPLETED'
        self.experiment.save()

        # Save Results to DB (This happens in the Main Django Process, so Models are safe here)
        print(f"Saving {len(results)} results to DB...")
        for res in results:
            if res['success']:
                # The worker returns the absolute path. We need relative for Django FileField.
                # However, our worker also returns 'relative_dir'.
                
                # Construct the relative path string for the FileField
                # Format: processed/run_timestamp/filename_final_output.wav
                filename = os.path.basename(res['processed_path'])
                relative_file_path = os.path.join(res['relative_dir'], filename).replace("\\", "/")

                ProcessedResult.objects.create(
                    experiment=self.experiment,
                    original_file_id=res['original_id'],
                    processed_file=relative_file_path,
                    spectrogram_path=res.get('spectrogram_path'),
                    processing_time_ms=res['duration'] * 1000
                )
            else:
                print(f"Skipping failed result for file {res['original_id']}")

        return self.experiment  