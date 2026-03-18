"""
Merge config/config.yaml with defaults. Used by training_pipeline and API service.
"""
from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG: dict[str, Any] = {
    "random_state": 42,
    "data": {
        "target_column": "Churn",
        "test_size": 0.2,
    },
    "model": {
        "default_threshold": 0.55,
    },
    "paths": {
        "raw_data": "data/raw/telco_customer_churn.csv",
        "model_output": "artifacts/models/churn_model.joblib",
        "metrics_output": "reports/metrics/metrics.json",
        "threshold_table": "reports/metrics/threshold_table.csv",
        "threshold_summary": "reports/metrics/threshold_summary.json",
        "model_comparison": "reports/metrics/model_comparison.csv",
        "error_analysis_detailed": "reports/metrics/error_analysis_detailed.csv",
    },
}


def _deep_merge(base: dict, update: dict) -> dict:
    for key, val in update.items():
        if val is None:
            continue
        if key in base and isinstance(base[key], dict) and isinstance(val, dict):
            _deep_merge(base[key], val)
        else:
            base[key] = val
    return base


def load_config(config_path: str | Path | None = None) -> dict[str, Any]:
    """
    Load merged configuration. Paths are string values suitable for Path(...).
    """
    cfg = copy.deepcopy(DEFAULT_CONFIG)
    path = Path(config_path or "config/config.yaml")
    if path.exists():
        with open(path, encoding="utf-8") as f:
            user = yaml.safe_load(f)
        if user:
            _deep_merge(cfg, user)
    # Legacy key: model.threshold -> default_threshold
    mt = cfg.get("model", {}).get("threshold")
    if mt is not None and cfg["model"].get("default_threshold") == DEFAULT_CONFIG["model"]["default_threshold"]:
        cfg["model"]["default_threshold"] = float(mt)
    return cfg
