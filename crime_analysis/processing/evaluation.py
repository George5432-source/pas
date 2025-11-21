import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
)

def compute_metrics(y_true, y_preds: dict) -> pd.DataFrame:
    """
    y_preds: dict of model_name -> predictions
    """
    rows = []
    for model_name, y_pred in y_preds.items():
        rows.append({
            "Model": model_name,
            "f1_score": f1_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred),
            "recall": recall_score(y_true, y_pred),
            "roc_auc": roc_auc_score(y_true, y_pred),
            "accuracy": accuracy_score(y_true, y_pred)
        })
    return pd.DataFrame(rows)