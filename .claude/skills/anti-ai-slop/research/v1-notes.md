# Slop notes: 10 one-line-brief landing pages

Sample: 01 Taskflow (tasks), 02 Brewly (coffee), 03 Nimbus AI (writing), 04 FitPulse (fitness), 05 Ledgerly (invoicing), 06 Studio Mara (architecture), 07 Shipyard (deploys), 08 Greenleaf (plants), 09 Vaultix (passwords), 10 Lingo Loop (languages).
All 10 files were read in full. Counts are pages showing the pattern, out of 10. Contrast ratios were computed with the WCAG formula.

Headline finding: the sameness is **structural and in the CSS tokens**, not in the buzzwords. The classic "Supercharge / Unlock / Seamless / Revolutionize / Elevate" vocabulary appeared in **0/10** pages. The copy is clean but follows a template. The layout skeleton, class names, wrapper widths, radii, button padding and token names are close to identical across products as unrelated as an architecture firm and a password manager.

---

## 1. Page structure and section order

| Pattern | Count | Pages | Example |
|---|---|---|---|
| Single-column `.wrap` with `max-width:1000–1080px; margin:0 auto; padding:0 16–20px` | 10 | all | 1040px in 02,04,05,07,08,09; 1000px in 01,03,10; 1080px in 06 |
| Skeleton: nav → hero → card grid(s) → closing CTA → one-line footer | 9 | 01,02,03,04,05,07,08,09,10 | 06 swaps cards for a services list and an about section, but still ends on a "Let's talk" CTA |
| Closing CTA section just before the footer | 10 | all | "Ready to flow?" (01), "Ready to ship?" (07) |
| Closing CTA as a tinted or gradient rounded band (radius 18–32px) | 6 | 01,02,04,05,08,10 | `.cta{background:var(--card);border-radius:18px;padding:48px 16px}` (01) |
| Feature grid as the first section after the hero | 8 | 01,03,04,05,07,08*,09,10 | (*08 has steps first, then features) |
| Pricing block with a highlighted "pop" tier | 3 | 05,08,09 | `.price.pop{border:2px solid var(--green)}` + "Most popular" pill (05,08) |
| 3-step "How it works" with a CSS-counter number circle | 2 | 02,08 | identical CSS: `.steps .card::before{counter-increment:s;...width:34px;height:34px;border-radius:50%}` |
| Email capture form with a fake JS "Thanks! Check your inbox" message | 3 | 02,05,08 | `this.innerHTML='<strong>Thanks! Check your inbox.</strong>'` (05) |
| "Get N% off your first ..." signup band | 2 | 02,08 | "Get 10% off your first bag" / "Get 20% off your first box" |
| Wraps the whole page in one `div.wrap`, no `<main>` | 10 | all | `<body><div class="wrap">…` |

## 2. Hero layout

| Pattern | Count | Pages | Example |
|---|---|---|---|
| Two buttons, solid primary + ghost/outline secondary | 9 | all but 06 | "Start free" + "See features" (01) |
| Secondary CTA reads "See features" or "See how it works" | 8 | 01,03,04,05,07 (features); 08,09,10 (how it works) | `<a class="btn ghost" href="#features">See features</a>` |
| Centered hero: text-align:center, paragraph `max-width:540–560px; margin:0 auto` | 5 | 01,03,07,09,10 | `.hero p{max-width:560px;margin:0 auto 32px}` (07,09) |
| Split hero `grid-template-columns:1.1fr .9fr` (or 1.2fr 1fr) | 4 | 04,05,08 (1.1fr .9fr), 02 (1.2fr 1fr) | `.hero{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center}` |
| A CSS-drawn fake product UI in the hero (board, phone, invoice, terminal, vault list, demo box) | 6 | 01,03,04,05,07,09 | `.phone{width:240px;height:440px;border-radius:36px}` (04) |
| One big emoji in a rounded square standing in for hero art | 2 | 02 (☕), 08 (🪴) | `.art{aspect-ratio:1;border-radius:28px;...font-size:7rem}` |
| No real image or illustration anywhere on the page | 10 | all | 06 even uses gradient boxes as "project photos" |
| Hero vertical padding 50–96px top, 40–80px bottom | 10 | all | `padding:72px 0 56px` (01), `80px 0 60px` (07,09) |

## 3. Headline and copy phrasing

