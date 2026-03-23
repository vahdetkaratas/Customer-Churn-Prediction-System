# Demo layout

The Vercel churn UI (`vercel_demo/static/index.html`) follows the repo’s **`layout-shell/`** reference:

- **CSS:** `vercel_demo/static/layout-shell.css` (copy of `layout-shell/styles.css`) + `vercel_demo/static/churn-demo.css` (cards, form, metrics).
- **Structure:** `.shell-outer` → `.shell-card` → info bar (`art-info-bar` + `#scrollbar2`) | `.shell-main-wrap` → main (`#main.shell-scroll`) + `.shell-rail` (portfolio home only).
- **Mobile:** Info drawer + curtain (see `layout-shell/README.md`).

Older “custom rail + burger” notes are obsolete for this demo.
