import pandas as pd
from .models import CrimeRecord

def save_to_db(df: pd.DataFrame):
    """
    Save a preprocessed/feature-engineered DataFrame into Django DB.
    """
    records = []

    for idx, row in df.iterrows():
        rec = CrimeRecord(
            date=idx,
            primary_type=str(row['Primary Type']),
            arrest=row.get('Arrest'),
            domestic=row.get('Domestic'),
            month=row.get('Month'),
            hour=row.get('Hour'),
            minute=row.get('Minute'),
            day_of_week=row.get('DayOfWeek'),
            is_weekend=bool(row.get('is_weekend')),
            is_night=bool(row.get('is_night')),
            season=int(row.get('Season')) if row.get('Season') is not None else None,
            is_violent_crime=bool(row.get('is_violent_crime')),
            crime_count=int(row.get('crime_count')) if row.get('crime_count') is not None else None,
            lag_1h=row.get('lag_1h'),
            lag_2h=row.get('lag_2h'),
            lag_3h=row.get('lag_3h'),
            lag_v_1h=row.get('lag_v_1h'),
            lag_v_2h=row.get('lag_v_2h'),
            lag_v_3h=row.get('lag_v_3h'),
            rolling_3h=row.get('rolling_3h'),
            rolling_v_3h=row.get('rolling_v_3h'),
            hour_sin=row.get('Hour_sin'),
            hour_cos=row.get('Hour_cos'),
            day_sin=row.get('Day_sin'),
            day_cos=row.get('Day_cos'),
            primary_type_code=int(row.get('primary_type_code')) if row.get('primary_type_code') is not None else None,
        )
        records.append(rec)

    # Bulk create for efficiency
    CrimeRecord.objects.bulk_create(records)