| Pattern | Count | Pages | Example |
|---|---|---|---|
| Hero paragraph contains a list of three | 9 | 01,02,03,04,05,06,07,09,10 | "Plan, assign and ship" (01); "drafts, edits and polishes" (03); "No config, no servers, no stress." (07) |
| Hero paragraph opens with the brand name ("X is the/a…", "X turns…") | 8 | 01,02,03,04,05,06,07,09 | "Taskflow is the simple task manager for small teams." / "Shipyard turns your git push into…" |
| Headline is a short sentence ending in a period | 8 | 01,02,03,05,06,08,09,10 | "Quiet buildings, made to last." |
| Footer says "© 2026 Brand." with a hardcoded year | 9 | all but 06 (06 sets the year with JS) | `&copy; 2026 Taskflow` |
| Pun on the brand name in the headline or CTA | 5 | 01,03,04,07,10 | "Get your team's work flowing." / "Ready to flow?"; "lifted to the clouds" (Nimbus); "Ready to close the loop?" |
| "Everything you need…" section heading | 5 | 01,03,04,05,08 | "Everything you need, nothing you don't" (01); "Everything you need to get stronger" (04); "Everything a plant parent needs" (08) |
| "instant / instantly" | 5 | 01,03,07,09,10 | "Instant editing", "Instant deploys", "alerted instantly" |
| "one click / one tap / single click / one-click" | 5 | 03,04,05,07,09 | "One-click rollbacks", "Sign in with one tap" |
| "Simple …" (simple pricing, simple insights, simple task manager) | 5 | 01,04,05,08,09 | "Simple pricing" as an h2 (05,09) and a feature card title (01) |
| "All rights reserved." | 5 | 03,04,07,09,10 | `&copy; 2026 Vaultix. All rights reserved.` |
| Two-beat headline "X. Y." / triplet headline | 4 | 02,04,05,09 | "Track every beat. Own your progress." / "Every password. One vault. Zero worries." |
| "Ready to …?" closing heading | 4 | 01,05,07,10 | "Ready to ship?", "Ready to simplify your finances?" |
| "No credit card required." | 4 | 03,04,05,07 | "Free for 14 days. No credit card required." |
| Feature titles starting with "Smart" | 4 | 03,08,09,10 | "Smart drafting", "Smart reminders", "Smart autofill", "Smart review loops" |
| "Get started" as a button label | 6 | 01,03,05,07,08,09 | nav button "Get started" / "Get started free" |
| CTA ending in "today" | 3 | 03,04,09 | "Lock down your digital life today." |
| ", so you can / so only you / so new words…" benefit clause | 3 | 03,09,10 | "…so you can ship great writing in minutes." |
| "…in seconds" | 2 | 03,07 | "Deploy your web app in seconds" |
| "without the bloat / guesswork" | 2 | 01,02 | "Fresh coffee without the guesswork." |
| Unsourced vanity stats | 2 | 04,08 | "2M+ Active users · 4.8 App store rating · 150M Workouts logged"; "Over 20,000 happy homes." |
| Vague social proof | 1 | 10 | "Join learners worldwide." |
| Testimonials signed "Firstname L." | 1 | 08 | "Maya R.", "Daniel K.", "Priya S." |
| Placeholder data | 5 | 02,05,06,08,09 | `you@example.com` (02,05,08); "Northwind Studio" + "Invoice #1042" (05); `bank.example`, `mail.example` (09); `hello@studiomara.example` (06) |
| Supercharge / Unlock / Seamless / Revolutionize / Elevate / Effortless | **0** | none | not observed |

## 4. Color

