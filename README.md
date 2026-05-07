# Customer Churn Prediction

[![CI](https://github.com/vahdetkaratas/Customer-Churn-Prediction-System/actions/workflows/ci.yml/badge.svg)](https://github.com/vahdetkaratas/Customer-Churn-Prediction-System/actions/workflows/ci.yml)

**Repository:** [Customer-Churn-Prediction-System](https://github.com/vahdetkaratas/Customer-Churn-Prediction-System)  
**Live:** interactive demo + API [churn-api.vahdetkaratas.com](https://churn-api.vahdetkaratas.com/) · JSON probe [/meta](https://churn-api.vahdetkaratas.com/meta) · OpenAPI [/docs](https://churn-api.vahdetkaratas.com/docs). Portfolio/labs framing (`layout-shell` folders) are optional static sites.

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
- **REST API** — browser demo at `GET /`, `POST /predict` (probability, `Yes`/`No`, risk bands), `GET /meta` for probes.
- **pytest** — API, preprocessing, CLI, config (skips when data/model missing).

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
| `layout-shell/`, `layout-shell-commercial/` | Optional static framing pages (generated locally; gitignored by default) |
| `notebooks/` | EDA → errors (01–04) |
| `data/raw/` | Place CSV locally (gitignored) |
| `config/config.yaml` | Paths, split, default threshold |
| `Dockerfile`, `docker-compose.yml` | Optional containerized FastAPI |

#
**Dataset:** [Telco Customer Churn (Kaggle)](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

## CI

Contributor notes (data gitignore, static deploy copies): **[CONTRIBUTING.md](CONTRIBUTING.md)**.

## License

[MIT](LICENSE)
