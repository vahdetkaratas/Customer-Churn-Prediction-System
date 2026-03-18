# Static assets for the demo UI

| File | Purpose |
|------|---------|
| `index.html` | Landing + predict form |
| `model_comparison.png` | Chart shown under **Key findings** — ROC-AUC / F1 for LogReg, RF, GB |

## Refresh the chart after retraining

From the **repository root** (not `vercel_demo`):

```bash
python scripts/generate_figures.py
copy reports\figures\model_comparison.png vercel_demo\static\   # Windows
# cp reports/figures/model_comparison.png vercel_demo/static/   # macOS/Linux
```

If the PNG is missing, the page shows copy instructions instead of the image.