| Pattern | Count | Pages | Example |
|---|---|---|---|
| Same token vocabulary: `--bg`, `--muted`, `--card`, plus `--line` or `--border` | 10 | all | `:root{--bg:#fff;--fg:#14171f;--muted:#5b6475;--accent:#4f46e5;--card:#f5f6fa;--line:#e3e6ee}` (01) |
| Dark mode by swapping tokens in `@media (prefers-color-scheme:dark)`, no manual toggle | 8 | 01,02,03,05,06,08,10 (dark); 07 (light variant) | 04 and 09 are dark-only with no light theme |
| Desaturated blue-gray muted text `#9a a_ __` in dark mode | 6 | 01,03,04,05,07,09 | `#9aa4bd` (04 and 07 identical), `#9aa3b5` (01), `#9aa6bd` (03), `#9aa5c4` (09), `#9aaba5` (05) |
| Two-stop accent gradient (`--accent` → `--accent2`) on buttons, text or a CTA band | 5 | 03,04,07,09,10 | `linear-gradient(135deg,var(--accent),var(--accent2))` |
| A `--accent2` / `--brand2` token defined only to feed that gradient | 5 | 03,04,07,09,10 | `--accent:#4f8cff;--accent2:#7c5cff` (07) |
| Warm off-white page background | 5 | 02,05,06,08,10 | `#faf6f0` (02), `#f4f1ec` (06), `#fffaf3` (10), `#f7f5ee` (08), `#fbfaf7` (05) |
| Indigo or violet as primary color or gradient stop | 4 | 01,03,07,10 | `#4f46e5`/`#818cf8` (01); `#4f6bff → #8b5cf6` (03); `#4f8cff → #7c5cff` (07); `#ff6b3d → #5b4bff` (10) |
| Exact Tailwind palette hexes | 4 | 01,03,05,09 | indigo-600 `#4f46e5`, indigo-400 `#818cf8` (01); violet-500 `#8b5cf6` (03); teal-700 `#0f766e`, teal-400 `#2dd4bf`, teal-300 `#5eead4` (05); green-400 `#4ade80`, cyan-400 `#22d3ee` (09) |
| Near-black navy background | 4 | 04,07,09 (default), 03 (dark mode) | `#0b1020` in 07 and 09 (identical), `#0b0f1a` (04), `#0d1220` (03) |
| Navy card on navy page | 4 | 03,04,07,09 | `#141b33` (07), `#131a30` (09), `#141a2b` (04), `#151c30` (03) |
| Terracotta / burnt-orange accent on cream | 2 | 02,06 | `#b5562b` (02) vs `#b4532a` (06), nearly the same, on two unrelated products |
| Status green `#3ecf8e` | 1 | 07 | terminal check marks |

## 5. Typography

| Pattern | Count | Pages | Example |
|---|---|---|---|
| No web font loaded at all | 10 | all | |
| Body line-height 1.6 | 10 | all | `font:16px/1.6 system-ui,…` |
| h1 sized with `clamp(2–2.4rem, 5–7vw, 3.4–5rem)` | 10 | all | `clamp(2.2rem,6vw,4rem)` (07,09), `clamp(2.2rem,5vw,3.6rem)` (04,08) |
| h1 line-height 1.05–1.1 | 10 | all | 1.1 in 8 pages |
| Logo wordmark in weight 800 | 9 | all but 06 | `.logo{font-weight:800;font-size:1.3rem}` |
| `system-ui,-apple-system,Segoe UI,(Roboto,)sans-serif` body stack | 8 | 01,03,04,05,07,08,09,10 | |
| Hero paragraph 1.1–1.15rem in the muted color | 10 | all | `.hero p{color:var(--muted);font-size:1.15rem}` |
| Button text weight 600 (700 in 09,10) | 9 | all but 06 | |
| Negative tracking on h1 (`-.02em` / `-.03em`) | 5 | 02,05,07,08,09 | `letter-spacing:-.03em` |
| Centered section h2 | 5 | 01,03,04,05,09 | `h2{text-align:center;font-size:2rem}` |
| Georgia serif body with system-ui headings | 2 | 02,06 | the only "type personality" in the set, and it is still a system font |

## 6. Spacing, radius, shadow

| Pattern | Count | Pages | Example |
|---|---|---|---|
| Button padding 12–13px × 22–26px | 9 | all but 06 | `padding:12px 24px` (01,03,04,10); `12px 22px` (05,07); `13px 26px` (02,08,09) |
| Card = `var(--card)` background + `1px solid var(--line)` + radius 14–20px | 9 | all but 06 | `.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:24px}` |
| Flat cards with no shadow | 9 | all but 06 (which has no cards) | only 04 and 05 use any `box-shadow`, and only on the hero mock |
| Card padding 24px or 26px | 9 | 24px: 01,02,03,05,07,10; 26px: 04,08,09 | |
| Nav `padding:20px 0` (18–24px) | 10 | all | |
| Card radius 14px | 5 | 01,03,05,07,09 | (18px in 02,04,10; 20px in 08) |
| Button radius 10px | 5 | 01,03,05,07,09 | pill `999px` in 02,04,08,10; 06 is square |
| Generic `section{padding:56–64px 0}` rule | 5 | 02,04,05,06,08 | `section{padding:56px 0}` |
| Grid gap 16–24px | 10 | all | |

## 7. Cards and grids

