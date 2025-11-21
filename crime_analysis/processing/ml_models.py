import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

def train_models(df: pd.DataFrame):
    # Fill numeric NaNs
    num_cols = df.select_dtypes(include=[float, int]).columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())

    # Drop string columns
    text_cols = df.select_dtypes(include=['object']).columns.tolist()
    df = df.drop(columns=text_cols)

    # Drop target-leakage features
    target_leak_cols = [c for c in df.columns if 'lag_v' in c or 'rolling_v' in c]
    df = df.drop(columns=target_leak_cols, errors='ignore')

    # Features & target
    feature_cols = [c for c in df.columns if c != 'is_violent_crime']
    X = df[feature_cols]
    y = df['is_violent_crime']

    # Time-based split
    train_size = int(0.8 * len(df))
    X_train, X_test = X.iloc[:train_size], X.iloc[train_size:]
    y_train, y_test = y.iloc[:train_size], y.iloc[train_size:]

    # Train models
    rf = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)

    gb = GradientBoostingClassifier(n_estimators=100, max_depth=3, random_state=42)
    gb.fit(X_train, y_train)
    gb_pred = gb.predict(X_test)

    return X_test, y_test, rf_pred, gb_pred

