from rest_framework import serializers
from .models import AudioBatch, AudioFile, ProcessingExperiment, ProcessedResult

class AudioFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFile
        fields = ['id', 'file', 'original_name', 'file_size_bytes']

class AudioBatchSerializer(serializers.ModelSerializer):
    files = AudioFileSerializer(many=True, read_only=True)
    class Meta:
        model = AudioBatch
        fields = ['id', 'name', 'created_at', 'files']

class ProcessedResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedResult
        fields = ['id', 'processed_file', 'spectrogram_path', 'processing_time_ms']

class ExperimentSerializer(serializers.ModelSerializer):
    results = ProcessedResultSerializer(many=True, read_only=True)
    class Meta:
        model = ProcessingExperiment
        fields = '__all__'