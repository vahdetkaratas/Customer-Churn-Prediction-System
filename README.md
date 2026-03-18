# Customer Churn Prediction

[![CI](https://github.com/vahdetkaratas/Customer-Churn-Prediction-System/actions/workflows/ci.yml/badge.svg)](https://github.com/vahdetkaratas/Customer-Churn-Prediction-System/actions/workflows/ci.yml)

**Repository:** [Customer-Churn-Prediction-System](https://github.com/vahdetkaratas/Customer-Churn-Prediction-System)  
**Live demo:** [churn.vahdetkaratas.com](https://churn.vahdetkaratas.com/) (Vercel — `vercel_demo/`)

Production-style **tabular ML** pipeline: preprocessing, engineered features, LogReg / Random Forest / Gradient Boosting (best by ROC-AUC), F1-tuned threshold, error analysis, **FastAPI** + optional CLI. Stack: scikit-learn, pandas, FastAPI.

**Hold-out test (Telco, default config):** ROC-AUC ≈ **0.84** · deployed model **Gradient Boosting** (chosen by test ROC-AUC). Re-run training to refresh; numbers are in `reports/metrics/metrics.json`.

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
- **Vercel demo** — inference UI + chart; see [`vercel_demo/README.md`](vercel_demo/README.md).

## Docker (API for clone users)

Train once on the host (or copy `churn_model.joblib` + `reports/metrics/threshold_summary.json`), then:

```bash
docker compose up --build
```

Open **http://127.0.0.1:8000/docs**. Model and metrics are read from host bind mounts (`artifacts/models`, `reports/metrics`). No GPU; image is inference-only.

## Quick start

```bash
pip install -r requirements.txt
# Kaggle → Telco Customer Churn → save as data/raw/telco_customer_churn.csv
python -m src.pipeline.training_pipeline   # or: make train
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
| `Dockerfile`, `docker-compose.yml` | Optional containerized FastAPI |

## Documentation

| Doc | Content |
|-----|---------|
| [docs/OVERVIEW.md](docs/OVERVIEW.md) | Problem, scope |
| [docs/USAGE.md](docs/USAGE.md) | Install, train, API, CLI |
| [docs/SYSTEM_DESIGN.md](docs/SYSTEM_DESIGN.md) | Pipeline design |
| [docs/IMPLEMENTATION_REFERENCE.md](docs/IMPLEMENTATION_REFERENCE.md) | Schemas, config |

**Dataset:** [Telco Customer Churn (Kaggle)](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

## CI

Workflow [.github/workflows/ci.yml](.github/workflows/ci.yml) runs `pytest` on Python 3.10–3.12. Contributor notes (data gitignore, Vercel copies): **[CONTRIBUTING.md](CONTRIBUTING.md)**.

## License

[MIT](LICENSE)
