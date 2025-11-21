import pandas as pd
from rest_framework.views import APIView

from .serializers import UploadDatasetSerializer, StartAnalysisSerializer
from crime_analysis.processing.preprocessing import preprocess_raw
from crime_analysis.processing.feature_engineering import add_lag_features, add_cyclic_features
from crime_analysis.processing.ml_models import train_models
from crime_analysis.processing.evaluation import compute_metrics
from rest_framework.response import Response

# Temporary in-memory storage for simplicity
DATASETS = {}

class UploadDatasetAPIView(APIView):
    """
    Upload CSV/Parquet file and store it in memory (or filesystem).
    """
    def post(self, request):
        serializer = UploadDatasetSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            # Load CSV into pandas
            df = pd.read_csv(file)
            dataset_id = len(DATASETS) + 1
            request.session["dataset_id"] = dataset_id
            return Response({"dataset_id": dataset_id, "rows": df.shape[0]}, status=201)
        return Response(serializer.errors, status=400)


class StartAnalysisAPIView(APIView):
    """
    Start preprocessing, feature engineering, and ML analysis.
    """
    def post(self, request):
        serializer = StartAnalysisSerializer(data=request.data)
        if serializer.is_valid():
            dataset_id = serializer.validated_data['dataset_id']
            if dataset_id not in DATASETS:
                return Response({"error": "Dataset not found"}, status=404)

            df = DATASETS[dataset_id]

            # Preprocess
            df = preprocess_raw(df)
            df = add_lag_features(df)
            df = add_cyclic_features(df)

            # Train models
            x_test, y_test, rf_pred, gb_pred = train_models(df)

            # Store predictions in memory
            DATASETS[dataset_id] = {
                "df": df,
                "X_test": x_test,
                "y_test": y_test,
                "rf_pred": rf_pred,
                "gb_pred": gb_pred
            }

            return Response({"message": "Analysis completed", "dataset_id": dataset_id})
        return Response(serializer.errors, status=400)


class GetDetectionsAPIView(APIView):
    """
    Return predictions for the dataset.
    """
    def get(self, request):
        dataset_id = request.query_params.get("dataset_id")
        if not dataset_id:
            return Response({"error": "dataset_id required"}, status=400)
        dataset_id = int(dataset_id)
        if dataset_id not in DATASETS:
            return Response({"error": "Dataset not found"}, status=404)

        data = DATASETS[dataset_id]
        x_test = data['X_test']
        rf_pred = data['rf_pred']
        gb_pred = data['gb_pred']

        # Return predictions as JSON
        return Response({
            "rf_pred": rf_pred.tolist(),
            "gb_pred": gb_pred.tolist(),
            "X_test_columns": x_test.columns.tolist()
        })


class GetMetricsAPIView(APIView):
    """
    Return evaluation metrics for the dataset.
    """
    def get(self, request):
        dataset_id = request.query_params.get("dataset_id")
        if not dataset_id:
            return Response({"error": "dataset_id required"}, status=400)
        dataset_id = int(dataset_id)
        if dataset_id not in DATASETS:
            return Response({"error": "Dataset not found"}, status=404)

        data = DATASETS[dataset_id]
        y_test = data['y_test']
        rf_pred = data['rf_pred']
        gb_pred = data['gb_pred']

        metrics_df = compute_metrics(
            y_test,
            {"Random Forest": rf_pred, "Gradient Boosting": gb_pred}
        )

        return Response(metrics_df.to_dict(orient="records"))


# class ExportMetricsPDFAPIView(APIView):
#     """
#     Endpoint to export latest metrics as PDF.
#     GET /api/export/pdf/
#     """
#
#     def get(self, request, format=None):
#         # Here you get the latest metrics from your processing module
#         metrics_table = compute_metrics()
#         if metrics_table is None:
#             return Response({"error": "No metrics available"}, status=status.HTTP_400_BAD_REQUEST)
#
#         return export_metrics_pdf(metrics_table)