"""Tests for data loading and feature engineering."""
import pytest
import pandas as pd
from pathlib import Path

from src.data.load_data import load_raw_data
from src.features.build_features import build_features
from src.data.preprocess import prepare_target


def test_load_raw_data_file_not_found():
    """load_raw_data raises FileNotFoundError for missing path."""
    with pytest.raises(FileNotFoundError, match="Raw data not found"):
        load_raw_data(Path("nonexistent.csv"))


def test_load_raw_data_returns_dataframe():
    """load_raw_data returns DataFrame with expected columns when file exists."""
    path = Path("data/raw/telco_customer_churn.csv")
    if not path.exists():
        pytest.skip("Raw data not found; run from project root")
    df = load_raw_data(path)
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "Churn" in df.columns
    assert "tenure" in df.columns
    assert "MonthlyCharges" in df.columns


def test_build_features_adds_columns():
    """build_features adds num_active_services, tenure_group; TotalCharges numeric."""
    raw = pd.DataFrame({
        "tenure": [5, 25, 60],
        "TotalCharges": ["100", "500.5", "2000"],
        "PhoneService": ["Yes", "No", "Yes"],
        "MultipleLines": ["No", "No", "Yes"],
        "OnlineSecurity": ["No", "Yes", "No"],
        "OnlineBackup": ["No", "No", "Yes"],
        "DeviceProtection": ["No", "No", "No"],
        "TechSupport": ["No", "Yes", "No"],
        "StreamingTV": ["No", "No", "Yes"],
        "StreamingMovies": ["No", "No", "Yes"],
    })
    out = build_features(raw)
    assert "num_active_services" in out.columns
    assert "tenure_group" in out.columns
    assert pd.api.types.is_numeric_dtype(out["TotalCharges"])
    assert out["num_active_services"].min() >= 0
    assert out["num_active_services"].max() <= 8


def test_prepare_target_drops_customerid_and_returns_xy():
    """prepare_target drops customerID, encodes Churn Yes->1 No->0, returns X and y."""
    df = pd.DataFrame({
        "customerID": ["a", "b"],
        "Churn": ["Yes", "No"],
        "tenure": [1, 2],
        "MonthlyCharges": [50.0, 60.0],
    })
    X, y = prepare_target(df)
    assert "customerID" not in X.columns
    assert "Churn" not in X.columns
    assert list(y) == [1, 0]
    assert len(X) == 2
    assert len(y) == 2


def test_prepare_target_invalid_churn_raises():
    """prepare_target raises if Churn has values other than Yes/No."""
    df = pd.DataFrame({
        "Churn": ["Yes", "Unknown"],
        "tenure": [1, 2],
    })
    with pytest.raises(ValueError, match="Target contains"):
        prepare_target(df)
