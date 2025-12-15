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
    processed_file = serializers.FileField(use_url=True)
    # Add this line so we can play the original input:
    original_file_url = serializers.FileField(source='original_file.file', use_url=True, read_only=True) 
    class Meta:
        model = ProcessedResult
        fields = ['id', 'processed_file', 'original_file_url', 'spectrogram_path', 'processing_time_ms']

class ExperimentSerializer(serializers.ModelSerializer):
    results = ProcessedResultSerializer(many=True, read_only=True)
    class Meta:
        model = ProcessingExperiment
        fields = '__all__'