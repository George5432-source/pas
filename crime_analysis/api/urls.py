from django.urls import path
from .views import (
    UploadDatasetAPIView,
    StartAnalysisAPIView,
    GetDetectionsAPIView,
    GetMetricsAPIView,

)

# from .views import ExportMetricsPDFAPIView

urlpatterns = [
    path('upload/', UploadDatasetAPIView.as_view(), name='upload-dataset'),
    path('start-analysis/', StartAnalysisAPIView.as_view(), name='start-analysis'),
    path('detections/', GetDetectionsAPIView.as_view(), name='get-detections'),
    path('metrics/', GetMetricsAPIView.as_view(), name='get-metrics'),
    # path('export/pdf/', ExportMetricsPDFAPIView.as_view(), name='export_pdf'),
]
