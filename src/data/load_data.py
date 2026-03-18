"""Load raw Telco churn dataset."""
from pathlib import Path

import pandas as pd


def load_raw_data(path: str | Path) -> pd.DataFrame:
    """Load raw Telco Customer Churn CSV from path."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Raw data not found: {path}")
    return pd.read_csv(path)