| Pattern | Count | Pages | Example |
|---|---|---|---|
| `grid-template-columns:repeat(auto-fit,minmax(230–260px,1fr))` | 10 | all | minmax(240px) in 01,02,05,06,09,10 |
| Feature card = icon (optional) + h3 + one-sentence muted `<p>` | 8 | 01,03,04,05,07,08,09,10 | `<div class="card"><h3>Real-time sync</h3><p>Changes appear instantly for the whole team.</p></div>` |
| Exactly 4 feature cards (so a 3+1 or 2+2 wrap at common widths) | 7 | 01,03,04,05,07,08,09 | 10 has 3 |
| Emoji as the feature icon | 5 | 04,05,08,09,10 | 💪 ❤️ 🌙 🏆 (04); 🔐 🕵️ ⚡ 🎲 (09); 🔁 🎙️ 🔥 (10) |
| Emoji inside a tinted rounded square "icon tile" | 1 | 05 | `.ico{width:42px;height:42px;border-radius:10px;background:var(--soft)}` |
| Cards are bare `<div>`s, not a list or `<article>` | 10 | all | |

## 8. Buttons and CTAs

| Pattern | Count | Pages | Example |
|---|---|---|---|
| `.btn` plus `.ghost`/`.alt` modifier: transparent with `1–2px solid var(--line)` | 9 | all but 06 | `.btn.ghost{background:transparent;color:var(--fg);border:1px solid var(--line)}` |
| Nav = logo on the left and a single CTA button on the right, no links | 6 | 01,03,04,05,07,10 | `<nav><div class="logo">Task<span>flow</span></div><a class="btn" href="#start">Get started</a></nav>` |
| The word "free" in the primary CTA | 7 | 01,03,04,05,07,09,10 | "Start free", "Try it free", "Download free", "Create free account" |
| Gradient-filled primary button | 4 | 03,04,07,09 | |
| Dead or self-referencing primary CTA (`href="#"`, or `#start` linking to its own section) | 6 | 01,03,04,07,09,10 | `<a class="btn" href="#">Create free account</a>` (03,07); "Create your workspace" `href="#start"` inside `#start` (01) |
| Button text contrast below 4.5:1 (16px/600 text) | 7 | 03 (4.3/4.2), 04 (3.2 → 2.05), 07 (3.2), 10 (2.8); dark mode: 02 (2.7), 06 (2.6), 08 nav (2.2) | white on `#ff9e4d` = 2.05:1 (04); white on `#ff6b3d` = 2.83:1 (10) |

## 9. Footers

| Pattern | Count | Pages | Example |
|---|---|---|---|
| Footer has no links (no contact, legal or social) | 10 | all | |
| Footer is one centered muted line at ~.9rem | 9 | all but 06 | `footer{text-align:center;color:var(--muted);padding:24px 0 40px;font-size:.9rem}` |
| Brand sign-off in the footer | 3 | 02,05,08 | "Roasted with care, locally." / "Made for freelancers." / "Grown with care." |

## 10. Hover, animation, effects

| Pattern | Count | Pages | Example |
|---|---|---|---|
| No `transition` anywhere | 10 | all | hover states snap instantly |
| No `:focus-visible` / `:focus` styles | 10 | all | |
| No `prefers-reduced-motion` handling | 10 | all | matters for 03 (typewriter) and 06 (`scroll-behavior:smooth`) |
| No hover state at all | 5 | 01,03,04,07,10 | |
| Hover = brightness/opacity tweak or darker token | 5 | 02,05,06,08,09 | `.btn:hover{filter:brightness(1.1)}` (02); `opacity:.88` (06) |
| Gradient-clipped text (`background-clip:text; color:transparent`) on h1 `<em>` or logo | 5 | 03 (logo), 04,07,09,10 (h1 em) | `h1 em{background:linear-gradient(135deg,var(--accent),var(--accent2));-webkit-background-clip:text;color:transparent}` |
| Accent-colored `<em>` phrase in h1 (gradient or solid) | 5 | 04,07,08,09,10 | "Deploy your web app *in seconds*" |
| Colored glow shadow | 1 | 04 | `box-shadow:0 30px 80px rgba(255,77,109,.2)` |
| JS typewriter effect | 1 | 03 | `setTimeout(s,35)` |

## 11. Logo, icons, emoji

| Pattern | Count | Pages | Example |
|---|---|---|---|
| Split two-tone text wordmark: half of the name wrapped in an accent `<span>` | 8 | 01,02,03,04,05,07,09,10 | `Task<span>flow</span>`, `Vault<span>ix</span>`, `Ledger<span>ly</span>` |
| Decorative emoji somewhere on the page | 6 | 02,04,05,08,09,10 (+07 uses a ✔ glyph) | 🌿 in the 08 logo; ☕ as the 02 hero |
| No SVG icons, no `<img>`, no favicon | 10 | all | |
| Emoji not hidden from screen readers | 5 | 04,05,08,09,10 | `<div class="ic">&#128170;</div>` |

## 12. Accessibility and responsive gaps

