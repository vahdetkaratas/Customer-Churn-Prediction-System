# Public assets (Vercel CDN)

Files here are served at the **site root** on Vercel (e.g. `model_comparison.png` → `https://your-domain.com/model_comparison.png`).

| File | Update |
|------|--------|
| `model_comparison.png` | After training: `python scripts/generate_figures.py` from repo root, then copy `reports/figures/model_comparison.png` here. |

Local `uvicorn`: the same image is also available via `GET /model_comparison.png` in `app.py`.
