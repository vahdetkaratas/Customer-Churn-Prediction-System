# Contributing

## Local setup

1. Clone the repo and install: `pip install -r requirements.txt`
2. Download [Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) → `data/raw/telco_customer_churn.csv` (CSV is gitignored).

## If `data/raw/*.csv` was committed by mistake

```bash
git rm --cached data/raw/*.csv
git commit -m "Stop tracking Kaggle CSV"
```

The file stays on your machine; only git tracking is removed.

## Demo bundle (optional)

The **`GET /`** page is the **Vercel-style demo** (`src/api/static/index.html`, `/static/layout-shell.css`, `churn-demo.css`, `favicon.svg`). **`GET /meta`** fills hold-out metrics (reads `reports/metrics/metrics.json`) plus repo links.

For the comparison chart on that page, copy `reports/figures/model_comparison.png` → **`src/api/static/model_comparison.png`** on the server (often gitignored).

## Docker

With **Docker** and **Docker Compose** installed, after `artifacts/models/churn_model.joblib` exists:

```bash
docker compose up --build
```

Same API as `uvicorn src.api.app:app`; useful when you do not want a local venv.

## Tests

```bash
python -m pytest tests/ -q
```

CI runs the same on Python 3.10–3.12; tests skip when the CSV or trained model is missing.
