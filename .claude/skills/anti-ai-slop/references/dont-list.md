# Frontend DO NOT list (anti-slop)

Derived from 10 landing pages built from one-line briefs (see ../research/v1-notes.md). A second run with 10 skill-guided pages found the second-order defaults listed at the end (see ../research/v2-analysis.md). The number in brackets is how many of the 10 pages showed the pattern. Within each group, rules are ordered by that frequency.
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
10. **Do not invent claims about the business** (stats, quotes, customer names, prices, terms, address, audits: "2M+ Active users", "Over 20,000 happy homes", "Maya R.") [v1 2–5], **and do not stub them either** [v2: 38 `[… NEEDED]` on 8 pages; three sections made only of placeholders].
    Instead: if the brief lacks the fact, cut the section and list it in a `<!-- LAUNCH TODO -->` comment. Max 2 visible placeholders per page, none in the hero.
11. **Do not ship demo data that looks like a real third party** ("Northwind Studio", "Maya R.", a plausible `.app` domain) [v1 5; v2 1].
    Instead: demo data lives inside the product artifact, uses roles or objects ("Dev", a lot number), and is labelled once in the caption. Never more than one "sample" note per artifact.
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

1. **Do not ship with no typeface decision** (system-ui only, or Georgia plus system-ui) [10 no web font; 8 system-ui stack].
   Instead: list three candidate families from different classifications, cross out the first that came to mind, and choose one for this product. Load it with `font-display:swap`. Default to one family. A monospace face appears only inside code, terminal or aligned-figure elements, and only if the page has them.
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
   Instead: derive the button shape from the product's material (a key cap for a dev tool, a plate edge for a gym).
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

1. **Do not ship a page with no image, SVG or favicon** [10].
   Instead: use a real product screenshot, photo or custom SVG, plus a favicon and an OG image.
2. **Do not use emoji as feature icons** (💪 ❤️ 🌙 🏆, 🔐 🕵️ ⚡ 🎲, 🔁 🎙️ 🔥) [5], **or emoji anywhere as decoration** [6].
   Instead: use one consistent SVG icon set with `aria-hidden="true"`, or no icons, since a good title does not need one.
3. **Do not use a giant emoji in a rounded square as the hero image** (☕, 🪴) [2].
   Instead: use a photo of the actual product, or an illustration made for it.
4. **Do not use gradient boxes as stand-ins for photos** (`linear-gradient(135deg,#b4532a,#e3b896)`) [1].
   Instead: use real images with alt text, or a clearly marked `[PHOTO: Clay House exterior]` placeholder.
5. Do keep **a CSS/SVG product artifact in the hero** [v1 6; v2 10], but show it in a specific state (a refusal, a failure, a total). Give it `role="img"` and an `aria-label`, or real semantic markup. Do not wrap it in the stock chrome strip (label on the left, "sample" on the right) [v2 8], and do not make it interactive just for a "Try it" moment [v2 9 interactive or animated; 3 "Try it"]. Interactivity must be the product's own core action.

## Code quality and accessibility

1. **Do not skip landmarks:** no `<main>` [10], no skip link [10], hero wrapped in `<header>` [2].
   Instead: use `header > nav`, `main > section[aria-labelledby]` and `footer`, plus a skip link.
2. **Do not ship text below 4.5:1 contrast**, such as white on `#ff9e4d` (2.05), `#ff6b3d` (2.83), `#4f8cff` (3.22), `#ff4d6d` (3.21), or dark-mode `#e08653` (2.73) / `#e08a5e` (2.64) [7].
   Instead: check every text/background pair in both themes, and use dark text on light accents.
3. **Do not ship `href="#"`, self-referencing CTAs, or invented destinations** ("Create free account" → `#`; `hello@brand.example`, `.invalid`, a plausible `brand.app`, `tel:+10000000000`, `mailto:?subject=Privacy` as a legal page, a `data:` og:image) [v1 6; v2 7].
   Instead: link to an on-page section that does the thing (a working form, calculator or picker), or to a URL or email the user supplied. With neither, use a `<button>` that opens the on-page form, and list the missing URL in `<!-- LAUNCH TODO -->`. With no legal pages, show no legal links.
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

## Second-order defaults (pages that followed this skill converged here)
Measured on 10 skill-guided pages (v2). They are now as recognisable as the v1 template. Bracketed numbers count v2 pages.

1. **Stationery material** (pad, ledger, galley proof, vellum, index card, label, stamp) [7; 10 chose a printed or marked surface].
   Instead: take the material from where the visitor uses or receives the product. List three, cross out the first.
2. **Sage paper / green-black / green-grey ink** (`#e4e8e1`, `#16201a`, `#46564b`) [8/8/8].
   Instead: tint neutrals toward *this* brand's accent hue. If that hue is green, say why the product is green.
3. **Pencil-red accent that turns salmon in dark mode** (`#a3261c` → `#ff8f7e`) [7].
   Instead: derive the accent from the material, not from editing marks.
4. **Ink/paper token vocabulary** (`--ink`, `--ink-soft`, `--rule`, `--paper-deep`, `--pencil`) [9]. This is the v1 `--fg/--muted/--line/--card/--accent` set renamed one for one.
   Instead: name tokens for product roles. At most one "surface" token, used for one component type.
5. **Serif + IBM Plex Mono** [7; Plex Mono 8; Newsreader 5, with an identical font request].
   Instead: one family, chosen by the three-candidate procedure.
6. **Italic `<em>` in a weight-400 h1, `-.012em`, line-height ~1.03, lede at 34ch** [8/6/6/10/9].
   Instead: set the h1 from the headline's length and the face. Use emphasis only if the phrase is the claim.
7. **Tracked uppercase mono micro-labels everywhere; tracked uppercase wordmark** [10/6].
   Instead: one label style, at most two uses.
8. **Copy-left / artifact-right split hero at 5fr/7fr** [10 split; 3 exact 5/7].
   Instead: choose among three described compositions.
9. **Ruled rows in every section; tables that collapse to blocks** [10; 6 tables].
   Instead: pick the form from the data shape, with each form in at most two sections.
10. **Artifact chrome strip with "sample" on the right** [8].
    Instead: let the artifact's own header carry real content.
11. **Stacked skeuomorphism** (rotation, stamp, offset shadow, ruled gradient, clip-path) [up to 4 on one page].
    Instead: one physical cue at most.
12. **Count-led h2s, "What happens after…", "Where X stops"** [7/4/3].
    Instead: headings that state the section's finding.
13. **Mailto for everything; `.example` domains; mailto legal links; data-URI og:image** [7/7/4/7].
    Instead: see Code 3 and the LAUNCH TODO comment.
14. **Disclaimer clutter** ("sample", "prototype", "illustrative", "not X advice") [10].
    Instead: one caption on the artifact.
15. **Pages 2.7× longer than v1** [v2 average]. Rules to add proof made agents add sections.
    Instead: cut any section that answers no question the visitor has.
16. **Copied skill examples** ("Deploy your first app", "Pick a roast", "Book a site visit", $17) [3].
    Instead: examples here are shapes, not text.

---

## Pre-ship self-check

Use the checklist in SKILL.md step 4, which includes the second-order swap test. Run `scripts/slop_check.py` first.
