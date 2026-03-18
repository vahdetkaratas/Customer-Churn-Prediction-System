"""Tests for preprocessor and prepare_target with full feature set."""
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.data.preprocess import build_preprocessor, prepare_target, NUMERIC_FEATURES, CATEGORICAL_FEATURES
from src.features.build_features import build_features
from src.data.load_data import load_raw_data


@pytest.fixture
def sample_df():
    """Minimal DataFrame with all columns needed after build_features."""
    path = Path("data/raw/telco_customer_churn.csv")
    if not path.exists():
        pytest.skip("Raw data not found")
    df = load_raw_data(path).head(100)
    return build_features(df)


def test_build_preprocessor_fit_transform(sample_df):
    """Preprocessor fits and transforms; output has no NaN and correct shape."""
    X, y = prepare_target(sample_df)
    preprocessor = build_preprocessor()
    Xt = preprocessor.fit_transform(X)
    assert Xt.shape[0] == X.shape[0]
    assert not np.isnan(Xt).any()
    assert Xt.shape[1] >= len(NUMERIC_FEATURES)


def test_prepare_target_after_build_features(sample_df):
    """After build_features, prepare_target yields X with numeric and categorical columns."""
    X, y = prepare_target(sample_df)
    for col in NUMERIC_FEATURES:
        assert col in X.columns, f"Missing numeric: {col}"
    for col in CATEGORICAL_FEATURES:
        assert col in X.columns, f"Missing categorical: {col}"
    assert y.isin([0, 1]).all()
