# AI prompt pack — theme-aligned portfolio demo pages

Use this document when asking an AI to build a **standalone demo landing** (static HTML, FastAPI-served HTML, or similar) that **visually matches** the main site **vahdetkaratas.com** (Arter-based Next.js theme). Goal: same **colors, typography, left “info bar” structure, and content-area card patterns** as the main layout.

**Reference implementation in this repo:** `vercel_demo/static/index.html` (churn demo) — left rail + main column; full shell (outer padding, 1440px card, right menu rail) follows the layout section below.

**Source of truth on the main site repo (for humans verifying the prompt):**

- Colors & shadows: `src/app/_styles/scss/_config.scss`
- App shell (widths, flex): `src/app/_styles/scss/_markup.scss` (`.art-app-container`, `.art-info-bar`, `.art-content`, `.art-menu-bar`)
- Info bar UI blocks: `src/app/_layouts/info-bar/Index.jsx` + `src/app/_styles/scss/_info-bar.scss`
- Cards / section chrome: `src/app/_styles/scss/_content.scss` (`.art-card`, `.art-section-title`, `.art-banner`)
- Root fonts: `src/app/layout.jsx` (Next `next/font/google`)

---

## Copy-paste: master prompt (English)

Paste the block below into your AI chat. Replace `[PROJECT_NAME]`, `[YOUR_CONTENT]`, and optional links.

```
You are implementing a self-contained portfolio demo page (single HTML file with embedded CSS, or HTML + CSS files) that MUST match an existing personal site theme.

### Visual identity — exact tokens (CSS)

Use these as CSS custom properties (or equivalent). Do not substitute a different palette (no default indigo/purple “AI” theme).

- Accent (buttons, links, list bullets, focus rings): `#FFC107`
- Accent hover (slightly darker): `#e0ac06`
- App outer padding background: `rgb(25, 25, 35)`  /* deep */
- Main content background: `rgb(30, 30, 40)`   /* content */
- Left sidebar base: `rgb(32, 32, 42)`           /* info-bar-1 */
- Left sidebar header / gradient panels:
  `linear-gradient(159deg, rgb(37, 37, 50) 0%, rgb(35, 35, 45) 100%)`  /* info-bar-2 */
- Card / elevated panels:
  `linear-gradient(159deg, rgb(45, 45, 58) 0%, rgb(43, 43, 53) 100%)`
- Inputs / nested dark panels: `rgb(25, 25, 35)`
- Primary text: `rgb(250, 250, 252)`
- Secondary text: `rgb(140, 140, 142)`
- Tertiary / muted: `rgb(100, 100, 102)`
- Hairline borders: `rgba(255, 255, 255, 0.08)`
- Shadow (cards, bars): `0 3px 8px 0 rgba(15, 15, 20, 0.2)`
- Shadow (small): `0 1px 4px 0 rgba(15, 15, 20, 0.1)`
- Optional semantic accents (use sparingly): success `#4CAF50`, warning `#FFC107`, danger `#f44336`
- Primary button label on yellow: dark text `#1a1a1a` for contrast

### Typography

- Body / UI: **Poppins** — weights 400, 600, 700 (Google Fonts)
- Code / numeric metrics: **Courier Prime** — 400, 700 (Google Fonts)
- Load via Google Fonts `display=swap`. Do not use Inter, Roboto, or system-default stacks as the primary brand.

### Layout — mirror the main site shell (MANDATORY for “sitting” like the theme)

The live theme is **not** “full-bleed content edge-to-edge”. It is three nested layers, then a **three-column row** (info | content | menu rail). Reproduce this structure so the demo visually **locks** to the same frame as vahdetkaratas.com.

#### Layer 0 — outer frame (`.art-app`)

- **Padding:** `15px` on all sides of the viewport (top/right/bottom/left).
- **Background:** `rgb(25, 25, 35)` (deep) — this is the “letterbox” around the site card.
- **Min-height:** `100vh` (or `min-height: 100%` on html/body chain).
- **Overflow:** hide horizontal overflow if needed (`overflow-x: hidden` on this layer or body).

#### Layer 1 — centered site card (`.art-app-wrapper`)

- **Max-width:** `1440px`.
- **Margin:** `0 auto` (centered horizontally).
- **Width:** `100%`.
- **Background:** `rgb(30, 30, 40)` (content) — the main “card” fill.
- **Box-shadow:** `0 3px 8px 0 rgba(15, 15, 20, 0.2)` (theme shadow-1).
- **Position:** `relative` (children may use absolute positioning relative to this).

