from rest_framework import serializers

class UploadDatasetSerializer(serializers.Serializer):
    file = serializers.FileField()

class StartAnalysisSerializer(serializers.Serializer):
    dataset_id = serializers.IntegerField()  # optional, if you store datasets

class GetDetectionsSerializer(serializers.Serializer):
    dataset_id = serializers.IntegerField()

class GetMetricsSerializer(serializers.Serializer):
    dataset_id = serializers.IntegerField()
