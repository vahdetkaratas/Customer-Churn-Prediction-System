"""Config merge and defaults."""
import tempfile
from pathlib import Path

import yaml

from src.config_loader import DEFAULT_CONFIG, load_config


def test_load_config_defaults_without_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    cfg = load_config()
    assert cfg["random_state"] == 42
    assert cfg["paths"]["model_output"] == "artifacts/models/churn_model.joblib"
    assert cfg["paths"]["metrics_output"] == "reports/metrics/metrics.json"
    assert cfg["model"]["default_threshold"] == 0.55


def test_load_config_overrides_paths(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "config").mkdir()
    custom = {
        "paths": {"model_output": "custom/model.joblib"},
        "data": {"test_size": 0.25},
    }
    with open(tmp_path / "config" / "config.yaml", "w", encoding="utf-8") as f:
        yaml.dump(custom, f)
    cfg = load_config()
    assert cfg["paths"]["model_output"] == "custom/model.joblib"
    assert cfg["paths"]["raw_data"] == DEFAULT_CONFIG["paths"]["raw_data"]
    assert cfg["data"]["test_size"] == 0.25


def test_legacy_model_threshold_key(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "config").mkdir()
    with open(tmp_path / "config" / "config.yaml", "w", encoding="utf-8") as f:
        yaml.dump({"model": {"threshold": 0.42}}, f)
    cfg = load_config()
    assert cfg["model"]["default_threshold"] == 0.42
