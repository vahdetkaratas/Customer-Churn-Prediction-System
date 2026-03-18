"""
Build full pipeline (preprocessor + model) and fit.
"""
from sklearn.pipeline import Pipeline


def build_model_pipeline(preprocessor, model, model_name: str = "model") -> Pipeline:
    """Return a sklearn Pipeline: preprocessor + model."""
    return Pipeline(
        [
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )


def fit_pipeline(pipeline: Pipeline, X, y) -> Pipeline:
    """Fit pipeline on X, y. Returns the same pipeline (fitted)."""
    pipeline.fit(X, y)
    return pipeline
