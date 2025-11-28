from django.urls import path
from .views import (
    # UploadDatasetAPIView,
    # StartAnalysisAPIView,
    # EvaluationAPIView,
    # VisualizationAPIView,
    DashboardAPIView,
)

urlpatterns = [
    # path("upload/", UploadDatasetAPIView.as_view(), name="upload-dataset"),
    # path("start-analysis/", StartAnalysisAPIView.as_view(), name="start-analysis"),
    # path("evaluation/<int:dataset_id>/", EvaluationAPIView.as_view(), name="evaluation"),
    # path("visualization/<int:dataset_id>/", VisualizationAPIView.as_view(), name="visualization"),
    path("dashboard/", DashboardAPIView.as_view(), name="dashboard"),

]