"""Tests for thresholding, evaluation, and model registry."""
import numpy as np
import pandas as pd
import pytest

from src.models.thresholding import evaluate_thresholds, select_best_threshold
from src.models.model_registry import get_model, MODEL_NAMES
from src.models.evaluate import evaluate_classifier
from sklearn.dummy import DummyClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def test_evaluate_thresholds_shape():
    """evaluate_thresholds returns one row per threshold, columns include threshold, f1, precision, recall."""
    y_true = np.array([0, 1, 0, 1, 1])
    y_proba = np.array([0.1, 0.9, 0.2, 0.8, 0.7])
    tbl = evaluate_thresholds(y_true, y_proba)
    assert len(tbl) == 17  # 0.1 to 0.9 step 0.05
    assert "threshold" in tbl.columns
    assert "f1" in tbl.columns
    assert "precision" in tbl.columns
    assert "recall" in tbl.columns


def test_select_best_threshold():
    """select_best_threshold returns threshold that maximizes given metric."""
    tbl = pd.DataFrame({
        "threshold": [0.3, 0.5, 0.7],
        "f1": [0.5, 0.8, 0.6],
    })
    best = select_best_threshold(tbl, metric="f1")
    assert best == 0.5


def test_get_model_returns_classifier():
    """get_model returns a classifier for each known name."""
    for name in MODEL_NAMES:
        model = get_model(name)
        assert hasattr(model, "fit")
        assert hasattr(model, "predict")


def test_get_model_unknown_raises():
    """get_model raises ValueError for unknown model name."""
    with pytest.raises(ValueError, match="Unknown model"):
        get_model("unknown_model")


def test_evaluate_classifier_returns_metrics_and_proba():
    """evaluate_classifier returns dict with roc_auc, precision, recall, f1, accuracy and y_proba array."""
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("model", DummyClassifier(strategy="stratified", random_state=42)),
    ])
    X = np.random.randn(50, 3)
    y = np.random.randint(0, 2, 50)
    pipe.fit(X, y)
    metrics, y_proba = evaluate_classifier(pipe, X, y)
    assert "roc_auc" in metrics
    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1" in metrics
    assert "accuracy" in metrics
    assert len(y_proba) == len(y)
    assert np.all((y_proba >= 0) & (y_proba <= 1))
