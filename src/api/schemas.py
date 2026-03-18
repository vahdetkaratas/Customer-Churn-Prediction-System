"""API request/response schemas (IMPLEMENTATION_REFERENCE §5)."""
from pydantic import BaseModel


class ChurnRequest(BaseModel):
    """POST /predict body — one customer."""

    gender: str = "Female"
    SeniorCitizen: int = 0
    Partner: str = "Yes"
    Dependents: str = "No"
    tenure: int = 12
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
    MonthlyCharges: float = 79.85
    TotalCharges: float = 965.4


class ChurnResponse(BaseModel):
    """Response: churn_probability, prediction, risk_band, threshold_used."""

    churn_probability: float
    prediction: str  # "Yes" / "No"
    risk_band: str   # "high" / "medium" / "low"
    threshold_used: float
