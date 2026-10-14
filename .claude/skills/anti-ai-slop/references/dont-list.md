# Frontend DO NOT list (anti-slop)

Derived from 10 landing pages built from one-line briefs (see ../research/v1-notes.md). Two further runs with skill-guided pages found the later-order defaults listed at the end (see ../research/v2-analysis.md and v3-analysis.md). The number in brackets is how many of the 10 pages showed the pattern. Within each group, rules are ordered by that frequency.
Each "instead:" is meant to push toward a choice that only makes sense for *this* product, not toward a different default.

## Layout and structure

1. **Do not wrap everything in one `div.wrap` with `max-width:1000–1080px; margin:0 auto`** and a stack of equal-width sections [10].
   Instead: give each section the width its content needs (a 60–75ch text measure, a full-bleed artifact, a wide table), give at least two sections different horizontal edges, and put the page in a `<main>`. One shared fluid gutter (4vw, `clamp(16px,4vw,48px)`) for every section is the same wrapper with a new number [v2 8].
2. **Do not use the skeleton nav → hero → card grid → "Ready to…?" band → one-line footer** [9].
   Instead: write the sections the visitor actually needs to decide (menu, portfolio, changelog, sample lesson) and order them by that visitor's questions.
3. **Do not use a two-button hero (solid primary + ghost "See features" / "See how it works")** [9; label in 8].
   Instead: use one primary action and default to no secondary. If one is earned, make it underlined body text on its own line that names the evidence it leads to (write it for this product; do not reuse labels from this list).
4. **Do not end on a tinted or gradient rounded CTA band (radius 18–32px, `padding:48px`)** [6].
   Instead: end on something concrete the visitor can act on: an address and hours, a code snippet, a calendar link, a real signup form.
5. **Do not center the hero with `max-width:560px; margin:0 auto` under a centered h1** [5].
   Instead: align the hero to the layout's own grid (left-aligned editorial, product-first, or split around a real screenshot).
6. **Do not use `grid-template-columns:1.1fr .9fr` for the split hero** [4].
   Instead: size the columns from the visual's real aspect ratio, or let the product artifact take most of the width.
7. **Do not add a 3-tier pricing block with a bordered "Most popular" middle card** unless pricing was in the brief [3].
   Instead: if a real price was given, state it inline in one specific sentence. If not, leave pricing out entirely (no `[PRICE NEEDED]` tiers).
8. **Do not add a 3-step "How it works" with CSS-counter circles (`width:34px;height:34px;border-radius:50%`)** [2].
   Instead: show the process as the product's own artifact (a timeline of a real order, a terminal session, a before/after).

## Copy

1. **Do not write the hero paragraph as a list of three** ("Plan, assign and ship"; "No config, no servers, no stress.") [9].
      Not a violation: real data (tasting notes, three actual plans, table rows). Test: if the line works as well with two or four items, the count is decoration. The rule covers the h1, h2s and CTA rows too, including staccato ("Push. Build. Float.", v2) and stacked negations ("no config, no servers, no stress").
   Instead: write one specific claim with a number, place or mechanism, for the visitor's level (not crypto jargon for consumers).
2. **Do not open the hero paragraph with "[Brand] is the/a…" or "[Brand] turns…"** [8].
   Instead: start from the reader's situation or the concrete outcome, and let the logo carry the name.
3. **Do not make "© 2026 Brand. All rights reserved." the whole footer** [9; 5 "All rights reserved"].
   Instead: put the footer facts that actually exist in it (contact, address, docs, status). A static year is fine as a no-JS fallback. Do not build a 4-column "Product · Contact · Legal" footer filled with placeholders [v2 8].
4. **Do not use "Get started" / "Start free" / "Try it free" / "Create free account" as CTA labels** [6 "Get started"; 7 "free"].
   Instead: name the actual action and object, written fresh for this product. Avoid the "[Verb] your first [noun]" formula [v2 5]; three v2 pages copied this list's old example labels word for word.
5. **Do not pun on the brand name** ("work flowing" / "Ready to flow?", "lifted to the clouds", "close the loop") [5].
   Instead: write the line a domain expert would say; use wordplay only if it also states a fact.
6. **Do not write "Everything you need…" headings** ("…nothing you don't", "…to get stronger") [5].
   Instead: write a heading that makes a claim a competitor could not copy word for word.
7. **Do not use "instant(ly)", "one click / one tap", "Smart X" or "Simple pricing" as filler** [5 / 5 / 4 / 3].
   Instead: give the measured fact ("rollback in ~3 s", "autofill in Chrome, Safari, Firefox") or the mechanism ("spaced repetition").
8. **Do not use the "X. Y." or "Every X. One Y. Zero Z." headline formula** [4].
   Instead: write one sentence only this product could say.
9. **Do not close with "Ready to…?"** [4] **or "No credit card required."** [4] **or "…today."** [3].
   Instead: state the real terms (trial length, what happens after it, cancel policy) in plain words.
