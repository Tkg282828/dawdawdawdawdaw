# Frontend DO NOT list (anti-slop)

Derived from 10 landing pages built from one-line briefs (see slop-notes.md). The number in brackets is how many of the 10 pages showed the pattern. Within each group, rules are ordered by that frequency.
Each "instead:" is meant to push toward a choice that only makes sense for *this* product, not toward a different default.

## Layout and structure

1. **Do not wrap everything in one `div.wrap` with `max-width:1000–1080px; margin:0 auto`** and a stack of equal-width sections [10].
   Instead: choose widths per section from the content (a 65ch text column, a full-bleed product shot, a wide table) and put the page in a `<main>`.
2. **Do not use the skeleton nav → hero → card grid → "Ready to…?" band → one-line footer** [9].
   Instead: write the sections the visitor actually needs to decide (menu, portfolio, changelog, sample lesson) and order them by that visitor's questions.
3. **Do not use a two-button hero (solid primary + ghost "See features" / "See how it works")** [9; label in 8].
   Instead: use one primary action, and make any secondary link specific ("Read the docs", "View this month's beans") or leave it out.
4. **Do not end on a tinted or gradient rounded CTA band (radius 18–32px, `padding:48px`)** [6].
   Instead: end on something concrete the visitor can act on: an address and hours, a code snippet, a calendar link, a real signup form.
5. **Do not center the hero with `max-width:560px; margin:0 auto` under a centered h1** [5].
   Instead: align the hero to the layout's own grid (left-aligned editorial, product-first, or split around a real screenshot).
6. **Do not use `grid-template-columns:1.1fr .9fr` for the split hero** [4].
   Instead: size the columns from the visual's real aspect ratio, or let the product artifact take most of the width.
7. **Do not add a 3-tier pricing block with a bordered "Most popular" middle card** unless pricing was in the brief [3].
   Instead: if price matters, state it inline in one specific sentence ("$17 a bag, ships Tuesdays"). If it does not, leave it out.
8. **Do not add a 3-step "How it works" with CSS-counter circles (`width:34px;height:34px;border-radius:50%`)** [2].
   Instead: show the process as the product's own artifact (a timeline of a real order, a terminal session, a before/after).

## Copy

1. **Do not write the hero paragraph as a list of three** ("Plan, assign and ship"; "No config, no servers, no stress.") [9].
   Instead: write one specific claim with a number, place or mechanism ("ships within 48 hours of roasting").
2. **Do not open the hero paragraph with "[Brand] is the/a…" or "[Brand] turns…"** [8].
   Instead: start from the reader's situation or the concrete outcome, and let the logo carry the name.
3. **Do not hardcode "© 2026 Brand. All rights reserved." as the whole footer** [9 hardcoded year; 5 "All rights reserved"].
   Instead: put useful information in the footer (contact, address, docs, status, legal links) and generate the year.
4. **Do not use "Get started" / "Start free" / "Try it free" / "Create free account" as CTA labels** [6 "Get started"; 7 "free"].
   Instead: name the actual action and object ("Deploy your first app", "Pick a roast", "Book a site visit").
5. **Do not pun on the brand name** ("work flowing" / "Ready to flow?", "lifted to the clouds", "close the loop") [5].
   Instead: write the line a domain expert would say; use wordplay only if it also states a fact.
6. **Do not write "Everything you need…" headings** ("…nothing you don't", "…to get stronger") [5].
   Instead: write a heading that makes a claim a competitor could not copy word for word.
7. **Do not use "instant(ly)", "one click / one tap", "Smart X" or "Simple pricing" as filler** [5 / 5 / 4 / 3].
   Instead: give the measured fact ("rollback in ~3 s", "autofill in Chrome, Safari, Firefox") or the mechanism ("spaced repetition").
8. **Do not use the "X. Y." or "Every X. One Y. Zero Z." headline formula** [4].
   Instead: write one sentence only this product could say (example from 02: "Coffee roasted this week, at your door this week.").
