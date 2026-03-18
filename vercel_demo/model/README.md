# Model files (Vercel)

| File | Source |
|------|--------|
| `churn_model.joblib` | After training, copy from `artifacts/models/churn_model.joblib`. **Commit this file** (or use Git LFS) so Vercel has the model; the copy under `artifacts/` stays gitignored. |
| `threshold_summary.json` | Optional — copy from `reports/metrics/threshold_summary.json` for the same F1-tuned threshold as training. |

Without `churn_model.joblib`, `/predict` returns **503**.
