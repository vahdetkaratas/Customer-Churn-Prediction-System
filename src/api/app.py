"""FastAPI app: /, /health, /predict (IMPLEMENTATION_REFERENCE §5)."""
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from .schemas import ChurnRequest, ChurnResponse
from .service import predict_single_customer

_STATIC = Path(__file__).resolve().parent / "static"
_DEMO_HTML = _STATIC / "demo.html"

app = FastAPI(title="Customer Churn Prediction API", version="0.1.0")


@app.get("/meta")
def api_meta():
    """Small JSON banner for probes (formerly served at GET /)."""
    return {"message": "Customer Churn Prediction API", "docs": "/docs", "demo": "/"}


@app.get("/")
def root():
    """Browser-facing churn scoring demo (same host as POST /predict)."""
    if not _DEMO_HTML.is_file():
        raise HTTPException(status_code=500, detail="Demo UI missing on server.")
    return FileResponse(_DEMO_HTML, media_type="text/html; charset=utf-8")


@app.get("/health")
def health():
    """Health check."""
    return {"status": "ok"}


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