9. **Do not close with "Ready to…?"** [4] **or "No credit card required."** [4] **or "…today."** [3].
   Instead: state the real terms (trial length, what happens after it, cancel policy) in plain words.
10. **Do not invent stats or testimonials** ("2M+ Active users · 4.8 · 150M", "Over 20,000 happy homes", "Maya R.", "Join learners worldwide") [2 stats, 1 testimonials, 1 vague].
    Instead: use real, attributable proof. If there is none, show the product itself, or mark the slot clearly as `[TESTIMONIAL NEEDED]`.
11. **Do not ship placeholder data that looks real** ("Northwind Studio", "Invoice #1042", `you@example.com` as visible content) [5].
    Instead: use sample content written for this product's real customers, and use a field label instead of an example-email placeholder.
12. Watch-list (seen 0/10 here, but still banned): "Supercharge", "Unlock", "Seamless", "Revolutionize", "Elevate", "Effortless", "Game-changer".

## Color

1. **Do not reuse the token set `--bg / --fg / --muted / --card / --line / --accent`** with a card one step off the background [10].
   Instead: derive tokens from a product-specific reference (paper stock, a terminal theme, a plant leaf, a bank statement) and name them for their role in this product.
2. **Do not stop at dark mode as an auto token swap under `prefers-color-scheme`** [8], **and do not ship dark-only** [2].
   Instead: design both themes on purpose, check contrast in both, and add a toggle if the audience expects one.
3. **Do not use blue-gray muted text `#9aa4bd` / `#9aa3b5` / `#9aa6bd` / `#9aa5c4`** [6].
   Instead: tint the neutrals toward the brand hue (warm grays for coffee, green-grays for plants) and check 4.5:1.
4. **Do not use a two-stop `linear-gradient(135deg, var(--accent), var(--accent2))`** on buttons, text or bands, and do not define `--accent2` only for it [5].
   Instead: use one confident solid brand color. Use a gradient only if it represents something real (a heart-rate zone scale, a roast curve).
5. **Do not default to indigo/violet: `#4f46e5`, `#818cf8`, `#8b5cf6`, `#4f6bff → #8b5cf6`, `#4f8cff → #7c5cff`, `#5b4bff`** [4].
   Instead: pick a hue from the product's world and justify it in one sentence.
6. **Do not paste raw Tailwind palette hexes** (`#4f46e5`, `#8b5cf6`, `#0f766e`, `#2dd4bf`, `#4ade80`, `#22d3ee`) [4].
   Instead: tune your own values (hue, chroma, lightness) from the brand reference.
7. **Do not use a near-black navy page `#0b1020` / `#0b0f1a` with navy cards `#141b33` / `#131a30`** [4].
   Instead: if the product calls for dark, choose a dark specific to it (terminal black, espresso brown, night-sky blue with a reason).
8. **Do not pair a warm off-white (`#faf6f0`, `#f4f1ec`, `#fffaf3`) with a terracotta accent (`#b5562b` / `#b4532a`)** as the "tasteful" fallback [cream 5; terracotta 2].
   Instead: if you go warm, take the exact colors from a real material the brand uses (kraft bag, clay, brick).

## Typography

