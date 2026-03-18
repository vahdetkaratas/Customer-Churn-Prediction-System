# Usage

## Prerequisites

- Python 3.10+  
- [Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) → save as `data/raw/telco_customer_churn.csv`  
- Run all commands from the **project root**

## Install

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
```

Dependencies: pandas, numpy, scikit-learn, matplotlib, fastapi, uvicorn, pydantic, pyyaml, joblib, pytest, httpx.

Clone: `git clone https://github.com/vahdetkaratas/Customer-Churn-Prediction-System.git`

Paths and default API threshold: `config/config.yaml`. After training, `reports/metrics/threshold_summary.json` overrides the classification threshold.

## Train

```bash
make train
# or: python -m src.pipeline.training_pipeline
```

Writes:

- `artifacts/models/churn_model.joblib` — fitted preprocessor + best classifier  
- `reports/metrics/metrics.json` — test metrics for the selected model  
- `reports/metrics/model_comparison.csv` — all three models  
- `reports/metrics/threshold_table.csv`, `threshold_summary.json`  
- `reports/metrics/error_*.csv`, `error_summary.json`

## API

```bash
make run-api
# uvicorn src.api.app:app --reload
```

Open `http://127.0.0.1:8000/docs`. `POST /predict` with JSON body matching `ChurnRequest` (see IMPLEMENTATION_REFERENCE).

## CLI

```bash
python -m src.cli.predict -i scripts/sample_customer.json --json
```

## Tests

```bash
make test
```

## Figures

```bash
python scripts/generate_figures.py
```

Requires raw data + trained metrics under `reports/metrics/`. Output: `reports/figures/*.png`.

## Vercel demo

**Monorepo:** set Vercel Root Directory to `vercel_demo`, copy `churn_model.joblib` (and optional `threshold_summary.json`) into `vercel_demo/model/` after training.  
**Separate repo:** copy the contents of `vercel_demo/` to a new repo and add the model file.  
Details: [`vercel_demo/README.md`](../vercel_demo/README.md).
