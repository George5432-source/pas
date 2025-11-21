from django.db import models

class CrimeRecord(models.Model):
    """
    Store preprocessed and feature-engineered crime records.
    Raw CSV/Parquet files are NOT stored in the DB.
    """
    # Original raw fields (after preprocessing)
    date = models.DateTimeField(db_index=True)
    primary_type = models.CharField(max_length=100, db_index=True)
    arrest = models.BooleanField(null=True)
    domestic = models.BooleanField(null=True)

    # Metadata / engineered features
    month = models.IntegerField(null=True)
    hour = models.IntegerField(null=True)
    minute = models.IntegerField(null=True)
    day_of_week = models.IntegerField(null=True)

    is_weekend = models.BooleanField(null=True)
    is_night = models.BooleanField(null=True)
    season = models.IntegerField(null=True)  # encoded 0..3

    # Target variable
    is_violent_crime = models.BooleanField(db_index=True)

    # Time-series features
    crime_count = models.IntegerField(null=True)
    lag_1h = models.FloatField(null=True)
    lag_2h = models.FloatField(null=True)
    lag_3h = models.FloatField(null=True)

    lag_v_1h = models.FloatField(null=True)
    lag_v_2h = models.FloatField(null=True)
    lag_v_3h = models.FloatField(null=True)

    rolling_3h = models.FloatField(null=True)
    rolling_v_3h = models.FloatField(null=True)

    # Cyclical features
    hour_sin = models.FloatField(null=True)
    hour_cos = models.FloatField(null=True)
    day_sin = models.FloatField(null=True)
    day_cos = models.FloatField(null=True)

    # Encoded primary type
    primary_type_code = models.IntegerField(db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['primary_type']),
            models.Index(fields=['is_violent_crime']),
        ]

    def __str__(self):
        return f"{self.date} - {self.primary_type}"

