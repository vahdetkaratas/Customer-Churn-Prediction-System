# Static (FastAPI-served)

| File | Purpose |
|------|---------|
| `index.html` | Landing + predict form (`GET /`) — **Arter / vahdetkaratas.com** shell (`layout-shell.css` + `churn-demo.css`). Prompt pack: [`docs/PORTFOLIO_DEMO_THEME_PROMPT.md`](../../docs/PORTFOLIO_DEMO_THEME_PROMPT.md) |
| `layout-shell.css` | Layout shell (info bar, main, rail) |
| `churn-demo.css` | Churn cards, form, metrics |
| `favicon.svg` | Portfolio mark: `#1a1a1f` tile, `rx=6`, white **VK** paths (see brand section in theme prompt) |

Charts and other root URLs live in **`../public/`** (Vercel CDN + `GET /model_comparison.png` in `app.py` for local dev).
