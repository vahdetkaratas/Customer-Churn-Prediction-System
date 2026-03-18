"""
Preprocessing: prepare_target (drop customerID, encode Churn), build_preprocessor (ColumnTransformer).
Feature engineering (build_features) must be applied to df before calling prepare_target.
"""
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Feature columns after build_features (excluding identifier and target)
NUMERIC_FEATURES = [
    "SeniorCitizen",
    "tenure",
    "MonthlyCharges",
    "TotalCharges",
    "num_active_services",
]
CATEGORICAL_FEATURES = [
    "gender",
    "Partner",
    "Dependents",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "tenure_group",
]


def prepare_target(
    df: pd.DataFrame,
    target_column: str = "Churn",
    drop_columns: list[str] | None = None,
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Drop identifier/target and return feature matrix X and target y.
    - Drops customerID (if present) and any columns in drop_columns.
    - Encodes target: Yes -> 1, No -> 0.
    """
    drop_columns = list(drop_columns or [])
    if "customerID" in df.columns and "customerID" not in drop_columns:
        drop_columns.append("customerID")

    X = df.drop(columns=[target_column] + [c for c in drop_columns if c in df.columns], errors="ignore")
    y = df[target_column].map({"Yes": 1, "No": 0})
    if y.isna().any():
        raise ValueError("Target contains values other than Yes/No")
    return X, y


def build_preprocessor(
    numeric_features: list[str] | None = None,
    categorical_features: list[str] | None = None,
    random_state: int = 42,
) -> ColumnTransformer:
    """
    Build ColumnTransformer: numeric -> median impute + StandardScaler;
    categorical -> most_frequent impute + OneHotEncoder(handle_unknown="ignore").
    """
    numeric_features = numeric_features or NUMERIC_FEATURES
    categorical_features = categorical_features or CATEGORICAL_FEATURES

    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    return ColumnTransformer(
        [
            ("num", num_pipeline, numeric_features),
            ("cat", cat_pipeline, categorical_features),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )
