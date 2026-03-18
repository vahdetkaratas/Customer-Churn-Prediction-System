"""
Train and compare LogReg, RF, GB; select best by ROC-AUC; optionally save comparison table.
Each model uses a fresh clone of the preprocessor (fit per model — no shared mutable state).
"""
from pathlib import Path

import pandas as pd
from sklearn.base import clone

from .evaluate import evaluate_classifier
from .model_registry import MODEL_NAMES, get_model
from .train import build_model_pipeline, fit_pipeline


def compare_models(
    preprocessor,
    X_train,
    y_train,
    X_test,
    y_test,
    random_state: int = 42,
):
    """
    Train each model (preprocessor + classifier), evaluate on test set.
    Returns (best_model_name, comparison_df, best_metrics, best_fitted_pipeline).
    Best model is selected by ROC-AUC.
    """
    results = []
    best_name = None
    best_auc = -1.0
    best_metrics = None
    best_fitted_pipeline = None

    for name in MODEL_NAMES:
        model = get_model(name, random_state=random_state)
        prep = clone(preprocessor)
        pipeline = build_model_pipeline(prep, model, model_name=name)
        fit_pipeline(pipeline, X_train, y_train)
        metrics, _ = evaluate_classifier(pipeline, X_test, y_test)
        metrics["model"] = name
        results.append(metrics)
        if metrics["roc_auc"] > best_auc:
            best_auc = metrics["roc_auc"]
            best_name = name
            best_metrics = metrics
            best_fitted_pipeline = pipeline

    comparison_df = pd.DataFrame(results)
    comparison_df = comparison_df[["model", "roc_auc", "precision", "recall", "f1", "accuracy"]]
    return best_name, comparison_df, best_metrics or {}, best_fitted_pipeline


def save_comparison(comparison_df: pd.DataFrame, path: str | Path) -> None:
    """Save model comparison table to CSV."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    comparison_df.to_csv(path, index=False)
