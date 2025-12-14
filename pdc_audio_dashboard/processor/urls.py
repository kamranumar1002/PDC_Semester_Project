from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BatchViewSet, ExperimentViewSet

router = DefaultRouter()
router.register(r'batches', BatchViewSet, basename='batch')
router.register(r'experiments', ExperimentViewSet, basename='experiment')

urlpatterns = [
    path('', include(router.urls)),
]