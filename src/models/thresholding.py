"""
Threshold analysis: evaluate thresholds 0.1–0.9 (step 0.05), select best by F1.
Outputs: threshold_table.csv, threshold_summary.json.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, precision_score, recall_score


def evaluate_thresholds(y_true: np.ndarray, y_proba: np.ndarray) -> pd.DataFrame:
    """For each threshold in [0.1, 0.15, ..., 0.9], compute precision, recall, F1, n_positive."""
    thresholds = np.arange(0.1, 0.91, 0.05)
    rows = []
    for t in thresholds:
        y_pred = (y_proba >= t).astype(int)
        rows.append({
            "threshold": round(t, 2),
            "precision": float(precision_score(y_true, y_pred, zero_division=0)),
            "recall": float(recall_score(y_true, y_pred, zero_division=0)),
            "f1": float(f1_score(y_true, y_pred, zero_division=0)),
            "n_predicted_positive": int(y_pred.sum()),
        })
    return pd.DataFrame(rows)


def select_best_threshold(threshold_table: pd.DataFrame, metric: str = "f1") -> float:
    """Return threshold that maximizes the given metric (default F1)."""
    idx = threshold_table[metric].idxmax()
    return float(threshold_table.loc[idx, "threshold"])


def save_threshold_results(
    threshold_table: pd.DataFrame,
    best_threshold: float,
    table_path: str | Path,
    summary_path: str | Path,
) -> None:
    """Save threshold_table.csv and threshold_summary.json."""
    table_path = Path(table_path)
    summary_path = Path(summary_path)
    table_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    threshold_table.to_csv(table_path, index=False)
    summary = {"best_threshold": best_threshold, "metric_used": "f1"}
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
