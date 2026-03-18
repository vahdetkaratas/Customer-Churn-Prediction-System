"""
End-to-end training pipeline.
Run: python -m src.pipeline.training_pipeline
"""
import json
from pathlib import Path

import joblib

from sklearn.model_selection import train_test_split

from src.config_loader import load_config
from src.data.load_data import load_raw_data
from src.data.preprocess import build_preprocessor, prepare_target
from src.features.build_features import build_features
from src.models.compare_models import compare_models, save_comparison
from src.models.error_analysis import (
    build_prediction_analysis_df,
    save_error_analysis,
    segment_error_analysis,
    summarize_error_types,
)
from src.models.evaluate import evaluate_classifier
from src.models.thresholding import (
    evaluate_thresholds,
    save_threshold_results,
    select_best_threshold,
)


def main() -> None:
    cfg = load_config()
    random_state = int(cfg["random_state"])
    test_size = float(cfg["data"]["test_size"])
    target_column = str(cfg["data"]["target_column"])
    paths = cfg["paths"]

    raw_path = Path(paths["raw_data"])
    model_output = Path(paths["model_output"])
    metrics_output = Path(paths["metrics_output"])
    threshold_table_path = Path(paths["threshold_table"])
    threshold_summary_path = Path(paths["threshold_summary"])
    model_comparison_path = Path(paths["model_comparison"])
    error_analysis_path = Path(paths["error_analysis_detailed"])

    df = load_raw_data(raw_path)
    df_fe = build_features(df)
    X, y = prepare_target(df_fe, target_column=target_column)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )

    preprocessor = build_preprocessor(random_state=random_state)
    best_name, comparison_df, best_metrics, best_pipeline = compare_models(
        preprocessor, X_train, y_train, X_test, y_test, random_state=random_state
    )

    model_output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_pipeline, model_output)
    metrics_output.parent.mkdir(parents=True, exist_ok=True)
    with open(metrics_output, "w", encoding="utf-8") as f:
        json.dump(best_metrics, f, indent=2)
    save_comparison(comparison_df, model_comparison_path)

    _, y_proba = evaluate_classifier(best_pipeline, X_test, y_test)
    threshold_table = evaluate_thresholds(y_test.values, y_proba)
    best_threshold = select_best_threshold(threshold_table, metric="f1")
    save_threshold_results(
        threshold_table,
        best_threshold,
        threshold_table_path,
        threshold_summary_path,
    )

    y_pred = best_pipeline.predict(X_test)
    segment_df = (
        X_test[["tenure_group", "Contract"]].copy()
        if "tenure_group" in X_test.columns and "Contract" in X_test.columns
        else None
    )
    analysis_df = build_prediction_analysis_df(
        y_test.values, y_pred, y_proba, segment_df=segment_df
    )
    summary = summarize_error_types(analysis_df)
    tenure_segment = (
        segment_error_analysis(analysis_df, "tenure_group")
        if "tenure_group" in analysis_df.columns
        else __empty_segment()
    )
    contract_segment = (
        segment_error_analysis(analysis_df, "Contract")
        if "Contract" in analysis_df.columns
        else __empty_segment()
    )
    save_error_analysis(
        analysis_df,
        summary,
        tenure_segment,
        contract_segment,
        error_analysis_path,
    )

    print("Done. Best model:", best_name, "| ROC-AUC:", best_metrics.get("roc_auc"))
    print("Best threshold (F1):", best_threshold)
    print("Model:", model_output, "| Metrics: reports/metrics/")


def __empty_segment():
    import pandas as pd

    return pd.DataFrame()


if __name__ == "__main__":
    main()
