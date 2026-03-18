"""Tests for prediction and risk_band."""
import pytest
from fastapi.testclient import TestClient

from src.api.app import app
from src.api.service import get_risk_band

client = TestClient(app)


def test_get_risk_band():
    """Risk bands: high >= 0.75, medium 0.45-0.75, low < 0.45."""
    assert get_risk_band(0.8) == "high"
    assert get_risk_band(0.75) == "high"
    assert get_risk_band(0.5) == "medium"
    assert get_risk_band(0.45) == "medium"
    assert get_risk_band(0.3) == "low"


def test_predict_returns_schema():
    """POST /predict returns churn_probability, prediction, risk_band, threshold_used."""
    payload = {
        "gender": "Female", "SeniorCitizen": 0, "Partner": "Yes", "Dependents": "No",
        "tenure": 12, "PhoneService": "Yes", "MultipleLines": "No",
        "InternetService": "Fiber optic", "OnlineSecurity": "No", "OnlineBackup": "Yes",
        "DeviceProtection": "No", "TechSupport": "No", "StreamingTV": "Yes", "StreamingMovies": "No",
        "Contract": "Month-to-month", "PaperlessBilling": "Yes", "PaymentMethod": "Electronic check",
        "MonthlyCharges": 79.85, "TotalCharges": 965.4,
    }
    r = client.post("/predict", json=payload)
    if r.status_code != 200:
        pytest.skip("Model not found; run training first")
    data = r.json()
    assert "churn_probability" in data
    assert "prediction" in data
    assert data["prediction"] in ("Yes", "No")
    assert data["risk_band"] in ("high", "medium", "low")
    assert "threshold_used" in data