10. **Sort missing facts by who supplies them.**
    - Never invent **third-party claims** (quotes, ratings, user counts, customer logos, press, audits) [v1 2–5]; cut the section.
    - Draft **owner facts** (prices, plans, product names, trial terms, hours, shipping) as plausible values in `<data class="todo">`, listed in LAUNCH TODO and named in the hand-off. Do not cut them: v3 cut pricing on 10/10, and a shop without prices cannot sell.
    - **Contact facts** are launch constants, never invented.
11. **Do not put honesty notes on the page** ("not connected", "nothing is sent", "pre-launch", "[… NEEDED]") [v2 38 placeholders; v3 7/10 pages]. One short caption on a demo artifact is the maximum. The hand-off message carries the rest.
12. Watch-list (seen 0/10 here, but still banned): "Supercharge", "Unlock", "Seamless", "Revolutionize", "Elevate", "Effortless", "Game-changer".

## Color

1. **Do not reuse the token set `--bg / --fg / --muted / --card / --line / --accent`** with a card one step off the background [10].
   Instead: derive tokens from a product-specific reference (paper stock, a terminal theme, a plant leaf, a bank statement) and name them for their role in this product.
2. **Do not ship half a dark theme**: an auto token swap under `prefers-color-scheme` [v1 8; v2 7], or `[data-theme]` selectors with no toggle [v2 5].
   Instead: ship one finished theme (set `<meta name="color-scheme">` and say why; a terminal can be dark-only), or two themes with a persistent toggle in which at least one element changes role, not just value. Check every text pair and button boundary in both (`slop_check.py --contrast`).
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

1. **Do not ship with no typeface decision** (system-ui only, or Georgia plus system-ui) [v1 10], **and do not pick by "anything but my first idea"** [v3: 6/10 landed on the same second idea, Barlow Semi Condensed].
   Instead: take the class and shortlist from `scripts/brief_seed.py`. Load with `font-display:swap`. Monospace appears only inside code, terminal or aligned-figure elements.
2. **Do not use the h1 formula `clamp(2.2rem,5–6vw,3.6–4rem); line-height:1.1; letter-spacing:-.03em`** [10 clamp; 5 negative tracking].
   Instead: set the scale from the typeface and the headline's length. A 3-word headline and a 12-word headline need different sizes.
3. **Do not use the body formula `16px/1.6` plus a muted `1.1–1.15rem` hero paragraph** [10].
   Instead: set line-height for the chosen font and measure, and give the lead paragraph full ink if it carries the main claim.
4. **Do not use a weight-800 logo** [9] **or weight-600 buttons** [9] by reflex.
   Instead: pick weights from the typeface's character (v2 copied v1's one good weight-400 serif h1 onto 6 pages, so do not treat that as the answer either).
5. **Do not center every section h2 at `font-size:2rem`** [5].
   Instead: align headings to the content they introduce, and vary scale when importance varies.

## Components

1. **Do not use `repeat(auto-fit,minmax(240px,1fr))` card grids** for features, products and steps alike [10].
   Instead: name the section's data shape first (sequence → timeline or log; comparison → table; one number → a single large figure; spatial → map or plan; dialogue → transcript; inventory → shelf with images) and choose the form from it. Ruled rows are one option, not the alternative to cards: no form may be used in more than two sections of one page [v2: ruled rows 10/10].
2. **Do not use the button padding `12px 24px` / `13px 26px` with radius `10px` or `999px`** [9 padding; 5 r10; 4 pill].
   Instead: take the button shape from the seed's edge language.
3. **Do not build cards as `background:var(--card); border:1px solid var(--line); border-radius:14px; padding:24px`** [9].
   Instead: drop the box when spacing alone groups the content, or give the card a product-specific form (a ticket, a bag label, a terminal pane).
4. **Do not pair a solid button with a ghost button** (`.btn.ghost{background:transparent;border:1px solid var(--line)}`) [9], **and do not put a "See…" text link beside the primary** [v2 4].
   Instead: default to one action. A ghost button is any secondary action with a border, a background, padding over 0.25em, or a place in the primary's flex row. A text link is underlined body text on its own line that names the evidence it leads to.
5. **Do not make the logo a split two-tone wordmark** (`Task<span>flow</span>`, `Vault<span>ix</span>`) [8].
   Instead: use a real mark or SVG wordmark, or a typographic treatment tied to the product. Do not default to a tracked-uppercase wordmark [v2 6].
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

1. **Do not ship a physical-product, delivery or portfolio page without photographs** [v1 10; v2 10; v3 10 had zero `<img>`].
   Instead: use real photos when supplied; otherwise use art-directed photo slots (`<figure class="photo-slot" data-todo="photo: 250 g bag, kraft, top-lit">`) with correct aspect ratios and alt text. The slot is designed space, not a grey box with "[PHOTO]".
2. **Do not use emoji as feature icons** (💪 ❤️ 🌙 🏆, 🔐 🕵️ ⚡ 🎲, 🔁 🎙️ 🔥) [5], **or emoji anywhere as decoration** [6].
   Instead: use one consistent SVG icon set with `aria-hidden="true"`, or no icons, since a good title does not need one.
3. **Do not use a giant emoji in a rounded square as the hero image** (☕, 🪴) [2].
   Instead: use a photo of the actual product, or an illustration made for it.
