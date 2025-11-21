import pandas as pd
import numpy as np

def add_lag_features(df: pd.DataFrame) -> pd.DataFrame:
    # Lags
    df['lag_1h'] = df['crime_count'].shift(1)
    df['lag_2h'] = df['crime_count'].shift(2)
    df['lag_3h'] = df['crime_count'].shift(3)

    df['lag_v_1h'] = df['is_violent_crime'].shift(1)
    df['lag_v_2h'] = df['is_violent_crime'].shift(2)
    df['lag_v_3h'] = df['is_violent_crime'].shift(3)

    # Rolling windows
    df['rolling_3h'] = df['crime_count'].rolling(3).mean()
    df['rolling_v_3h'] = df['is_violent_crime'].rolling(3).mean()

    # Drop rows with NaNs from lagging
    df = df.dropna()
    return df

def add_cyclic_features(df: pd.DataFrame) -> pd.DataFrame:
    df['Hour_sin'] = np.sin(2 * np.pi * df['Hour'] / 24)
    df['Hour_cos'] = np.cos(2 * np.pi * df['Hour'] / 24)

    df['Day_sin'] = np.sin(2 * np.pi * df['DayOfWeek'] / 7)
    df['Day_cos'] = np.cos(2 * np.pi * df['DayOfWeek'] / 7)

    # Encode season
    df['Season'] = df['Season'].astype('category').cat.codes

    # Encode Primary Type
    df['Primary Type'] = df['Primary Type'].astype('category')
    df['primary_type_code'] = df['Primary Type'].cat.codes

    return df