#### Layer 2 — flex row (`.art-app-container`)

- **Display:** `flex`, `flex-wrap: nowrap`, `align-items: stretch`.
- **Min-height:** `calc(100vh - 30px)` — accounts for **15px + 15px** vertical padding on Layer 0 (theme convention).
- **Position:** `relative` — used for optional decorative pseudo-elements.

#### Column A — left info bar (`.art-info-bar`)

- **Width / min-width:** `290px` (fixed).
- **Background:** `rgb(32, 32, 42)` (info-bar-1) for the bar frame; header block inside may use the **info-bar-2 gradient** (159deg, 37,37,50 → 35,35,45) like the React layout.
- **Height:** match row: `min-height: calc(100vh - 30px)` or stretch with flex parent.
- **Box-shadow:** same as shadow-1 (or subtle separation from content).
- **Z-index:** keep above content if overlapping (theme uses high z-index on the bar).

#### Column B — main content (`.art-content`)

- **Flex:** `1 1 auto`, **`min-width: 0`** (critical so flex does not overflow).
- **Background:** `rgb(30, 30, 40)` (content) — same as wrapper, or inherit.
- **Overflow-y:** `auto` (scroll inside this column only).
- **Padding-right:** **`80px`** — non-negotiable for theme fidelity: reserves the strip where the **right menu bar** peeks in on the real site.
- **Inner padding:** e.g. `2rem 1.5rem` for the demo copy/forms (left/top/bottom); keep the **80px** right gutter clear for the rail.
- **Height / min-height:** match `calc(100vh - 30px)` with the row.

#### Column C — right menu rail (`.art-menu-bar`)

On the real site the menu panel is **230px** wide but **mostly off-canvas**: only **~80px** remains visible (`right: -150px` offset in `_markup.scss`). For a **static demo without slide animation**, still implement a **visible right strip** so the layout does not look “wrong”:

- **Width:** `80px` **visible** column (or full **230px** if you implement the full sliding panel with JS — optional).
- **Background:** `rgb(32, 32, 42)` (same as info-bar-1).
- **Box-shadow:** shadow-1 or left-edge highlight (theme uses a subtle vertical gradient line on the left edge of the menu bar — see `_enhancements.scss` `.art-menu-bar::before`).
- **Header zone:** top **70px** height strip with **info-bar-2** gradient (light variant) and a **hamburger** icon (three lines) centered or top-aligned — can be **decorative** linking to `https://vahdetkaratas.com/` if no local nav.
- **Bottom:** optional small “current page” label style (theme: `.art-current-page` — padded label, letter-spacing ~2px, muted panel).

#### Optional fidelity — content-to-menu fade

Theme enhancement (`_enhancements.scss`, min-width 921px): `.art-app-container::after` — a **24px** wide vertical gradient at **`right: 80px`**, top-to-bottom, fading from transparent into `rgba(25, 25, 35, 0.12)` to soften the transition from scroll content to the menu rail. Add this **only on desktop** if you want pixel-close parity.

#### DOM order (recommended)

`[Layer0]` → `[Layer1 wrapper]` → `[Layer2 container]` → `[Info 290px] [Main flex+scroll+pr-80] [Rail 80px]`

#### What NOT to do

- Do not set `body { background: content }` only and skip the **15px deep border** — the demo will look like a different product.
- Do not drop **`padding-right: 80px`** on the main column if you include the right rail — text must not run under the rail.
- Do not use a single full-width flex row without the **1440px** centered card unless the user explicitly asks for full-bleed.

### Left sidebar — required content blocks (match structure and tone)

Replicate this structure and wording unless the user provides replacements:

1. **Top block** (centered): circular avatar 90×90, name as link to main site, role line **“Data & Reporting Consultant”**, line **“Available for 1–2 projects / month”**, link **“← Main site”** → `https://vahdetkaratas.com/`
2. **Location** (left-aligned list): label **“Location:”** + **“Prague, Czech Republic”**
3. **Horizontal divider** (1px, hairline border color)
4. **“Tools & Focus Areas”** + bullet list:
   - Dashboards & reporting
   - Data cleaning & analysis
   - Reporting workflows
   - Data pipelines & ETL
   - ML training → serving patterns
5. **“How I can help”** + bullet list:
   - Client work: dashboards, reports, automation
   - Applied ML & Interactive apps (link “see main site” → `https://vahdetkaratas.com/`)
   - Data cleaning & trustworthy spreadsheets
