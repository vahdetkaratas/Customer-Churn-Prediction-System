# Scripts

| File | Purpose |
|------|---------|
| `generate_figures.py` | After **`python -m src.pipeline.training_pipeline`**, run `python scripts/generate_figures.py` from the repo root to refresh `reports/figures/*.png` (aligned with latest `reports/metrics/`). |
| `sample_customer.json` | Example payload for `python -m src.cli.predict --input scripts/sample_customer.json` or API tests. |

Requires: raw CSV in `data/raw/`, trained metrics under `reports/metrics/`, and `artifacts/models/churn_model.joblib` for feature-importance plot.
