# Reports

| Directory | Contents | Produced by |
|-----------|----------|-------------|
| **`metrics/`** | `metrics.json`, `model_comparison.csv`, threshold/error CSVs and JSON | `python -m src.pipeline.training_pipeline` |
| **`figures/`** | PNG charts (same script). Files are **gitignored**; run the script locally or in CI if you need them in-repo. | `python scripts/generate_figures.py` |

**Tip:** Re-run the figures script after every training run so plots match the latest metrics.
