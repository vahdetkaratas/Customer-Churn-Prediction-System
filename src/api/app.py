"""FastAPI app: /, /health, /predict (IMPLEMENTATION_REFERENCE §5)."""
from fastapi import FastAPI, HTTPException

from .schemas import ChurnRequest, ChurnResponse
from .service import predict_single_customer

app = FastAPI(title="Customer Churn Prediction API", version="0.1.0")


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Customer Churn Prediction API", "docs": "/docs"}


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
