from django.db import models
import os

class AudioBatch(models.Model):
    """Represents a collection of audio files uploaded together."""
    name = models.CharField(max_length=255, default="Untitled Batch")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.created_at})"

class AudioFile(models.Model):
    """Raw input audio files belonging to a batch."""
    batch = models.ForeignKey(AudioBatch, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    original_name = models.CharField(max_length=255)
    file_size_bytes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.file:
            self.file_size_bytes = self.file.size
            if not self.original_name:
                self.original_name = os.path.basename(self.file.name)
        super().save(*args, **kwargs)

class ProcessingExperiment(models.Model):
    """Tracks a specific execution run (Serial vs Parallel)."""
    MODE_CHOICES = [('SERIAL', 'Serial'), ('PARALLEL', 'Parallel')]
    STATUS_CHOICES = [('PENDING', 'Pending'), ('PROCESSING', 'Processing'), ('COMPLETED', 'Completed'), ('FAILED', 'Failed')]

    batch = models.ForeignKey(AudioBatch, on_delete=models.CASCADE)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    # Metrics
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.FloatField(null=True, blank=True)
    cpu_cores_used = models.IntegerField(default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)

class ProcessedResult(models.Model):
    """The output for a single file in an experiment."""
    experiment = models.ForeignKey(ProcessingExperiment, related_name='results', on_delete=models.CASCADE)
    original_file = models.ForeignKey(AudioFile, on_delete=models.CASCADE)
    processed_file = models.FileField(upload_to='processed/')
    
    # Paths to generated features (stored as JSON or separate fields)
    spectrogram_path = models.CharField(max_length=500, null=True, blank=True)
    processing_time_ms = models.FloatField(help_text="Time taken for this specific file")