4. **Do not use gradient boxes or abstract objects as stand-ins for the product** (gradient "project photos", a barbell instead of the app screen, a ring diagram instead of the lesson screen) [v1 1; v3 2/2 apps showed no phone].
5. Do show the product itself in a specific state in the hero: the real UI, terminal session, phone screen, product photo or built work. Give it `role="img"` and an `aria-label`, or real semantic markup. A metaphor (pegboard, container yard, station signage) never replaces the product [v3 8/10 metaphors].

## Code quality and accessibility

1. **Do not skip landmarks:** no `<main>` [10], no skip link [10], hero wrapped in `<header>` [2].
   Instead: use `header > nav`, `main > section[aria-labelledby]` and `footer`, plus a skip link.
2. **Do not ship text below 4.5:1 contrast**, such as white on `#ff9e4d` (2.05), `#ff6b3d` (2.83), `#4f8cff` (3.22), `#ff4d6d` (3.21), or dark-mode `#e08653` (2.73) / `#e08a5e` (2.64) [7].
   Instead: check every text/background pair in both themes, and use dark text on light accents.
3. **Do not ship `href="#"`, invented domains, or a conversion that goes nowhere** [v1 6; v2 7; v3 9 toy CTAs, 0 real].
   Instead: the primary CTA is the category's real action and points to one launch constant (`<form action="SIGNUP_URL">` or `data-href="SIGNUP_URL"`), declared in `<!-- LAUNCH TODO -->`. On-page calculators and pickers are secondary proof, not the conversion. No visible "not connected" text; no fake "Thanks!" state.
4. **Do not use inline `style=""` patches** (`<h2 style="margin-top:0">`) [7].
   Instead: put the spacing rule in the stylesheet so the system stays consistent.
5. **Do not make the logo a `<div>`** [7].
   Instead: use `<a href="/" aria-label="Brand home">`.
6. **Do not leave out the `<meta name="description">`** [5] **or OG tags** [10].
   Instead: write a product-specific description, og:title and og:description. Use `og:image` only as an absolute https URL that exists; otherwise omit it and add it to LAUNCH TODO. Put the copyright year in as static text and let JS update it (`<span id="y">2026</span>`), so it is never blank.
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

## Later-order defaults (pages that followed this skill converged here)
Bans are written as **shapes**. Moving a value a few units does not clear a shape; the checker compares fingerprints and colour distance, not exact numbers.

### v2 "stationery editorial" [v2 counts]
1. Paper or stationery as the material; sage/grey-green paper ground; green-black dark theme; pencil-red accent turning salmon in dark mode [7/8/8/7].
2. A serif + IBM Plex/JetBrains Mono pair; Newsreader; an italic `<em>` in a weight-400 h1 [7/5/8].
3. Tracked-uppercase mono micro-labels everywhere; a tracked-uppercase wordmark [10/6].
4. A copy-left/artifact-right split hero; ruled rows in every section; an artifact chrome strip with "sample" on the right [10/10/8].
5. A 4-column "Product · Contact · Legal" footer full of `[… NEEDED]` [8; 38 placeholders].

### v3 "industrial caption" [v3 counts]
6. One condensed or semi-condensed sans for everything (Barlow Semi Condensed, Archivo at 62–80% width) [8].
7. An orange, amber or safety-yellow CTA with dark text on a grey or brown-black ground [9].
8. Artifact full-bleed first, h1 below as its caption; the CTA below the mobile fold [7; 7].
9. An industrial/signage material metaphor standing in for the product (pegboard, container yard, concrete, station sign, safe-deposit steel) [8].
10. The h1 narrates the demo state instead of saying what the product is [7].
11. Tokens renamed for the material but with the same seven slots (`--wall / --wall-deep / --enamel-white / --steel-label / --safety-outline / --on-safety / --tool-edge`) [10].
12. A timeline/sequence section, then a toy widget as the last section and the CTA target [7; 9].
13. A one-line footer; a nav of 1–3 phrase-labelled anchors; a single theme [10; 10; 10].
14. No prices, photos, proof or real conversion at all [10].
15. Checker values nudged past thresholds (34→37/38/41rem lede, `#ebebe8`→`#eeece9`, h1 tracking forced to 0) [4 admitted].

Instead of all of the above: use the seed's assignment, the category conventions, and the shape rules in SKILL.md. Do not choose "the opposite" of a listed value; opposites (weight 400 → 700, paper → steel) were how v3 converged.

## Defaults that are right (do not ban these)
- A terminal or code block for a developer tool; install steps; a Docs link.
- A phone screen with real UI for a mobile app; store links.
- Product photos, names and prices for a shop; plans with prices for a subscription.
- Photographs of built work for a studio or agency.
- A product UI screenshot in a specific state for SaaS.
- A clear "what it is" h1, a primary CTA above the fold, and a nav to Pricing/Docs/Log in.
- A centred hero, a single theme, or rounded corners, **when the seed assigns them or a visitor reason demands them**.

## Pre-ship self-check

Use the checklist in SKILL.md step 4, which includes the second-order swap test. Run `scripts/slop_check.py` first.
