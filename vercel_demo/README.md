# Churn demo (Vercel)

**Inference-only** bundle: FastAPI + static UI. Train in the **parent** repo, copy the model (and optional assets), then deploy.

## Monorepo (recommended)

1. Push the whole project to GitHub.
2. Vercel → import repo → **Project name:** must be **all lowercase** (e.g. `customer-churn-demo` or `churn-demo`). If the GitHub repo name uses capitals, edit Vercel’s suggested name — otherwise you get a “must be lowercase” error.
3. **Root Directory:** `vercel_demo` (lowercase folder name).
4. Install: `pip install -r requirements.txt` (default). First deploy can take a few minutes; cold starts add latency — `vercel.json` sets **60s** `maxDuration` (Pro).

After each train, copy:

| From (repo root) | To |
|------------------|-----|
| `artifacts/models/churn_model.joblib` | `vercel_demo/model/churn_model.joblib` |
| `reports/metrics/threshold_summary.json` (optional) | `vercel_demo/model/threshold_summary.json` |
| `reports/figures/model_comparison.png` (after `generate_figures`) | `vercel_demo/static/` — see `static/README.md` |

Train: `python -m src.pipeline.training_pipeline` (or `make train`).

**`GITHUB_REPO_URL`** in `app.py` points at [Customer-Churn-Prediction-System](https://github.com/vahdetkaratas/Customer-Churn-Prediction-System); change it if you fork.

## Separate demo repo

Copy everything inside `vercel_demo/` to a new repo root, add `model/churn_model.joblib` (+ optional `threshold_summary.json`), push, import on Vercel (root = repo root).

## After deploy — check

| URL | Expected |
|-----|----------|
| `/` | UI + key findings |
| `/meta` | JSON (stack, training summary) |
| `/health` | `model_configured: true` if joblib present |
| `/docs` | Swagger |
| POST `/predict` | probability, label, risk band |

## Troubleshooting

| Issue | Fix |
|-------|-----|
| 503 model not found | Ensure `vercel_demo/model/churn_model.joblib` exists and is included in the deploy (commit or CI copy from `artifacts/` after train) |
| Slow first request | Cold start; retry; smaller model if needed |
| Bundle too large | Prefer LogReg or smaller ensemble (~500 MB Vercel limit) |
| Timeout on cold start | Pro + `maxDuration` in `vercel.json` |

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Demo + project story |
| GET | `/meta` | Portfolio JSON |
| GET | `/health` | Status + model file |
| GET | `/docs` | Swagger |
| POST | `/predict` | Same schema as main API |
