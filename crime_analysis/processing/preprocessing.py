import pandas as pd
import numpy as np

def get_season(month: int) -> str:
    if month in [12, 1, 2]: return "Winter"
    if month in [3, 4, 5]: return "Spring"
    if month in [6, 7, 8]: return "Summer"
    return "Fall"

def preprocess_raw(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw crime data and add basic metadata.
    """
    # Drop geo columns
    columns_to_drop = [
        'X Coordinate', 'Y Coordinate', 'Latitude', 'Longitude',
        'Location', 'Community Area', 'Ward'
    ]
    df = df.drop(columns=columns_to_drop, errors='ignore')

    # Fix inconsistent crime names
    df['Primary Type'] = df['Primary Type'].replace(
        {'CRIM SEXUAL ASSAULT': 'CRIMINAL SEXUAL ASSAULT'}
    )

    # Date parsing
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    df['Month'] = df['Date'].dt.month
    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute
    df['DayOfWeek'] = df['Date'].dt.dayofweek
    df['is_weekend'] = df['DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)
    df['is_night'] = df['Hour'].apply(lambda h: 1 if (h >= 22 or h < 6) else 0)
    df['Season'] = df['Month'].apply(get_season)

    # Remove duplicates and empty columns
    df = df.drop_duplicates()
    df = df.dropna(axis=1, how='all')

    # Target variable: violent crimes
    violent_types = [
        'ASSAULT', 'BATTERY', 'HOMICIDE',
        'CRIMINAL SEXUAL ASSAULT', 'ROBBERY'
    ]
    df['is_violent_crime'] = df['Primary Type'].isin(violent_types).astype(int)

    # Set time index
    df = df.sort_values('Date')
    df = df.set_index('Date')

    # Initialize crime_count
    df['crime_count'] = 1

    return df

