"""
Evaluate classifier: metrics (ROC-AUC, precision, recall, F1, accuracy) and y_proba.
"""
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def evaluate_classifier(
    pipeline,
    X,
    y_true,
    prefix: str = "",
) -> tuple[dict[str, float], np.ndarray]:
    """
    Run pipeline.predict and predict_proba on X; compute metrics vs y_true.
    Returns (metrics_dict, y_proba) where y_proba is P(churn=1).
    """
    y_pred = pipeline.predict(X)
    try:
        y_proba = pipeline.predict_proba(X)[:, 1]
    except Exception:
        y_proba = np.full(len(y_true), np.nan)

    metrics = {}
    if prefix:
        sep = "_"
    else:
        sep = ""

    def k(name: str) -> str:
        return f"{prefix}{sep}{name}" if prefix else name

    metrics[k("roc_auc")] = float(roc_auc_score(y_true, y_proba)) if np.isfinite(y_proba).all() else 0.0
    metrics[k("precision")] = float(precision_score(y_true, y_pred, zero_division=0))
    metrics[k("recall")] = float(recall_score(y_true, y_pred, zero_division=0))
    metrics[k("f1")] = float(f1_score(y_true, y_pred, zero_division=0))
    metrics[k("accuracy")] = float(accuracy_score(y_true, y_pred))

    return metrics, y_proba
