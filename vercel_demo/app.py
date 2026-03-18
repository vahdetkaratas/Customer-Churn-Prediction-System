"""
Vercel demo: inference-only FastAPI + static UI.
Deploy: set Vercel Root Directory to this folder; add model/churn_model.joblib (+ optional threshold_summary.json).

Feature logic must stay aligned with main repo: src/features/build_features.py
"""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

_BASE = Path(__file__).resolve().parent

MODEL_PATH = Path("model/churn_model.joblib")
THRESHOLD_PATH = Path("model/threshold_summary.json")

# Public repo (UI footer + GET /meta)
GITHUB_REPO_URL = "https://github.com/vahdetkaratas/Customer-Churn-Prediction-System"

app = FastAPI(
    title="Customer Churn Prediction",
    description=(
        "Live inference for a scikit-learn pipeline trained on the IBM Telco Customer Churn dataset. "
        "Training: Logistic Regression, Random Forest, Gradient Boosting — best model by ROC-AUC; "
        "classification threshold tuned by F1 on the test set (see threshold_summary.json)."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

_pipeline = None
_threshold: float = 0.55


def _load_model():
    global _pipeline, _threshold
    if _pipeline is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                "model/churn_model.joblib missing. From the main repo run training, then copy: "
                "artifacts/models/churn_model.joblib → vercel_demo/model/churn_model.joblib"
            )
        _pipeline = joblib.load(MODEL_PATH)
        if THRESHOLD_PATH.exists():
            with open(THRESHOLD_PATH, encoding="utf-8") as f:
                _threshold = float(json.load(f).get("best_threshold", _threshold))
    return _pipeline, _threshold


def _build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Mirror main project src/features/build_features.py."""
    out = df.copy()
    if "TotalCharges" in out.columns:
        out["TotalCharges"] = pd.to_numeric(out["TotalCharges"], errors="coerce")
    service_cols = [
        "PhoneService", "MultipleLines", "OnlineSecurity", "OnlineBackup",
        "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",
    ]
    for c in service_cols:
        if c in out.columns:
            out[c] = out[c].fillna("").astype(str)
    out["num_active_services"] = (
        out[service_cols].apply(lambda x: (x.str.strip().str.lower() == "yes").astype(int)).sum(axis=1)
    )
    if "tenure" in out.columns:
        out["tenure_group"] = pd.cut(
            out["tenure"].astype(int),
            bins=[-1, 12, 24, 48, 72],
            labels=["0-12", "13-24", "25-48", "49-72"],
            include_lowest=True,
        ).astype(object)
    return out


def _risk_band(p: float) -> str:
    if p >= 0.75:
        return "high"
    if p >= 0.45:
        return "medium"
    return "low"


class ChurnRequest(BaseModel):
    gender: str = "Female"
    SeniorCitizen: int = Field(0, ge=0, le=1)
    Partner: str = "Yes"
    Dependents: str = "No"
    tenure: int = Field(12, ge=0, le=100)
    PhoneService: str = "Yes"
    MultipleLines: str = "No"
    InternetService: str = "Fiber optic"
    OnlineSecurity: str = "No"
    OnlineBackup: str = "Yes"
    DeviceProtection: str = "No"
    TechSupport: str = "No"
    StreamingTV: str = "Yes"
    StreamingMovies: str = "No"
    Contract: str = "Month-to-month"
    PaperlessBilling: str = "Yes"
    PaymentMethod: str = "Electronic check"
    MonthlyCharges: float = Field(79.85, ge=0)
    TotalCharges: float = Field(965.4, ge=0)


class ChurnResponse(BaseModel):
    churn_probability: float
    prediction: str
    risk_band: str
    threshold_used: float


@app.get("/meta")
def project_meta():
    """Static description for portfolio / recruiters."""
    return {
        "name": "Customer Churn Prediction (demo)",
        "dataset": "IBM Telco Customer Churn (Kaggle)",
        "stack": ["Python", "scikit-learn", "pandas", "FastAPI"],
        "training": (
            "Feature engineering (tenure groups, active services, TotalCharges); "
            "LogReg / Random Forest / Gradient Boosting; best model by ROC-AUC; "
            "F1-optimal binary threshold; full pipeline saved as joblib."
        ),
        "this_deploy": "Inference only — model file in model/churn_model.joblib",
        "github": GITHUB_REPO_URL or None,
        "notebooks_url": f"{GITHUB_REPO_URL}/tree/main/notebooks",
        "docs": "/docs",
    }


@app.get("/")
def root():
    ui = _BASE / "static" / "index.html"
    if ui.exists():
        return FileResponse(ui, media_type="text/html")
    return JSONResponse(
        {
            "message": "Customer Churn Prediction API",
            "ui": "Add static/index.html",
            "meta": "/meta",
            "docs": "/docs",
        }
    )


@app.get("/health")
def health():
    return {"status": "ok", "model_configured": MODEL_PATH.exists()}


@app.post("/predict", response_model=ChurnResponse)
def predict(req: ChurnRequest):
    try:
        pipeline, threshold = _load_model()
        df = pd.DataFrame([req.model_dump()])
        df = _build_features(df)
        proba = pipeline.predict_proba(df)[:, 1]
        p = round(float(proba[0]), 4)
        pred = "Yes" if p >= threshold else "No"
        return ChurnResponse(
            churn_probability=p,
            prediction=pred,
            risk_band=_risk_band(p),
            threshold_used=threshold,
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


_static_dir = _BASE / "static"
if _static_dir.is_dir():
    app.mount("/static", StaticFiles(directory=str(_static_dir)), name="static")
