"""
Error analysis: FP/FN breakdown, segment analysis (tenure_group, Contract).
Outputs: error_analysis_detailed.csv, error_summary.json, error_by_tenure_group.csv, error_by_contract.csv.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd


def build_prediction_analysis_df(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_proba: np.ndarray,
    segment_df: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Build a per-row analysis: true_label, pred_label, proba, error_type (TP/FP/TN/FN)."""
    out = pd.DataFrame({
        "true_label": y_true,
        "pred_label": y_pred,
        "churn_probability": y_proba,
    })
    out["error_type"] = "TP"
    out.loc[(out["true_label"] == 0) & (out["pred_label"] == 1), "error_type"] = "FP"
    out.loc[(out["true_label"] == 1) & (out["pred_label"] == 0), "error_type"] = "FN"
    out.loc[(out["true_label"] == 0) & (out["pred_label"] == 0), "error_type"] = "TN"
    if segment_df is not None and len(segment_df) == len(out):
        for c in segment_df.columns:
            out[c] = segment_df[c].values
    return out


def summarize_error_types(analysis_df: pd.DataFrame) -> dict:
    """Return counts of TP, FP, TN, FN."""
    return analysis_df["error_type"].value_counts().to_dict()


def segment_error_analysis(analysis_df: pd.DataFrame, segment_col: str) -> pd.DataFrame:
    """Aggregate error_type counts by segment column."""
    return (
        analysis_df.groupby(segment_col)["error_type"]
        .value_counts()
        .unstack(fill_value=0)
    )


def save_error_analysis(
    analysis_df: pd.DataFrame,
    summary: dict,
    tenure_segment: pd.DataFrame,
    contract_segment: pd.DataFrame,
    base_path: str | Path,
) -> None:
    """Save error_analysis_detailed.csv, error_summary.json, error_by_tenure_group.csv, error_by_contract.csv."""
    base = Path(base_path).parent
    base.mkdir(parents=True, exist_ok=True)
    analysis_df.to_csv(Path(base_path), index=False)
    summary_path = base / "error_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    tenure_path = base / "error_by_tenure_group.csv"
    contract_path = base / "error_by_contract.csv"
    tenure_segment.to_csv(tenure_path)
    contract_segment.to_csv(contract_path)
