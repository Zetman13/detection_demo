from django.urls import path
from .views import IndexView, DetectPreloadedView, DetectUploadedView

urlpatterns = [
    path('', IndexView.as_view(), name='detection_index'),
    path('api/detect_preloaded', DetectPreloadedView.as_view(), name='detection_detect_preloaded'),
    path('api/detect_uploaded', DetectUploadedView.as_view(), name='detection_detect_uploaded'),
]
