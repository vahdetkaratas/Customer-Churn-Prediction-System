"""FastAPI app: / demo UI, /health, /predict, /meta, /static."""
from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.config_loader import load_config

from .schemas import ChurnRequest, ChurnResponse
from .service import predict_single_customer

_STATIC = Path(__file__).resolve().parent / "static"
_INDEX_HTML = _STATIC / "index.html"

GITHUB_REPO_URL = "https://github.com/vahdetkaratas/Customer-Churn-Prediction-System"

_MODEL_LABELS = {
    "logistic_regression": "Logistic Regression",
    "random_forest": "Random Forest",
    "gradient_boosting": "Gradient Boosting",
}


def _test_metrics_block() -> dict | None:
    cfg = load_config()
    path = Path(cfg["paths"]["metrics_output"])
    if not path.is_file():
        return None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    key = str(raw.get("model", "")).strip().lower().replace(" ", "_")
    return {
        "model_name": _MODEL_LABELS.get(key, raw.get("model", "selected model")),
        "roc_auc": round(float(raw["roc_auc"]), 4),
        "f1": round(float(raw["f1"]), 4),
        "test_set": "Stratified 80/20 hold-out test set",
    }


app = FastAPI(title="Customer Churn Prediction API", version="0.1.0")

app.mount("/static", StaticFiles(directory=str(_STATIC)), name="static")


@app.get("/meta")
def api_meta():
    """JSON metadata + optional hold-out metrics for the demo UI."""
    out = {
        "message": "Customer Churn Prediction API",
        "docs": "/docs",
        "demo": "/",
        "name": "Customer Churn Prediction",
        "dataset": "IBM Telco Customer Churn (Kaggle)",
        "stack": ["Python", "scikit-learn", "pandas", "FastAPI"],
        "training": (
            "Feature engineering (tenure groups, active services, TotalCharges); "
            "LogReg / Random Forest / Gradient Boosting; best model by ROC-AUC; "
            "F1-optimal binary threshold; full pipeline saved as joblib."
        ),
        "github": GITHUB_REPO_URL,
        "notebooks_url": f"{GITHUB_REPO_URL}/tree/main/notebooks",
    }
    tm = _test_metrics_block()
    if tm:
        out["test_metrics"] = tm
    return out


@app.get("/model_comparison.png", include_in_schema=False)
def model_comparison_chart():
    png = _STATIC / "model_comparison.png"
    if png.is_file():
        return FileResponse(png, media_type="image/png")
    raise HTTPException(
        status_code=404,
        detail="Copy reports/figures/model_comparison.png to src/api/static/model_comparison.png",
    )


@app.get("/")
def root():
    """Serve neutral HTML demo (same origin as POST /predict)."""
    if not _INDEX_HTML.is_file():
        raise HTTPException(status_code=500, detail="Demo UI missing on server.")
    return FileResponse(_INDEX_HTML, media_type="text/html; charset=utf-8")


@app.get("/health")
def health():
    cfg = load_config()
    model_ok = Path(cfg["paths"]["model_output"]).is_file()
    return {"status": "ok", "model_configured": model_ok}


@app.post("/predict", response_model=ChurnResponse)
def predict(request: ChurnRequest):
    """Predict churn probability and risk band. Applies build_features then pipeline."""
    try:
        payload = request.model_dump()
        churn_probability, prediction, risk_band, threshold_used = predict_single_customer(payload)
        return ChurnResponse(
            churn_probability=churn_probability,
            prediction=prediction,
            risk_band=risk_band,
            threshold_used=threshold_used,
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