6. **“Recent outcomes”** + bullet list (three outcome lines as on main site)
7. **Divider** + one short sentence explaining **this demo page** (project-specific)
8. **Footer of sidebar:** social icons **GitHub**, **LinkedIn**, **Facebook** (Font Awesome 6 brands), centered row, hover color = accent

**List styling:** small circular bullet in accent color (~5px) before each item; comfortable line-height ~1.5; section titles slightly stronger than body, not all-caps unless matching a small-label pattern.

**Icons:** use Font Awesome 6 (CDN ok) for social brands.

**Avatar image:** prefer `https://vahdetkaratas.com/img/face-1.jpg` with `onerror` fallback to initials “VK” in a styled circle.

### Main column — content patterns

- Page title: ~1.45rem, weight 700, primary text
- Subtitle / lead: secondary text, ~0.9rem
- **Cards:** use the card gradient, 1px hairline border, `border-radius: 4px` (theme cards are often subtle; avoid huge 12px unless user asks), padding ~1.5rem, bottom margin ~1.25rem, small shadow
- **Card section labels:** small uppercase or small-caps style with `letter-spacing`, **secondary text color** (like `.art-card` h2 pattern)
- **Links** in body: accent color, font-weight 600, underline on hover
- **Primary buttons:** background accent, text `#1a1a1a`, hover `#e0ac06`
- **Secondary buttons:** transparent, border hairline, secondary text; hover brightens border/text
- **Form inputs:** deep background, hairline border, focus border accent
- **Code snippets:** Courier Prime, slightly smaller than body

Include the project-specific sections the user lists below.

### Responsive

- ≤900px: stack layout — sidebar full width first, then main; keep social row full width at bottom of sidebar block
- ≤520px: single-column form grids

### Technical constraints

- No external CSS frameworks unless requested
- Keep all theme colors as variables at `:root` for easy edits
- Must remain readable (WCAG-ish contrast on yellow buttons with dark text)
- Do not invent fake client names; demo datasets should be labeled as public/synthetic if applicable

### User-supplied project body (insert below)

[YOUR_CONTENT: sections, copy, embeds, API docs links, forms, charts, etc.]

Project name: [PROJECT_NAME]
```

---

## Optional add-on: full sliding right menu (230px)

If you implement **JS + open state** (beyond the default 80px rail):

- Panel width **230px**, `background: rgb(32,32,42)`, `right: -150px` when “closed” (only 80px peek), `transform: translateX(-150px)` when open — see `_markup.scss` `.art-menu-bar`.
- Menu header **70px**, gradient info-bar-2 light variant, burger toggles class `art-active` on the bar and optionally dims content (theme uses `.art-content.art-active` + curtain).
- The **master prompt above** already expects at minimum the **80px rail**; full 230px slide is optional.

---

## Optional add-on: top background banner

Main pages use `.art-top-bg` height **400px**, full width of content column, image + overlay gradient:

`linear-gradient(180deg, rgba(30,30,40,.93) 0%, rgba(30,30,40,.96) 70%, rgba(30,30,40,.99) 80%, rgba(30,30,40,1) 100%)`

You may add a slim hero banner under the main column top for extra fidelity.

---

## Checklist before shipping

- [ ] Poppins + Courier Prime loaded
- [ ] Accent `#FFC107` on primary actions and key links
- [ ] **Layer 0:** 15px padding, background `rgb(25,25,35)`
- [ ] **Layer 1:** max-width 1440px centered card, content bg + shadow-1
- [ ] **Layer 2:** flex row, `min-height: calc(100vh - 30px)`
- [ ] Left column **290px** with full profile + lists + socials (info-bar-1 + header gradient)
- [ ] Main column **`flex:1; min-width:0; overflow-y:auto; padding-right:80px`**
- [ ] Right rail **~80px** (or full 230px slide) with menu-bar bg + 70px header strip + burger
- [ ] (Desktop) Optional `::after` fade at `right: 80px` per `_enhancements.scss`
- [ ] Cards use 159deg gradient `45,45,58` → `43,43,53`
- [ ] Mobile: stack order sidebar → main → rail (or hide/collapse rail sensibly)
- [ ] Avatar fallback works offline / if image blocked

---

## Changelog

- 2026-03-23: Initial pack from Arter `_config.scss`, `_markup.scss`, and `vercel_demo/static/index.html`.
- 2026-03-23: Expanded **mandatory layout shell** (15px deep frame, 1440px wrapper, `calc(100vh-30px)`, main `padding-right:80px`, 80px menu rail, optional `::after` fade); clarified right bar vs full 230px slide.
