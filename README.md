# Customer Churn Prediction

**Repository:** [Customer-Churn-Prediction-System](https://github.com/vahdetkaratas/Customer-Churn-Prediction-System)  
**Live demo:** [churn.vahdetkaratas.com](https://churn.vahdetkaratas.com/) (Vercel — `vercel_demo/`)

Production-style **tabular ML** pipeline: preprocessing, engineered features, LogReg / Random Forest / Gradient Boosting (best by ROC-AUC), F1-tuned threshold, error analysis, **FastAPI** + optional CLI. Stack: scikit-learn, pandas, FastAPI.

```
Raw CSV → features → train/test split → compare models → best → joblib
                                    ↓
                    reports/metrics/ + POST /predict
```

## Features

- One-command training → model artifact + metrics + threshold tables.
- Single **joblib** pipeline (no train/serve skew on encodings).
- **REST API** — probability, `Yes`/`No`, risk bands.
- **pytest** — API, preprocessing, CLI, config (skips when data/model missing).
- **Vercel demo** — inference UI + static chart; see [`vercel_demo/README.md`](vercel_demo/README.md).

## Quick start

```bash
pip install -r requirements.txt
# Kaggle → Telco Customer Churn → save as data/raw/telco_customer_churn.csv
python -m src.pipeline.training_pipeline   # Windows: same (or make train)
uvicorn src.api.app:app --reload
pytest
python scripts/generate_figures.py
```

## Layout

| Path | Purpose |
|------|---------|
| `src/` | Load, features, models, training, API, CLI |
| `artifacts/models/` | `churn_model.joblib` after training (not in git) |
| `reports/metrics/` | Training outputs (JSON/CSV) |
| `reports/figures/` | PNGs from `generate_figures.py` (not in git) |
| `vercel_demo/public/model_comparison.png` | Demo chart (Vercel `public/` → site root) |
| `notebooks/` | EDA → errors (01–04) |
| `data/raw/` | Place CSV locally (gitignored) |
| `config/config.yaml` | Paths, split, default threshold |

## Documentation

| Doc | Content |
|-----|---------|
| [docs/OVERVIEW.md](docs/OVERVIEW.md) | Problem, scope |
| [docs/USAGE.md](docs/USAGE.md) | Install, train, API, CLI |
| [docs/SYSTEM_DESIGN.md](docs/SYSTEM_DESIGN.md) | Pipeline design |
| [docs/IMPLEMENTATION_REFERENCE.md](docs/IMPLEMENTATION_REFERENCE.md) | Schemas, config |

**Dataset:** [Telco Customer Churn (Kaggle)](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

## CI

[GitHub Actions](.github/workflows/ci.yml) runs `pytest` on Python 3.10–3.12. Tests that need the CSV or trained model **skip** when files are absent.

## Before you push to GitHub

- **`data/raw/*.csv`** is gitignored. If you ever committed the Kaggle CSV, run:  
  `git rm --cached data/raw/*.csv`  
  then commit (the file stays on your disk).
- **Vercel demo:** copy `artifacts/models/churn_model.joblib` → `vercel_demo/model/` after training so the live site can predict (see `vercel_demo/README.md`).

## License

[MIT](LICENSE)
