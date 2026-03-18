"""
Feature engineering: num_active_services, tenure_group, TotalCharges (numeric).
Runs before train/test split and before sklearn preprocessor.
"""
import pandas as pd

SERVICE_COLUMNS = [
    "PhoneService",
    "MultipleLines",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
]

TENURE_BINS = [-1, 12, 24, 48, 72]
TENURE_LABELS = ["0-12", "13-24", "25-48", "49-72"]


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add engineered features to the dataframe.
    - TotalCharges: convert to numeric (coerce errors to NaN).
    - num_active_services: count of Yes in service columns (No/No phone service/No internet service → 0).
    - tenure_group: bins [-1, 12, 24, 48, 72] with labels 0-12, 13-24, 25-48, 49-72.
    """
    out = df.copy()

    # TotalCharges: ensure numeric
    if "TotalCharges" in out.columns:
        out["TotalCharges"] = pd.to_numeric(out["TotalCharges"], errors="coerce")

    # num_active_services: Yes=1, else 0
    for col in SERVICE_COLUMNS:
        if col in out.columns:
            out[col] = out[col].fillna("").astype(str)
    out["num_active_services"] = (
        out[SERVICE_COLUMNS].apply(lambda x: (x.str.strip().str.lower() == "yes").astype(int)).sum(axis=1)
    )

    # tenure_group
    if "tenure" in out.columns:
        out["tenure_group"] = pd.cut(
            out["tenure"].astype(int),
            bins=TENURE_BINS,
            labels=TENURE_LABELS,
            include_lowest=True,
        ).astype(object)  # object so OneHotEncoder treats as categorical

    return out
