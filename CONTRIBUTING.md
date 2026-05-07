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

Deployed inference serves an HTML demo at **`GET /`** (same origin as `POST /predict`). For automation only, **`GET /meta`** returns the small JSON descriptor (`message`, `docs`, `demo`).

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