1. **Do not ship with no typeface decision** (system-ui only, or Georgia plus system-ui) [10 no web font; 8 system-ui stack].
   Instead: choose a typeface for the product (a monospace for a deploy tool, a humanist serif for an architect, a rounded sans for kids' learning) and load it with `font-display:swap`.
2. **Do not use the h1 formula `clamp(2.2rem,5–6vw,3.6–4rem); line-height:1.1; letter-spacing:-.03em`** [10 clamp; 5 negative tracking].
   Instead: set the scale from the typeface and the headline's length. A 3-word headline and a 12-word headline need different sizes.
3. **Do not use the body formula `16px/1.6` plus a muted `1.1–1.15rem` hero paragraph** [10].
   Instead: set line-height for the chosen font and measure, and give the lead paragraph full ink if it carries the main claim.
4. **Do not use a weight-800 logo** [9] **or weight-600 buttons** [9] by reflex.
   Instead: pick weights from the typeface's character. Studio Mara's weight-400, 5rem serif h1 is more memorable than any 800.
5. **Do not center every section h2 at `font-size:2rem`** [5].
   Instead: align headings to the content they introduce, and vary scale when importance varies.

## Components

1. **Do not use `repeat(auto-fit,minmax(240px,1fr))` card grids** for features, products and steps alike [10].
   Instead: pick the form for the content: a comparison table, a spec list, ruled rows (as in 06), a product shelf, a single annotated screenshot.
2. **Do not use the button padding `12px 24px` / `13px 26px` with radius `10px` or `999px`** [9 padding; 5 r10; 4 pill].
   Instead: derive the button shape from the brand (square and tracked for an architect, as in 06; key-cap style for a dev tool).
3. **Do not build cards as `background:var(--card); border:1px solid var(--line); border-radius:14px; padding:24px`** [9].
   Instead: drop the box when spacing alone groups the content, or give the card a product-specific form (a ticket, a bag label, a terminal pane).
4. **Do not write a `.btn.ghost{background:transparent;border:1px solid var(--line)}` secondary button** [9].
   Instead: make the secondary action a text link, or remove it.
5. **Do not make the logo a split two-tone wordmark** (`Task<span>flow</span>`, `Vault<span>ix</span>`) [8].
   Instead: use a real mark or SVG wordmark, or a typographic treatment tied to the product (06's tracked uppercase).
6. **Do not write feature cards as icon + h3 + one muted sentence, four of them** [8 shape; 7 exactly four].
   Instead: show fewer features, each with proof (a screenshot crop, a number, a code line).
7. **Do not make the nav a logo plus one "Get started" button** [6].
   Instead: link the pages a buyer of *this* product checks (Menu, Docs, Pricing, Work, Contact).
8. **Do not drop the same footer `text-align:center; color:var(--muted); font-size:.9rem` line** [9].
   Instead: build a footer with the information this business needs to show (address, hours, status page, license).
9. **Do not add an email form that only swaps in "Thanks! Check your inbox"** [3].
   Instead: wire it to a real endpoint, or label it clearly as a prototype.

## Motion and effects

1. **Do not ship interactive elements with no `transition` and no `:focus-visible` style** [10 / 10].
   Instead: add `transition: background-color .15s, color .15s` and a visible `:focus-visible` outline in the brand color.
2. **Do not leave links and buttons with no hover state** [5], **and do not use `filter:brightness(1.1)` / `opacity:.88` as the only hover** [5].
   Instead: design the hover from the brand (an underline offset, a fill sweep, a color shift between two named tokens).
3. **Do not use gradient-clipped text** (`background-clip:text; color:transparent`) **on an `<em>` in the h1 or on the logo** [5].
   Instead: emphasize with weight, italic from the real font, or a single solid accent, and only if the phrase is the claim.
4. **Do not add animation without `prefers-reduced-motion` handling** (typewriter, `scroll-behavior:smooth`) [10 missing].
   Instead: wrap motion in `@media (prefers-reduced-motion: no-preference)` and use motion only to demonstrate the product.
5. **Do not use colored glow shadows** (`0 30px 80px rgba(255,77,109,.2)`) [1].
   Instead: use one consistent elevation scale, or none.

## Imagery, icons, emoji

1. **Do not ship a page with no image, SVG or favicon** [10].
   Instead: use a real product screenshot, photo or custom SVG, plus a favicon and an OG image.
2. **Do not use emoji as feature icons** (💪 ❤️ 🌙 🏆, 🔐 🕵️ ⚡ 🎲, 🔁 🎙️ 🔥) [5], **or emoji anywhere as decoration** [6].
   Instead: use one consistent SVG icon set with `aria-hidden="true"`, or no icons, since a good title does not need one.
3. **Do not use a giant emoji in a rounded square as the hero image** (☕, 🪴) [2].
   Instead: use a photo of the actual product, or an illustration made for it.
4. **Do not use gradient boxes as stand-ins for photos** (`linear-gradient(135deg,#b4532a,#e3b896)`) [1].
   Instead: use real images with alt text, or a clearly marked `[PHOTO: Clay House exterior]` placeholder.
5. Do keep the one good default seen across pages: **a CSS-drawn product artifact in the hero** (kanban, invoice, terminal, phone ring) [6]. Make it the real UI, though, and not a generic mock.

## Code quality and accessibility

1. **Do not skip landmarks:** no `<main>` [10], no skip link [10], hero wrapped in `<header>` [2].
   Instead: use `header > nav`, `main > section[aria-labelledby]` and `footer`, plus a skip link.
2. **Do not ship text below 4.5:1 contrast**, such as white on `#ff9e4d` (2.05), `#ff6b3d` (2.83), `#4f8cff` (3.22), `#ff4d6d` (3.21), or dark-mode `#e08653` (2.73) / `#e08a5e` (2.64) [7].
   Instead: check every text/background pair in both themes, and use dark text on light accents.
3. **Do not ship `href="#"` or self-referencing CTAs** ("Create free account" → `#`, "Create your workspace" → `#start` inside `#start`) [6].
   Instead: link every CTA to a real destination, or use a `<button>` with a real handler.
4. **Do not use inline `style=""` patches** (`<h2 style="margin-top:0">`) [7].
   Instead: put the spacing rule in the stylesheet so the system stays consistent.
5. **Do not make the logo a `<div>`** [7].
   Instead: use `<a href="/" aria-label="Brand home">`.
6. **Do not leave out the `<meta name="description">`** [5] **or OG tags** [10].
   Instead: write a product-specific description and an og:title, og:image and og:description.
7. **Do not leave decorative emoji or icons exposed to screen readers** [5].
   Instead: add `aria-hidden="true"` to decoration, and add text labels to anything meaningful.
8. **Do not rely on `auto-fit` alone for responsive layout** (no media query) [4], **and do not hide nav links on mobile with no menu** [2].
   Instead: test at 360px; use `gap` in a flex container instead of `margin-left` between buttons, and provide a mobile menu.
9. **Do not skip heading levels** (h1 → h3 feature cards with no h2) [2].
   Instead: give each section a visible or visually-hidden h2.
10. **Do not reach for the default class vocabulary** `.wrap .hero .grid .card .btn .ghost .cta .logo .ic .final` [9–10].
    Instead: name classes for the domain (`.roast-card`, `.deploy-log`, `.project-row`); the names prompt you to think about the domain.
11. **Do not treat `*{box-sizing:border-box}` alone as a reset** [10].
    Instead: use a deliberate base layer (box-sizing, `img{max-width:100%;display:block}`, `:focus-visible`, a reduced-motion block, form font inheritance).

---

## Pre-ship self-check (each answer should be "yes")

1. If I swapped in another product's name and copy, would this layout and color scheme look wrong? (If not, it is a template.)
2. Does the hero show this product's real artifact (screenshot, sample, code, photo), and not an emoji or a gradient box?
3. Is every color value chosen for this brand, with no stock Tailwind hex, no indigo-to-violet gradient and no `#0b1020`-style navy?
4. Did I choose and load a typeface for this product, instead of shipping the system-ui stack?
5. Is the hero paragraph free of the "[Brand] is the…" opener and the list of three, and does it contain one concrete fact?
6. Is every stat, testimonial, name and company on the page real, or clearly marked as a placeholder?
7. Does every CTA say what happens next, and link to a real destination (no `href="#"`)?
8. Do all text/background pairs meet 4.5:1 in both light and dark themes?
9. Do all interactive elements have hover, `:focus-visible` and transition states, with motion gated by `prefers-reduced-motion`?
10. Does the page use `<main>` and a correct heading order (h1 → h2 → h3), with decorative icons hidden?
11. Does it work at 360px wide, with no orphaned buttons and no hidden nav without a menu?
12. Has every section (pricing tiers, "How it works", stats row, "Ready to…?" band) earned its place for this product, and not been added only because landing pages usually have one?
