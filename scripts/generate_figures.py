"""
Generate report figures under reports/figures/ (architecture, metrics plots, etc.).
Run from project root: python scripts/generate_figures.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW_DATA = ROOT / "data" / "raw" / "telco_customer_churn.csv"
METRICS_DIR = ROOT / "reports" / "metrics"
OUT = ROOT / "reports" / "figures"
OUT.mkdir(parents=True, exist_ok=True)


def fig_system_architecture():
    """Pipeline diagram: Load -> Feature Eng -> Split -> Preprocess+Model -> Threshold/Error -> Save -> API."""
    fig, ax = plt.subplots(figsize=(8, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis("off")

    boxes = [
        (5, 12, "Raw CSV\n(Telco Churn)"),
        (5, 10.5, "Load Data"),
        (5, 9, "Feature Engineering\n(num_active_services, tenure_group, TotalCharges)"),
        (5, 7.5, "Train/Test Split\n(80/20, stratified)"),
        (5, 6, "Preprocessing + Model\n(LogReg, RF, GB → best)"),
        (5, 4.5, "Threshold + Error Analysis"),
        (5, 3, "Save Artifact\n(churn_model.joblib)"),
        (5, 1.5, "FastAPI Inference\n(/, /health, /predict)"),
    ]
    for i, (x, y, label) in enumerate(boxes):
        b = mpatches.FancyBboxPatch((x - 1.8, y - 0.35), 3.6, 0.7, boxstyle="round,pad=0.05",
                                     facecolor="steelblue", edgecolor="black", alpha=0.8)
        ax.add_patch(b)
        ax.text(x, y, label, ha="center", va="center", fontsize=8, wrap=True)
        if i < len(boxes) - 1:
            ax.annotate("", xy=(x, y - 0.5), xytext=(x, y - 0.35),
                        arrowprops=dict(arrowstyle="->", color="black"))

    ax.set_title("System Architecture — Customer Churn Prediction", fontsize=12)
    plt.tight_layout()
    plt.savefig(OUT / "system_architecture.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved system_architecture.png")


def fig_churn_distribution():
    """Bar chart: Churn Yes/No counts."""
    df = pd.read_csv(RAW_DATA)
    counts = df["Churn"].value_counts().reindex(["No", "Yes"])
    fig, ax = plt.subplots(figsize=(5, 4))
    counts.plot(kind="bar", ax=ax, color=["#2ecc71", "#e74c3c"], edgecolor="black")
    ax.set_xlabel("Churn")
    ax.set_ylabel("Count")
    ax.set_title("Churn Distribution")
    ax.set_xticklabels(["No", "Yes"], rotation=0)
    plt.tight_layout()
    plt.savefig(OUT / "churn_distribution.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved churn_distribution.png")


def fig_churn_by_contract():
    """Bar chart: Churn rate by Contract type."""
    df = pd.read_csv(RAW_DATA)
    ct = pd.crosstab(df["Contract"], df["Churn"])
    ct = ct.reindex(["Month-to-month", "One year", "Two year"])
    fig, ax = plt.subplots(figsize=(7, 4))
    ct.plot(kind="bar", ax=ax, color=["#2ecc71", "#e74c3c"], edgecolor="black")
    ax.set_xlabel("Contract")
    ax.set_ylabel("Count")
    ax.set_title("Churn by Contract")
    ax.legend(title="Churn")
    ax.tick_params(axis="x", rotation=15)
    plt.tight_layout()
    plt.savefig(OUT / "churn_by_contract.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved churn_by_contract.png")


def fig_model_comparison():
    """ROC-AUC and F1 by model from reports/metrics/model_comparison.csv."""
    path = METRICS_DIR / "model_comparison.csv"
    if not path.exists():
        print("model_comparison.csv not found, skipping model_comparison.png")
        return
    df = pd.read_csv(path).sort_values("roc_auc", ascending=False)
    labels = df["model"].str.replace("_", " ").str.title()
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
    colors = plt.cm.Blues(np.linspace(0.45, 0.85, len(df)))
    lo = max(0.5, float(df["roc_auc"].min()) - 0.05)
    axes[0].barh(labels, df["roc_auc"], color=colors, edgecolor="black")
    axes[0].set_xlabel("ROC-AUC")
    axes[0].set_title("Selection metric (best model)")
    axes[0].set_xlim(lo, 1.0)
    for i, v in enumerate(df["roc_auc"]):
        axes[0].text(v + 0.003, i, f"{v:.3f}", va="center", fontsize=9)
    axes[1].barh(labels, df["f1"], color="coral", edgecolor="black", alpha=0.9)
    axes[1].set_xlabel("F1")
    axes[1].set_title("F1 at sklearn default threshold (0.5)")
    axes[1].set_xlim(0, 1.0)
    for i, v in enumerate(df["f1"]):
        axes[1].text(v + 0.02, i, f"{v:.3f}", va="center", fontsize=9)
    plt.suptitle("Model comparison — test set", fontsize=11, y=1.02)
    plt.tight_layout()
    plt.savefig(OUT / "model_comparison.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved model_comparison.png")


def fig_threshold_analysis():
    """Precision, recall, F1 vs threshold."""
    tbl = pd.read_csv(METRICS_DIR / "threshold_table.csv")
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(tbl["threshold"], tbl["precision"], label="Precision", marker="o", markersize=3)
    ax.plot(tbl["threshold"], tbl["recall"], label="Recall", marker="s", markersize=3)
    ax.plot(tbl["threshold"], tbl["f1"], label="F1", marker="^", markersize=3)
    ax.set_xlabel("Threshold")
    ax.set_ylabel("Score")
    ax.set_title("Threshold Analysis (test set)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT / "threshold_analysis.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved threshold_analysis.png")


def fig_confusion_matrix():
    """2x2 confusion matrix from error_summary.json."""
    with open(METRICS_DIR / "error_summary.json", encoding="utf-8") as f:
        s = json.load(f)
    tn = int(s.get("TN", 0))
    fp = int(s.get("FP", 0))
    fn = int(s.get("FN", 0))
    tp = int(s.get("TP", 0))
    cm = np.array([[tn, fp], [fn, tp]])
    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["Pred No", "Pred Yes"])
    ax.set_yticklabels(["Actual No", "Actual Yes"])
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center", color="black", fontsize=14)
    plt.colorbar(im, ax=ax, label="Count")
    ax.set_title("Confusion Matrix (test set)")
    plt.tight_layout()
    plt.savefig(OUT / "confusion_matrix.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved confusion_matrix.png")


def fig_error_distribution():
    """Bar chart: TP, TN, FP, FN counts."""
    with open(METRICS_DIR / "error_summary.json", encoding="utf-8") as f:
        s = json.load(f)
    order = ["TN", "TP", "FP", "FN"]
    counts = [int(s.get(k, 0)) for k in order]
    colors = ["#2ecc71", "#3498db", "#f39c12", "#e74c3c"]
    fig, ax = plt.subplots(figsize=(5, 4))
    bars = ax.bar(order, counts, color=colors, edgecolor="black")
    ax.set_xlabel("Error type")
    ax.set_ylabel("Count")
    ax.set_title("Error Distribution (test set)")
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 5, str(int(b.get_height())),
                ha="center", va="bottom", fontsize=10)
    plt.tight_layout()
    plt.savefig(OUT / "error_distribution.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved error_distribution.png")


def fig_api_docs():
    """Simple API endpoints diagram (stand-in for /docs screenshot)."""
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")
    ax.set_title("API Endpoints — Churn Prediction", fontsize=12)
    endpoints = [
        (5, 3.5, "GET  /", "Root: message + link to /docs"),
        (5, 2.5, "GET  /health", "Health check"),
        (5, 1.5, "POST /predict", "ChurnRequest → ChurnResponse\n(churn_probability, prediction, risk_band)"),
    ]
    for x, y, title, desc in endpoints:
        b = mpatches.FancyBboxPatch((x - 2.5, y - 0.4), 5, 0.8, boxstyle="round,pad=0.05",
                                     facecolor="lightsteelblue", edgecolor="black")
        ax.add_patch(b)
        ax.text(x, y + 0.05, title, ha="center", va="center", fontsize=10, fontweight="bold")
        ax.text(x, y - 0.2, desc, ha="center", va="center", fontsize=7, style="italic")
    ax.text(5, 0.4, "Interactive docs: http://127.0.0.1:8000/docs", ha="center", fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT / "api_docs.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved api_docs.png")


def fig_feature_importance():
    """Feature importance (or coefficient magnitude for LR) from saved pipeline."""
    import joblib
    model_path = ROOT / "artifacts" / "models" / "churn_model.joblib"
    if not model_path.exists():
        print("Model not found, skipping feature_importance.png")
        return
    pipeline = joblib.load(model_path)
    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]
    names = np.asarray(preprocessor.get_feature_names_out())
    if hasattr(model, "feature_importances_"):
        imp = np.asarray(model.feature_importances_)
    elif hasattr(model, "coef_"):
        imp = np.abs(model.coef_[0])
    else:
        print("Model has no feature_importances_ or coef_, skipping feature_importance.png")
        return
    order = np.argsort(imp)[::-1][:20]
    names = names[order]
    imp = imp[order]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(range(len(imp)), imp, color="steelblue", edgecolor="black")
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("Importance (or |coefficient|)")
    ax.set_title("Feature Importance (top 20)")
    plt.tight_layout()
    plt.savefig(OUT / "feature_importance.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved feature_importance.png")


def main():
    if not RAW_DATA.exists():
        print("Raw data not found:", RAW_DATA)
        return
    fig_system_architecture()
    fig_churn_distribution()
    fig_churn_by_contract()
    if (METRICS_DIR / "model_comparison.csv").exists():
        fig_model_comparison()
    if (METRICS_DIR / "threshold_table.csv").exists():
        fig_threshold_analysis()
    if (METRICS_DIR / "error_summary.json").exists():
        fig_confusion_matrix()
        fig_error_distribution()
    fig_api_docs()
    fig_feature_importance()
    print("All figures written to", OUT)


if __name__ == "__main__":
    main()
