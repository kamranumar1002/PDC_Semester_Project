import threading
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import AudioBatch, AudioFile, ProcessingExperiment
from .serializers import AudioBatchSerializer, ExperimentSerializer
from .utils import ExperimentRunner

class BatchViewSet(viewsets.ModelViewSet):
    queryset = AudioBatch.objects.all()
    serializer_class = AudioBatchSerializer

    @action(detail=False, methods=['POST'])
    def upload(self, request):
        """
        Expects 'files' in request.FILES. 
        Creates a Batch and associated AudioFiles.
        """
        files = request.FILES.getlist('files')
        if not files:
            return Response({'error': 'No files provided'}, status=status.HTTP_400_BAD_REQUEST)

        batch = AudioBatch.objects.create(name=f"Batch {len(files)} files")
        
        audio_objects = [
            AudioFile(batch=batch, file=f, original_name=f.name)
            for f in files
        ]
        AudioFile.objects.bulk_create(audio_objects)

        return Response(AudioBatchSerializer(batch).data, status=status.HTTP_201_CREATED)

class ExperimentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View to trigger experiments and view results.
    """
    queryset = ProcessingExperiment.objects.all()
    serializer_class = ExperimentSerializer

    @action(detail=False, methods=['POST'])
    def start(self, request):
        """
        Payload: { "batch_id": 1, "mode": "PARALLEL" }
        """
        batch_id = request.data.get('batch_id')
        mode = request.data.get('mode', 'SERIAL')

        try:
            batch = AudioBatch.objects.get(id=batch_id)
        except AudioBatch.DoesNotExist:
            return Response({'error': 'Batch not found'}, status=404)

        experiment = ProcessingExperiment.objects.create(
            batch=batch,
            mode=mode,
            status='PENDING'
        )

        # Run processing in a separate thread to avoid blocking the HTTP response
        thread = threading.Thread(target=self._run_background, args=(experiment,))
        thread.start()

        return Response(ExperimentSerializer(experiment).data)

    def _run_background(self, experiment):
        runner = ExperimentRunner(experiment)
        runner.run()