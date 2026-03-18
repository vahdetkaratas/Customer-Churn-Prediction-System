"""Inference service: load model, predict_single_customer, get_risk_band."""
import json
from pathlib import Path

import pandas as pd

from src.config_loader import load_config

_model = None
_threshold: float | None = None
_config = None


def _get_paths_and_default_threshold():
    global _config
    if _config is None:
        _config = load_config()
    p = _config["paths"]
    return (
        Path(p["model_output"]),
        Path(p["threshold_summary"]),
        float(_config["model"]["default_threshold"]),
    )


def load_model():
    """Load pipeline from joblib; load threshold from threshold_summary.json if present."""
    global _model, _threshold
    model_path, threshold_path, default_t = _get_paths_and_default_threshold()
    if _threshold is None:
        _threshold = default_t
    if _model is None:
        import joblib

        if not model_path.exists():
            raise FileNotFoundError(
                f"Model not found: {model_path}. Run training first."
            )
        _model = joblib.load(model_path)
    if threshold_path.exists():
        with open(threshold_path, encoding="utf-8") as f:
            _threshold = float(json.load(f).get("best_threshold", _threshold))
    return _model, _threshold


def get_risk_band(probability: float) -> str:
    """Map probability to risk_band: ≥0.75 high, 0.45–0.75 medium, <0.45 low."""
    if probability >= 0.75:
        return "high"
    if probability >= 0.45:
        return "medium"
    return "low"


def request_to_dataframe(payload: dict) -> pd.DataFrame:
    """Convert ChurnRequest-like dict to single-row DataFrame (raw columns for build_features)."""
    return pd.DataFrame([payload])


def predict_single_customer(payload: dict) -> tuple[float, str, str, float]:
    """
    Run inference: request -> DataFrame -> build_features -> pipeline.predict_proba.
    Returns (churn_probability, prediction, risk_band, threshold_used).
    """
    from src.features.build_features import build_features

    pipeline, threshold = load_model()
    df_raw = request_to_dataframe(payload)
    df_fe = build_features(df_raw)
    proba = pipeline.predict_proba(df_fe)[:, 1]
    p = float(proba[0])
    pred = "Yes" if p >= threshold else "No"
    band = get_risk_band(p)
    return round(p, 4), pred, band, threshold
