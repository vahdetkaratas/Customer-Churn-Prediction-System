"""
Model registry: Logistic Regression, Random Forest, Gradient Boosting.
Same config as IMPLEMENTATION_REFERENCE §6 and SYSTEM_DESIGN §6.
"""
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression


def get_model(name: str, random_state: int = 42):
    """Return a configured classifier by name."""
    if name == "logistic_regression":
        return LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            random_state=random_state,
        )
    if name == "random_forest":
        return RandomForestClassifier(
            n_estimators=200,
            max_depth=None,
            class_weight="balanced",
            random_state=random_state,
        )
    if name == "gradient_boosting":
        return GradientBoostingClassifier(random_state=random_state)
    raise ValueError(f"Unknown model: {name}")


MODEL_NAMES = ["logistic_regression", "random_forest", "gradient_boosting"]