| Pattern | Count | Pages | Example |
|---|---|---|---|
| No `<main>` landmark | 10 | all | |
| No skip link, no focus styles | 10 | all | |
| Logo is a `<div>`, not a home link | 7 | 01,02,03,04,05,09,10 | `<div class="logo">` |
| Button contrast below AA (see section 8) | 7 | 02*,03,04,06*,07,08*,10 | *dark mode only |
| Inline `style=""` patches | 7 | 01,03,04,05,06,08,09 | `<h2 style="margin-top:0">` |
| No `<meta name="description">` | 5 | 01,03,07,09,10 | |
| No media query at all (relies only on auto-fit) | 4 | 03,07,09,10 | buttons placed with `margin-left` wrap unevenly on phones (01,03,10) |
| `<header>` element used to wrap the hero instead of the site header | 2 | 04,05 | `<header class="hero">` |
| Heading level skip (h1 → h3, no h2 before the feature cards) | 2 | 07,10 | |
| Nav links hidden on mobile with no menu to replace them | 2 | 02,08 | `nav a:not(.keep){display:none}` |
| `aria-label` on a plain div (no role) | 1 | 05 | `<div class="invoice" aria-label="Example invoice">` |
| Typewriter output not announced (no aria-live) and runs regardless of motion preference | 1 | 03 | |

## 13. Code-level habits

| Pattern | Count | Pages | Example |
|---|---|---|---|
| One file, minified one-line CSS rules in a single `<style>` | 10 | all | |
| Class names `.wrap`, `.btn`, `.grid`, `.hero` | 10 | all | |
| `*{box-sizing:border-box}` as the whole reset | 10 | all | plus `margin:0` in 02,04,06,09 |
| `.card` | 9 | all but 06 (`.proj`) | |
| `.logo` | 9 | all but 02 (`.brand`) | |
| `.cta` | 9 | all but 06 | used both for a button row (04,05,07,08) and for a closing band (01,02,03,09,10) |
| `.ghost` / `.alt` button modifier | 9 | all but 06 | |
| Title format "Brand - tagline" with a hyphen | 8 | 01,02,03,04,05,07,08,09 | `<title>Shipyard - Deploy web apps fast</title>` |
| `.ic` / `.ico` icon class | 5 | 04,05,08,09,10 | |
| `.final` closing section | 3 | 04,05,07 | |
| `.tag` pill | 3 | 02,05,08 | |
| `!important` | 1 | 09 | `color:#04210f!important` |
| No Open Graph tags | 10 | all | |

---

## What was distinctive (where the page fit its product)

- **06 Studio Mara (most distinctive overall).** Editorial layout: square corners (no radius), an uppercase tracked logo and nav, a large weight-400 serif headline up to 5rem, services as hairline-ruled rows rather than cards, no emoji, no stats, a `mailto:` CTA, and honest, specific copy ("meant to be lived in for generations, not photographed once"). Weak spot: gradient boxes as fake project photos.
- **02 Brewly.** Georgia body text, a brown/cream palette that suits the product, real product cards with origin, tasting notes, roast tag and price ("Jasmine, bergamot and ripe peach"), and a concrete promise ("roasted this week, at your door this week", "ship within 48 hours"). Weak spots: an emoji as the hero image, and dark-mode button contrast.
- **03 Nimbus.** The hero shows the product working: a broken sentence struck through and a typed-out corrected version.
- **07 Shipyard.** A terminal snippet (`npm i -g shipyard`, `✔ Live at …`) in monospace shows the real workflow. This is the right idea for a developer audience.
- **05 Ledgerly.** A sample invoice with line items and a "Paid" tag, a teal palette that suits money, and plain, specific copy ("always know what you owe", "never have to chase a client again").
- **04 FitPulse.** A phone mock with a `conic-gradient` activity ring and real-looking metrics (7,214 of 10,000 steps, 68 bpm). The coral/orange palette has energy.
- **08 Greenleaf.** On-theme tier names (Sprout / Bloom / Jungle) and plant-specific detail ("fiddle leaf fig", "monstera", "plant doctors").
- **01 Taskflow.** A mini kanban board (To do / In progress / Done) with believable tasks.
- **09 Vaultix.** A masked password list in the hero, and concrete security claims (AES-256, zero-knowledge).
- **10 Lingo Loop.** Language chips, and a headline that explains the product idea (spaced repetition as a "loop").

Pattern: the distinctive part of every page is the **product-specific artifact** (the invoice, the terminal, the tasting notes, the tier names). The slop is everything around it, which is the same scaffold in every page.
