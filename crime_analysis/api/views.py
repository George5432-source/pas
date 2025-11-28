# Django & DRF
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
# Serializers
from .serializers import UploadDatasetSerializer, StartAnalysisSerializer


from crime_analysis.processing.feature_engineering import add_lag_features, add_cyclic_features

from crime_analysis.processing.preprocessing import preprocess_raw

from crime_analysis.processing.ml_models import train_models


from .storage import DATASETS


import pandas as pd


from crime_analysis.database.load import save_to_db


# class DashboardAPIView(APIView):
#     """
#     Main dashboard: links to Upload, Analysis, Evaluation, Visualization
#     """
#     def get(self, request):
#         dataset_id = request.session.get("dataset_id")
#         df_loaded = dataset_id in DATASETS if dataset_id else False
#         preprocessed = request.session.get("preprocessed", False)
#         visualized = request.session.get("visualized", False)
#
#         return render(request, "webapp/dashboard.html", {
#             "dataset_id": dataset_id,
#             "df_loaded": df_loaded,
#             "preprocessed": preprocessed,
#             "visualized": visualized,
#         })


class UploadDatasetAPIView(APIView):
    """
    Upload CSV/Parquet file and store the raw dataframe in memory.
    """

    def post(self, request):
        serializer = UploadDatasetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        file = serializer.validated_data["file"]

        # Read file
        filename = file.name.lower()
        if filename.endswith(".csv"):
            df = pd.read_csv(file)
        elif filename.endswith(".parquet"):
            df = pd.read_parquet(file)
        else:
            return Response({"error": "Unsupported file format"}, status=400)

        # Assign dataset ID
        dataset_id = len(DATASETS) + 1

        # Store ONLY raw dataframe initially
        DATASETS[dataset_id] = {
            "raw_df": df,
            "processed_df": None,
            "results": None,
        }

        # Store dataset ID in session for Django templates
        request.session["dataset_id"] = dataset_id

        return Response(
            {"dataset_id": dataset_id, "rows": df.shape[0]},
            status=201
        )


class StartAnalysisAPIView(APIView):
    """
    Run preprocessing, feature engineering and ML training.
    """

    def post(self, request):
        serializer = StartAnalysisSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        dataset_id = serializer.validated_data["dataset_id"]

        if dataset_id not in DATASETS:
            return Response({"error": "Dataset not found"}, status=404)

        raw_df = DATASETS[dataset_id]["raw_df"]

        if raw_df is None:
            return Response({"error": "No raw dataframe found"}, status=500)

        # ----------- Preprocessing & Feature Engineering -----------
        df = preprocess_raw(raw_df.copy())
        df = add_lag_features(df)
        df = add_cyclic_features(df)

        # ---------------------- Model Training ----------------------
        x_test, y_test, rf_pred, gb_pred = train_models(df)

        # 3. Save to DB
        save_to_db(df)

        # Save everything cleanly
        DATASETS[dataset_id] = {
            "raw_df": raw_df,            # keep original
            "processed_df": df,          # store processed dataset
            "results": {
                "X_test": x_test,
                "y_test": y_test,
                "rf_pred": rf_pred,
                "gb_pred": gb_pred,
            }
        }

        # Mark in the session that preprocessing happened
        request.session["preprocessed"] = True

        return Response(
            {"message": "Analysis completed", "dataset_id": dataset_id}
        )





from ..processing.evaluation import compute_metrics

class EvaluationAPIView(APIView):
    def get(self, request, dataset_id):
        if dataset_id not in DATASETS:
            return Response({"error": "Dataset not found"}, status=404)

        results = DATASETS[dataset_id]["results"]

        if not results:
            return Response({"error": "No analysis performed yet"}, status=400)

        y_test = results["y_test"]

        # Build prediction dict
        model_preds = {
            "Random Forest": results["rf_pred"],
            "Gradient Boosting": results["gb_pred"],
        }

        # Compute metrics
        metrics_df = compute_metrics(y_test, model_preds)

        # Convert DF → HTML table directly
        metrics_html = metrics_df.to_html(classes="table table-striped")

        return render(request, "webapp/evaluation.html", {
            "dataset_id": dataset_id,
            "metrics_table": metrics_html,
            "evaluated": True
        })



from crime_analysis.processing.visualizations import generate_charts

class VisualizationAPIView(APIView):
    def get(self, request, dataset_id):
        if dataset_id not in DATASETS:
            return Response({"error": "Dataset not found"}, status=404)

        df = DATASETS[dataset_id]["processed_df"]
        results = DATASETS[dataset_id]["results"]

        if df is None or results is None:
            return Response({"error": "Analysis not completed"}, status=400)

        charts = generate_charts(
            df,
            rf_pred=results["rf_pred"],
            gb_pred=results["gb_pred"],
            feature_importances=results.get("feature_importances")
        )

        return render(request, "webapp/visualization.html", {
            "dataset_id": dataset_id,
            "charts": charts,
            "visualized": True
        })


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