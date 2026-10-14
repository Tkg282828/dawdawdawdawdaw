# v2 analysis: second-order slop from the anti-ai-slop skill

Inputs: 10 v1 pages (no skill) in `research/pages/`, 10 v2 pages (with the skill) in `scratchpad/pages-v2/NN/index.html`, `v2-feedback.md` and `v2-check.txt`. I read all 10 v2 files in full. Counts below come from grep plus manual reading. "n/10" means the number of v2 pages that show the pattern.

Main finding: the skill removed the v1 template, and the v2 pages now share a new one. In short: **"stationery editorial"**. Most pages sit on a sage-grey paper background, or a green-black one in dark mode. The h1 is a weight-400 serif with an italic `<em>`. Small labels are tracked uppercase mono, usually IBM Plex Mono. Sections are ruled rows, and the accent is a red pencil. The hero is split, with copy on the left (5fr) and an artifact on the right (7fr). The artifact has a label strip that says "sample". Every CTA goes to an on-page anchor or a `mailto:`. The footer has 4 columns and is full of `[… NEEDED]`. This stack is as recognisable as the v1 one. A v2 page for a password manager and a v2 page for an architect could swap palettes, and you would barely notice.

---

## 1. What the skill fixed (v1 → v2)

Checker totals: **150 FAIL / 121 WARN → 4 FAIL / 5 WARN**. Of the 4 v2 FAILs, 2 are checker false positives (see §4) and 2 are "no img/svg" on pages that draw their artifact in CSS.

| v1 pattern | v1 | v2 |
|---|---|---|
| No web font (system-ui only) | 10 | 0 |
| No `<main>` / no skip link / no `:focus-visible` / no transition | 10/10/10/10 | 0/0/0/0 |
| Motion without `prefers-reduced-motion` | 10 missing | 0 missing |
| `auto-fit minmax(240px,1fr)` card grid | 10 | 0 |
| Generic `--bg/--muted/--card` tokens | 10 | 0 (but see the token renaming in §2) |
| `#9aa*` blue-gray muted | 7 | 0 real (1 false positive, a green-gray `#9aa59c`) |
| Split two-tone wordmark | 7 | 0 |
| Gradient-clipped text / 135deg accent gradient | 5 / 3 | 0 / 0 |
| Tailwind hexes / stock navy | 4 / 3 | 0 / 0 |
| Emoji as icons or hero | 6 | 0 |
| "Get started" / "See features" / "Ready to…?" / "All rights reserved" | 6 / 5 / 4 / 5 | 0 / 0 / 0 / 0 |
| `href="#"` dead links | 5 | 0 |
| Invented stats or testimonials | 2–3 | 0 |
| Hero shows a product-specific artifact | 6 (generic mocks) | 10 (all specific: refusal row, tracked edits, PAID invoice, 1:50 plan, failed health check, ciphertext pane) |
| SVG / favicon present | 0 | 10 favicons, 8 with inline SVG |
| Measured contrast failures (text) | 7 | 0 among the 23 risky pairs I computed. The one real failure is non-text (08 dark CTA, §4) |

Copy also improved. Every hero lead now states a mechanism with a number: "12 kg batches on Monday and Thursday", "27% by default", "1:20", "/healthz answers 200", "day 1, 3, 8 and 21", "64 MiB".

---

## 2. Second-order slop table

These patterns recur across products, so the skill created them. They did not come from the briefs.

### Typography

| Pattern | n/10 | Pages | Exact example |
|---|---|---|---|
| A monospace web font is loaded | **9** | all except 04 | `family=IBM+Plex+Mono:wght@400;500` (02,03,05,06,07,08,09,10). 01 uses `JetBrains+Mono` |
| …and the page shows no code or terminal | **7 of those 9** | 01,02,03,05,06,08,10 | Mono is justified as "like a ledger", "typed marginalia", "a date stamp on the card", "drawing-sheet lettering", "stamped data on the tag" |
| IBM Plex Mono specifically | **8** | 02,03,05,06,07,08,09,10 | |
| Serif display + mono pairing | **7** | 01,02,03,05,06,08,10 | Newsreader+JetBrains, Zilla Slab+Plex Mono, Newsreader+Plex Mono ×4, Spectral+Plex Mono |
| Newsreader | **5** | 01,03,06,08,10 | `Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400`, the same axis string on all 5 |
| `font-optical-sizing:auto` on body | 6 | 01,03,06,08,09,10 | |
| h1 at weight 400 (Studio Mara copied) | 6 | 01,03,05,06,08,10 | `.opening h1{font-weight:400;font-size:clamp(2.4rem,5.2vw,4.4rem);line-height:1.04;letter-spacing:-.012em}` (01) |
| h1 `letter-spacing:-.012em` (same value) | **6** | 01,02,03,06,08,10 | the new `-.03em` |
| h1 line-height ≤ 1.04 | **10** | all | 1.04 (01,03,05,09), 1.02 (06,08), .96 (02,10), .92 (04,07) |
| h1 still built with `clamp()`, max 4.4–5rem | 10 / 5 | 4.4rem: 01,03,05. 5rem: 06,08 | `clamp(2.4rem,1.3rem + 4.2vw,4.4rem)` (03) |
| Emphasized fragment inside h1 | **8** | `<em>` italic: 01,02,03,05,06,10. Colored `<span>`: 04,07 | "The sixth `<em>`waits`</em>`." in pencil red (01), "sets aside `<em>`its own tax.`</em>`" in red (05). This is the gradient `<em>` again with a different finish |
| Every h1 ends with a period | **10** | all | "Push. Build. Float." / "Drawn at 1:20 before a brick is ordered." |
| Tracked uppercase small labels (≥ .06em, ~.7–.85rem) | **10** | all; set in mono on 9 | `font:500 .72rem/1.3 var(--mono);text-transform:uppercase;letter-spacing:.14em` (02 footer h3) |
| Mono or uppercase-tracked nav links | 7 | 01,02,03,06,07,08 (mono), 09 (condensed uppercase) | `.masthead nav a{font:500 .8rem/1 var(--mono);letter-spacing:.06em;text-transform:uppercase}` (08) |
| Wordmark in tracked uppercase (Studio Mara copied) | **6** | 02 (.34em), 06 (.34em), 09 (.28em), 04 (.14em), 10 (.14em mono), 07 (.08em) | `.mark{font:700 1.15rem/1 var(--slab);letter-spacing:.34em;text-transform:uppercase}` (02), the same .34em as 06 |
| Otherwise an italic serif wordmark plus a small SVG | 3 | 03,05,08 | `font-style:italic;font-size:1.6–1.7rem;font-weight:500` |
| Lede `max-width` of 34 (ch/rem/em) | **9** | all except 10 (31rem) | `max-width:34ch` (01,05,06,07), `34rem` (02,04,09), `34em` (03,08) |
| Lede at 1.25–1.3125rem | 6 | 01,02,03,04,08,10 | |
| Body at 1.125rem / 1.5–1.55 | 6 (1.0625rem on 3) | | the new `16px/1.6` |

### Color and tokens

| Pattern | n/10 | Pages | Exact example |
|---|---|---|---|
| Light page bg in a narrow sage/green-grey "paper" band (hue ~70–150°, low chroma, L ~88–94%) | **8** | 01 `#eef1e4`, 03 `#ECECE6`, 04 `#E9EAE4`, 05 `#e9eee0`, 06 `#e6e9e0`, 07 `#e4e8e1`, 08 `#E6EADA`, 09 `#dde2db` | The new cream. Only 02 (kraft `#e2c9a0`) and 10 (`#f7f5ee`) leave this band |
| Dark page bg is green-black | **8** | 01 `#16201a`, 06 `#16201a` (**identical**), 05 `#121c17`, 08 `#141A15`, 09 `#141917`, 03 `#171B1A`, 04 `#151613`, 07 `#0c1412` | The new `#0b1020`. A task app, an AI editor, a gym app and a password manager all get the same dark green |
| Muted ink is a green-grey `#44–4f / 4c–5a` | **8** | 01 `#4d5946`, 03 `#4A524F`, 04 `#4F5448`, 05 `#46564b`, 06 `#454c43`, 07 `#44524d`, 08 `#46564A`, 09 `#445049` | "Tint neutrals toward the brand hue" turned into "tint toward green" whatever the brand |
| Dark oxblood / pencil red as an accent or mark | **7** | primary accent: 01 `#b3402a`, 05 `#9c2a24`, 06 `#a3261c`, 10 `#a82d1b`. Secondary (strike/stamp/warn): 03 `#A21F19`, 02 `#7a2e14`, 09 `#8a2f1f` | |
| …turning salmon in dark mode | **7** | 01 `#ff9c80`, 03 `#FF9E96`, 05 `#e68b81`, 06 `#ff8f7e`, 09 `#f0917c`, 10 `#ff9a85`, 07 `#ff9a8a` | |
| Brass / plate yellow as the other accent family | 4 | 02 `#f0d36b`, 04 `#F2C200`, 07 `#e2b93b`, 09 `#c79a2e` | |
| Stationery token vocabulary (`--ink`, `--ink-soft`, `--rule`, `--pencil*`, `--paper`, `--*-deep`, `--on-*`) | **9 use a `rule` token; 7 `ink`; 6 `pencil`; 7 `-soft`; 7 `-deep`/`-shade`** | `--pad-paper / --pad-paper-deep / --pad-ink / --pad-ink-soft / --pad-rule / --pencil-red / --pencil-red-ink` (01). `--vellum / --vellum-deep / --graphite / --graphite-soft / --pencil-red / --on-pencil / --sheet-rule` (06) | These are `--bg/--card/--fg/--muted/--line/--accent` renamed one for one. The structure (bg, one surface shade, ink, soft ink, rule, accent, on-accent) did not change |
| Material reference = paper/stationery | **7** | 01 engineer's pad, 02 kraft bag/sticker, 03 galley proof, 05 ledger book, 06 drafting vellum, 08 nursery label stake, 10 index cards | The other 3 are "stamped/stencilled metal" (04 plates, 07 hull stencil, 09 safe-deposit "stamped serials"). So 10/10 chose **a printed or marked surface** |
| "Desk lamp" dark theme narrative | 2 | 01 ("under a desk lamp, dark green board"), 03 ("under a desk lamp, graphite ground") | 3 more tell a material-variant story for dark mode (04 rubber, 06 cutting mat, 07 hull) |
| Theme toggle labelled "paper" | 2 | 01 `paper: auto`, 05 `Paper: light` | |

### Layout and skeleton

| Pattern | n/10 | Pages | Exact example |
|---|---|---|---|
| Split hero, copy left, artifact right | **10** | all | `grid-template-columns:minmax(0,5fr) minmax(0,7fr)` (01,03,09); `5fr/6fr` (05); `5fr/8fr` (07); `1fr / 29–30rem` (02,10); `1fr 340px` (04); `25rem 1fr` (06); `7fr/5fr` (08) |
| `minmax(0,5fr) minmax(0,7fr)` reused for non-hero sections | 4 | 02 `.after`, 04 `.logging-grid`, 08 `.band-head`, 09 `.sec-head` | the new `1.1fr .9fr` |
| One shared fluid gutter `4vw` | **8** | `clamp(16px,4vw,48px)` 01,08; `clamp(1rem,4vw,3rem)` 02,06,09; `max(16px,4vw)` 04,07,10 | the new `.wrap`. Sections do get different widths, but every section has the same edge |
| Hero class named `.opening` | 6 | 01,02,03,06,08,10 | (`.opener` 04, `.front` 05, `.bow` 07, `.door` 09). `.masthead` 5, `.colophon` 2, `.band` 2, `.kicker` 2 |
| Ruled rows (`border-top:1px solid var(--rule)`) as the main content form | **10** | `.rule-row` 01, `.roast-row` 02, `.refusals li` 03, `.steps li`/`.spec div` 04, `.ledger` 05, `.project-row`/`.scales` 06, `.phase` 07, `.plans li` 08, `.threats li` 09, `.schedule` 10 | Replaced cards everywhere. 04 said so in its feedback |
| A `<table>` used as a marketing section | 6 | 03,05,06,08,09,10 | 5 of them collapse to `display:block` on mobile (03,06,08,09,10), and 2 add `td::before{content:attr(data-label)}` (03,08) |
| `<dl>` spec list (term / value rows) | 9 | all except 03 | `.terms dl` 01, `.bag dl` 02, `.spec` 04, `.readout` 05, `.contact-lines` 06, `.tag dl` 08, `.field` 09, … |
| Numbered first column (`01`, `1 / build`, `Tap 1`) | 4 | 01,04,06,07 | `.rule-row .num{font-family:var(--mono);color:var(--pencil-red)}` "01" |
| Artifact has a chrome strip: label on the left, "sample"/meta on the right (`display:flex;justify-content:space-between`) | **8** | 01 "WEEK OF MON 12 OCT \| sample sheet", 02 "Brewly Roasters \| Lot 24-11", 03 "Product update, para. 1 of 4 \| 2 edits pending", 04 "Set 3 of 5 \| Sample session", 05 "Invoice \| INV-0007", 06 figcaption "Sheet A-101 / Plan \| 1:50 / Sample sheet", 07 "~/orders-api \| sample session", 10 "Portuguese · Deck 1 \| Card 14" | |
| A full-bleed inverted (dark) band mid-page or at the end | 6 | 01 `.close-out`, 02 `.visit`, 04 `.zones` + yellow `.beta`, 07 `.config`, 08 `.band-shelf`, 09 `.contact` | |
| Section order: hero+artifact → "how it works" ruled rows/table → spec/limits → terms/price → mailto contact band → 4-col footer | **7 follow most of it** | 01,03,04,05,07,09,10 | nav → hero → card grid → "Ready to…?" again, renamed |
| Closing "send us one X" contact band | 6 | 01 "Set up your first sheet", 03 "Send one paragraph you are stuck on.", 04 "Beta is open to lifters…", 06 "A site visit comes before a fee proposal.", 08 "Tell us which way your window faces", 09 "…Ask for a seat." | the "Ready to…?" band with specific copy |
| Footer: multi-column grid with tracked-uppercase small headings | **8** | 01,02,03,04,05,07,08,10 | `.colophon{grid-template-columns:repeat(4,minmax(0,1fr))}` (01,05). `repeat(auto-fit,minmax(11rem,1fr))` (04,07,10, **the same value**) |
| Footer column set "Product/Read · Contact · Legal" | 7 | 01,03,04,05,07,08,10 | "Legal" column on 5 |

### Components and effects

| Pattern | n/10 | Pages | Exact example |
|---|---|---|---|
| Square or 2px corners on everything | **10** | radius 2px: 03,04,05,07,08,10. 0: 06,09. None set: 01,02 | the opposite of the v1 pill, and just as automatic |
| Mono, uppercase, tracked CTA button | 7 | 02,03,05,06,08,10 (mono), 09 (condensed) | `.book{padding:1rem 1.6rem;font-family:"IBM Plex Mono";font-size:.8rem;letter-spacing:.14em;text-transform:uppercase}` (06) |
| CTA hover swaps to the red/accent fill | 5 | 01,05,06,10 (ink→pencil red), 03 (fill→outline) | `.start-link:hover{background:var(--pencil-red)}` |
| Hard offset "press" shadow plus translate on hover | 3 (+1 on an artifact) | 02 `5px 5px 0`, 04 `4px 4px 0`, 07 `4px 4px 0`. 05 invoice `6px 6px 0` | `.launch:hover{transform:translate(2px,2px);box-shadow:2px 2px 0 var(--plate-line)}` |
| Slightly rotated artifact | 3 | 02 `rotate(1.6deg)`, 05 `rotate(.4deg)`, 10 `rotate(1.2deg)` | |
| Rotated rubber stamp / sticker at −9deg | 2 | 02 sticker, 05 PAID stamp (+ "thud" keyframes) | |
| Ruled-paper `repeating-linear-gradient` lines | 3 | 01 sheet, 05 draft section and red margin on `<body>`, 10 index card | |
| `clip-path` skeuomorph (zigzag, stake, key tag) | 3 | 02, 08, 09 | |
| Hero artifact is interactive, animated or computed | **9** | inputs: 03 accept/reject, 08 date→window, 09 reveal, 10 typed cloze. Ticking/animated: 04 timer, 06 wall draw, 07 blinking cursor, 05 stamp thud. Computed: 02 roast date | "Try it: the buttons work." (03), "Try the tag" (08), "Try it, this one is live." (10) |
| Underline-grow hover via `background-size` | 3 | 04,07,09 | `background:linear-gradient(currentColor,currentColor) 0 100%/0 2px no-repeat` |
| `transition: … .15s` (the skill's own example value) | **10** | all | |
| Identical base layer (`button,input{font:inherit;color:inherit}`, `img,svg{max-width:100%;display:block}`, `-webkit-text-size-adjust:100%`, reduced-motion `*{transition:none!important;animation:none!important}`) | **10** | all | taken from the skill's own "deliberate base layer" sentence. Fine as hygiene, but nothing about it is a design decision |
| Skip link `top:-60px` → `top:12px` | 5 | 01,04,07,08,10 | |
| `:root:not([data-theme="light"])` selectors **with no toggle on the page** | **5** | 02,03,08,09,10 | dead CSS. 03 has `:root[data-theme="dark"]{color-scheme:dark}` with no tokens at all |
| Only an auto swap under `prefers-color-scheme` (the thing dont-list Color 2 bans) | 7 | all except the toggles on 01,05,06 | |

### Copy formulas

| Pattern | n/10 | Pages | Exact example |
|---|---|---|---|
| Hero lead = mechanism + number (often jargon) | **10** | all | "stretched with Argon2id, using 64 MiB of memory per guess" (09), "We resolve every wall, sill and stair at 1:20" (06), "immutable image… `/healthz` answers 200" (07). For lay visitors (09 and 06 consumers) the number is jargon, not proof |
| Lead ends with ", so [benefit]" | 4 | 02,06,09,10 | "…so the quote you sign describes the house you get." |
| h2 led by a count | **7** | 01 "Three rules…", 03 "Four passes, run one at a time.", 04 "Five zones…", 06 "Four scales, four decisions…", 07 "Four phases, always in this order.", 08 "Five plants that…", 10 "One word, four visits, one way back." | the new "Everything you need" |
| "What happens after / in / when…" | 4 | 02 link "See what happens after you order", 04 "What happens in the 90 seconds after the bar goes down", 07 "What happens after you push", 10 "What it costs and what happens after." | |
| "What it costs and what…" | 2 | 01 "What it costs and what you give up", 10 "What it costs and what happens after." | |
| A limits / "what it won't do" section | 3 (+3 one-line disclaimers) | 01 "Missing: No Gantt chart…", 03 "Where Nimbus stops.", 09 "What Vaultix stops, and what it does not". Disclaimers: 04 "Not a medical device", 05 "not tax advice", 09 "not audited results" | honesty as a trope |
| "X, not Y" construction | 5 | 03 h1 "marked up, not rewritten", 10 "Start with a language, not a level quiz.", 04 "a training guide, not medical advice", 05, 09 | |
| Secondary hero action is a text link starting "See…" | 4 (+1 primary) | 02,03,05,10. 09's *primary* is "See what we store" | "See how it works" made specific |
| Hero CTA "[Verb] your first [noun]" | 5 | 05 "Draft your first invoice", 07 "Deploy your first app →", 08 "Pick your first plant", 10 "Pick your first deck", 01 h2 "Set up your first sheet" | |
| **Skill examples copied verbatim** | 3 (+1 data) | 02 "Pick a roast", 06 "Book a site visit", 07 "Deploy your first app". 02 prices its lead coffee at **$17**, from the skill's "$17 a bag" | examples in a skill act as templates |
| Visible "sample / illustrative / prototype / placeholder" disclaimers | **10** | 17 text nodes across 10 pages | "A sample sheet with made-up tasks." (01), "Prototype: orders open a pre-filled email…" (02), "Specifications shown are the design targets… not audited results." (09) |
| Pre-launch framing (beta, early access, "until accounts are live") | 6 | 01,02,03,04,05,09 | the honesty rule makes every product look unlaunched |
| Banned rhetorical triplets that came back in headings or body | 4 | 07 h1 "**Push. Build. Float.**" (triplet + "X. Y. Z." + brand pun, 3 bans in 3 words). 10 h2 "One word, four visits, one way back.". 01 "no rollover bucket, no "backlog" tab, and no filter". 01 "No Gantt chart, no subtasks, no time tracking." | the checker only scans the hero lead |
| "[Brand] is the…" opener | 1 real | 01 "Taskflow is one sheet per week…" | (checker WARNs on 03 and 09 are false positives) |

### Proof, placeholders, destinations

| Pattern | n/10 | Pages | Exact example |
|---|---|---|---|
| `[… NEEDED]` visible placeholders | **8 pages, 38 instances** | 06 ×10, 08 ×8, 10 ×6, 01 ×3, 07 ×3, 02 ×2, 05 ×2, 09 ×2. (03 uses a prose placeholder plus `.invalid`. 04 invents a domain instead) | Most common: `[PRICE NEEDED]` ×4 (+3 variants), `[POSTAL ADDRESS NEEDED]`/`[ADDRESS NEEDED]` ×6, `[PROJECT NAME NEEDED]` ×3 |
| A placeholder-only section | 3 | 06 Work (3 rows, all placeholders), 08 Plans (3 × `[PRICE NEEDED]`), 10 Terms (`[PRICING NEEDED]` + `[TESTIMONIAL NEEDED]`) | 10 added a testimonial slot only to say it has none |
| Hero CTA = on-page anchor | **9** | all except 04 | `href="#start"`, `#roasts`, `#install`, … |
| Conversion endpoint = `mailto:` | 7 | 01 (form `action="mailto:"`), 02, 03, 04, 06, 08, 09 | |
| `.example` / `.invalid` domains | 7 | 01,02,05,06,08,09 `.example`, 03 `.invalid` | |
| An invented real-looking domain | 1 (+1 sample) | 04 `beta@fitpulse.app`, `support@fitpulse.app` (a domain the product may not own). 07 `orders-api.shipyard.app` in the sample | |
| Legal links as `mailto:?subject=Privacy` pseudo-pages | 4 | 01,02,04,05 | "Privacy policy (on request)" |
| Broken `og:image` | **7** | `.example` URL: 01,02,05,09. Invented domain: 04. `data:` URI, which crawlers ignore: 07,10. None: 03,06,08 | 0/10 have a working og:image |
| Design brief left as an HTML comment in shipped source | **10** | all | "BRIEF … Material reference: … Typeface: …" |

### Size and verbosity

| Metric | v1 avg | v2 avg | v2 range |
|---|---|---|---|
| Visible words | 156 | **424 (2.7×)** | 331 (05) – 510 (03) |
| File size | 5.0 KB | **18.5 KB (3.7×)** | 15.6 – 21.3 KB |
| `<section>` count | 3.3 | 4.0 | 3–5 |

The size growth is mostly CSS and disclaimers, not content the visitor needs. On 01, 04, 06 and 09, roughly 10–15% of the visible words are notes about sample data or prototype status.

---

## 3. Rule conflicts and ambiguities (deduplicated from v2-feedback.md)

Each item lists the pages that raised it.

**C1. "Every CTA goes to a real destination" vs a fictional or pre-launch product with no URLs.** (01,03,04,05,06,07,08,09)
Resolution: a destination is real if clicking it completes or advances the visitor's action *on this page or with data the user supplied*. In order of preference:
(a) an on-page section that does the thing: a working form, calculator, deck picker or order list;
(b) a URL or email the user gave in the brief;
(c) if neither exists, a single config constant declared once (`<!-- LAUNCH: SIGNUP_URL, CONTACT_EMAIL -->` plus `data-href="SIGNUP_URL"`), with the CTA rendered as a `<button>` that opens the on-page form.
Never invent a domain, `.example` included, in visible text or a `mailto:`. Never make the same anchor the target of both the hero and the nav.

**C2. "No invented proof" vs "use sample content".** (01,02,04,05,10)
Resolution: split all content into three classes.
- **Claims about the business** (stats, quotes, customer names, logos, awards, press, audit results, prices, trial terms, address, hours, team): never invent. If missing, **remove the section**; do not leave a slot.
- **Demo data inside the product artifact** (tasks, invoice lines, terminal output, a vocabulary card, a plant tag): may be invented. It must be plausible for this domain, use roles or objects rather than fake people, and be labelled **once**, in the artifact's caption.
- **Domain facts** (pothos watering interval, Argon2id): fine if true; write them for the visitor's level.

**C3. Placeholders make the page look unfinished.** (06,08,10 and others)
Resolution: at most **2** visible placeholders per page, and none in the hero or nav. A section that would be more than half placeholder is cut. All other missing facts go in one top-of-file comment: `<!-- LAUNCH TODO: price, trial length, postal address, legal pages -->`. `[TESTIMONIAL NEEDED]` is only for a testimonial section the brief explicitly asks for.

**C4. Text link vs ghost button; what a "specific secondary link" is.** (02,05,10)
Resolution: a ghost button is any secondary action with a border, a background, or padding over 0.25em, or one placed in the same flex row as the primary. A text link is inline in running text or on its own line below, uses the body font at body size, and carries only an underline. Default to no secondary action. Add one only if the visitor's first question is answered lower on the page *and* the hero does not answer it. Its label names that answer as a noun phrase ("The 21-day schedule", "shipyard.toml reference"), not a "See…" verb phrase.

**C5. What counts as a "list of three".** (01,03)
Resolution: banned means three or more parallel items used *rhetorically* in one sentence, headline or button row: series of verbs, adjectives or nouns ("Plan, assign, ship"), staccato fragments ("Push. Build. Float."), or repeated negations ("no X, no Y, no Z"). Data is allowed (tasting notes, table rows, three real plans). Test: if the sentence stays equally true with two or four items, the count is decoration, so rewrite it. The rule applies to h1, h2, lead and CTA rows, not only the lead. A section with three rows is fine if there really are three things.

**C6. What a deliberate dark theme is; dark-only vs auto swap.** (01,09)
Resolution: one finished theme beats two half-made ones.
- *Single theme* is allowed when the material implies it (a terminal is dark, kraft paper is light). Set `<meta name="color-scheme" content="light">` and say why in the brief.
- *Two themes* count as deliberate only if (1) a visible toggle exists and persists, (2) at least one element is *not* a token swap (the artifact keeps its material, or the accent changes role), and (3) every text pair and button boundary was checked in both.
- Never ship `[data-theme]` selectors without a toggle. 5/10 did.

**C7. Material reference vs banned palettes; "how specific is specific".** (02,03,07)
Resolution: the banned palettes are banned as *unmotivated defaults*. A material may land near one if the brief names the physical object and the sampled hex. But the material must come from where the visitor *uses* the product or what they *receive* (gym floor, the coffee bag that arrives, a server log, the building site). It must not come from stationery about the product. See §5 (paper ban).

**C8. How far tokens must differ from `--bg/--card`.** (08)
Resolution: renaming is not the test, structure is. Allowed: at most one "surface" token that is a small lightness shift of the page, and it is used for one component type at most. Token names describe the product role (`--receipt`, `--hull`, `--zone-3`), not ink/paper metaphors (`--ink`, `--ink-soft`, `--rule`, `--paper-deep`).

**C9. OG image in a single file.** (01,07,10)
Resolution: `og:image` must be an absolute https URL that exists. With no host, omit it and add it to the LAUNCH TODO comment. `data:` URIs and `.example` URLs are not allowed. `og:title`/`og:description` are always required.

**C10. "Generate the year" leaves it blank without JS.** (05)
Resolution: write the current year as static text and let JS update it: `<span id="y">2026</span>`. The v1 ban was on a footer made of *only* "© 2026 Brand. All rights reserved.", not on a static year.

**C11. Legal links with no destination.** (05,01,02,04)
Resolution: if there are no legal pages, show no legal links and list them in LAUNCH TODO. `mailto:?subject=Privacy` is not a privacy policy.

**C12. Contrast and 360px "checked by eye", no tool available.** (01,02,05,06,08,09)
Resolution: ship a runnable check. Extend `slop_check.py` to resolve dark-theme tokens (§5.4) and add `--contrast-table`, which prints every resolved text/bg pair for both themes. The skill should require running it and pasting the FAIL lines, which must be empty.

**C13. "Real screenshot" vs CSS mock.** (04)
Resolution: a CSS/SVG artifact is "real" if it shows a specific state the product produces: a number, a refusal, a failure, a decision. It is generic if it would still make sense with the product name changed.

**C14. Ruled rows becoming the new default.** (04, confirmed 10/10)
Resolution: no single content form (ruled rows, table, dl, cards) may be used for more than 2 sections on a page. Each section's form is chosen from its data shape (see §5.2 rule 2).

**C15. Studio Mara is praised, but the swap test says don't copy it.** (06; and 6/10 copied its logo and h1)
Resolution: remove the outlier's concrete traits from SKILL.md (§5.1). Describe *why* it worked: every choice came from drawing-sheet conventions. Do not describe *what* it did.

**C16. Does a mid-tone section background count as a card?** (01)
Resolution: no. A card is a bounded box repeated three or more times as siblings. A full-bleed band is a section. Only one inverted band per page (§5.2).

---

## 4. Quality regressions

| Page | v1 → v2 problem | Evidence |
|---|---|---|
| **06 Studio Mara** (v1's best page) | Now reads as unfinished. An architecture firm shows **zero built work**: the Work section is 3 rows of `[PROJECT NAME NEEDED]` / `[LOCATION, YEAR, PHOTO NEEDED]`. The contact `<dl>` is all placeholders, and the email's visible text is `[STUDIO EMAIL NEEDED]` while its href goes to `hello@studiomara.example`. The footer is a placeholder too. 10 placeholders in total. The SVG plan is excellent, but the page cannot convert | lines `project-row` ×3, `contact-lines` |
| **10 Lingo Loop** | Dead-end funnel. The hero CTA "Pick your first deck" leads to a table where 2 of 3 decks are "In writing", and nothing in it can be picked. "Join a deck's waiting list at the contact address below" points to `[CONTACT EMAIL NEEDED]`. There is no working contact anywhere. Terms is placeholders only, including a `[TESTIMONIAL NEEDED]` slot the skill itself suggested | 6 placeholders |
| **08 Greenleaf** | A Plans section with three `[PRICE NEEDED]`. It kept a pricing section (because SKILL.md praises the Sprout/Bloom/Jungle names) but has no prices. Dark mode: `.cta{background:var(--pot-black)}` equals the dark page `#141A15`, so the button boundary is **1.0:1** (WCAG 1.4.11 fail), and `.band-shelf` merges into the page | 8 placeholders |
| **07 Shipyard** | h1 "Push. Build. Float." breaks the list-of-three, "X. Y." formula and brand-pun rules at once. The checker missed it because it only scans the lead. The footer's Contact and Legal columns are plain-text placeholders, so the visitor has no way to reach anyone. `og:image` is a data URI | |
| **01 Taskflow** | "Taskflow is one sheet per week…" opener (a banned rule). 491 words against 111 in v1. The form `action="mailto:"` with `enctype="text/plain"` is a brittle prototype. 4 sample/prototype disclaimers | |
| **02 Brewly** | Overdesigned skeuomorphism: rotated bag + 27-point zigzag `clip-path` + rotated sticker + offset-shadow "stamp" button + `settle` keyframe + a hover that pads the rows. `tel:+10000000000` is a fake phone link wrapped around `[PHONE NEEDED]`. It copied "Pick a roast" and $17 from the skill | |
| **05 Ledgerly** | Stacked effects: a red margin line on `<body>` + rotated invoice + offset shadow + rotated "thud" stamp + lined-paper section. The footer year is blank without JS. Legal links are mailto "on request" | |
| **09 Vaultix** | The hero lead is cryptography jargon (Argon2id, 64 MiB, XChaCha20-Poly1305) for a consumer audience. Without JS the copyright reads "© Vaultix Vaultix" (`<span id="yr">Vaultix</span> Vaultix`). `data-theme` selectors exist with no toggle | |
| **04 FitPulse** | Invents a real-looking domain (`fitpulse.app`) for every CTA and for og:image, so beta requests would go to a domain the product may not own. Auto swap only. Otherwise one of the strongest v2 pages: it was the only one without a mono font or paper | |
| **03 Nimbus** | Strongest overall. Its regression is mostly sameness: Newsreader + Plex Mono, sage paper, pencil tokens, "Where Nimbus stops." `:root[data-theme="dark"]` holds only `color-scheme` | |
| All | 2.7× the words and 3.7× the bytes. Visible sample/prototype disclaimers on 10/10. Pre-launch framing on 6/10. Every page reads as an honest mockup, not a product page. 7/10 broken og:image. 5/10 dead theme CSS | |

Checker false positives: 05 `FAIL low contrast #10201a on #9c2a24` (the checker resolves light tokens inside a `[data-theme="dark"]` rule, and the real pair is `#10201a` on `#e68b81`, about 6.5:1). 09 `#9aa59c` (a green-gray border token, which the hue-blind `#9aa` prefix regex catches). 03 and 09 "[Brand] is…" (the regex matched "Every change Nimbus makes" and "Your master password is").

---

## 5. Concrete edits

The principle behind every edit: **ban the convergence point, then require a divergence procedure, never a new fixed choice.** Remove concrete examples that agents copy verbatim.

### 5.1 SKILL.md

**(a) Replace the whole "### 1. Before writing code: the product brief (required)" block with:**

```markdown
### 1. Before writing code: the product brief (required)
Write these down in your reasoning (not in the shipped file):
- **Visitor:** who arrives and the one question they must answer before acting.
- **Product artifact:** the one real thing that proves the product, shown in a specific state (a refusal, a failure, a total, a decision). It goes in the hero.
- **Material reference:** take it from where the visitor *uses* the product or what they *receive* (the gym floor, the bag on the doorstep, the server log, the plot of land), never from stationery *about* the product. Paper, notebooks, ledgers, index cards, galley proofs, vellum, labels, tags and rubber stamps are off-limits unless the product itself is a printed object. List three candidate materials, cross out the first one that came to mind, and pick from the other two. Derive every token from it and name the tokens for product roles (`--receipt`, `--zone-3`, `--hull`), not for ink and paper (`--ink`, `--ink-soft`, `--rule`, `--paper-deep`, `--pencil`).
- **Typeface:** list three candidates from three different classifications (e.g. grotesk, slab, humanist serif, condensed, rounded, display). Cross out the first one you thought of. Default to **one** family; a second family needs a job the first cannot do. Use a monospace face only if the page shows code, a terminal or columns of figures that must align, and then only inside those elements, never for nav, labels, buttons or footers.
- **Composition:** sketch three hero compositions in words (e.g. artifact full-bleed with the headline as its caption; headline set into the artifact; artifact above a stacked claim; copy right of artifact; artifact only, claim below the fold). Reject "copy left, artifact right" unless the other two are worse for this artifact, and say why.
- **Sections:** list only the sections this visitor needs, in the order of their questions. For each, name its data shape (sequence, comparison, single number, map, conversation, gallery) and pick the form from that shape. No form may repeat in more than two sections.
- **What you don't have:** list the facts the brief did not give (price, address, legal pages, testimonials, URLs). Those sections are cut, not stubbed (see rule 10).
```

**(b) Replace hard bans 5, 6, 10, 11 and 12 with:**

```markdown
5. One primary hero action named for its action and object, written fresh for this product (do not reuse example labels from this skill). Default to no secondary action. If you add one, it is plain underlined body text on its own line, with no border, no box and no "See…" verb; it names the evidence it leads to. [9]
6. No rhetorical list of three anywhere in h1, h2, lead or button rows: no "A, B and C", no "X. Y. Z." staccato, no "no X, no Y, no Z". Data lists are fine. If the line works equally well with two or four items, rewrite it. No "[Brand] is the…" opener. [9/8; v2 still 4]
10. Never invent claims about the business: stats, quotes, customers, prices, terms, address, audit results. If the brief lacks them, **cut the section**; do not leave a slot. Demo data *inside the product artifact* may be invented, must use roles rather than fake people, and is labelled once in the artifact caption. At most 2 visible `[… NEEDED]` placeholders per page, none in the hero; list everything else in one `<!-- LAUNCH TODO: … -->` comment at the top of the file. [v1 2–5 invented; v2 38 placeholders on 8 pages]
11. Every CTA advances the visitor's action: an on-page section that does the thing (form, calculator, picker), or a URL/email the user supplied. Never invent a domain (no `.example`, `.invalid` or plausible `.app` in visible text, `href`, `mailto:` or `og:image`). No `href="#"`, no fake `tel:`, no `mailto:?subject=Privacy` pretending to be a legal page. [v1 6; v2 7 invented domains]
12. No missing `transition`, `:focus-visible` or `prefers-reduced-motion`; every text pair ≥ 4.5:1 and every button boundary ≥ 3:1 against its page, **in every theme you ship**. Ship one finished theme or two with a working toggle; never ship `[data-theme]` selectors without a toggle. Run `scripts/slop_check.py` and fix every FAIL. [10/10/10/7; v2 5 dead theme blocks]
```

**(c) Add new hard bans 15–20 (second-order defaults, from the v2 run):**

```markdown
15. No stationery template: sage/grey-green "paper" background (`#dde2db`–`#eef1e4`), green-black dark (`#0c1412`–`#171b1a`), green-grey muted ink, pencil/oxblood red accent turning salmon in dark mode. [v2 8/8/8/7]
16. No serif-display + IBM Plex Mono / JetBrains Mono pairing, no Newsreader by reflex, no h1 with an italic or colored `<em>` fragment, no `letter-spacing:-.012em` / `line-height:1.02–1.04` / `max-width:34ch` lede as a formula. [v2 7/5/8/6/10/9]
17. No tracked-uppercase mono micro-labels as the page's voice: max one uppercase label style, used in at most two places. No tracked-uppercase wordmark unless the brand already has one. [v2 10/6]
18. No ruled rows for every section, no 4-column "Product · Contact · Legal" footer with uppercase headings, no `minmax(0,5fr) minmax(0,7fr)` split, no single `4vw` gutter for every section. [v2 10/8/4/8]
19. No skeuomorphic stack: pick at most one of rotated artifact, rubber stamp, offset "press" shadow, ruled-paper gradient, `clip-path` shape. [v2 3/2/3/3/3]
20. No disclaimer clutter: one "sample" label per artifact, no "Prototype:" paragraphs, no "not X advice" lines unless legally required, no count-led h2 ("Four passes…", "Five zones…"), no "What happens after…" headings. [v2 10/7/4]
```

**(d) Add to "### 3. Before shipping: self-check":**

```markdown
13. **Second-order swap test:** would this page sit unnoticed among the pages this skill already produced (sage paper, serif h1 with an italic word, Plex Mono labels, ruled rows, red pencil, 4-column footer, `[… NEEDED]`)? If yes, return to step 1 and take the second candidate for material, typeface and composition.
14. Count the visible placeholders and disclaimers: ≤ 2 placeholders, ≤ 1 "sample" label per artifact.
15. Does every section's form differ from the section before it?
16. Is any label, price or phrase copied from an example in this skill? Replace it.
```

**(e) Replace the whole "## What the good outliers did" section with:**

```markdown
## Copy the method, not the result
The one v1 page that did not look templated (architecture) worked because every choice came from its own domain's conventions: drawing sheets set its corners, its lettering and its rows. When later agents copied its *results* (tracked uppercase logo, weight-400 serif h1, square corners, ruled rows) onto a coffee shop, a password manager and a language app, those results became the next template (6/10, 6/10, 10/10, 10/10). Do the same thing it did: find the conventions of *this* product's world and let them set the form. Never borrow another page's form.
Distinctive parts were always a piece of the product itself, in a specific state. Build outward from that piece.
```

**(f) Remove verbatim-copyable examples.** In SKILL.md rule 5, replace `("Deploy your first app", "Pick a roast")` with `(write it for this product; labels quoted in this skill are examples of shape, not text to reuse)`. Apply the same change in dont-list.md Layout 3, Copy 4 and Copy 1 (`"ships within 48 hours of roasting"`), Copy 8 (the 02 headline example) and Layout 7 (`"$17 a bag, ships Tuesdays"`). For each, either delete the example or prefix it with *"Shape only, do not reuse:"*.

### 5.2 references/dont-list.md

**Replace Layout rule 1's "Instead:" with:**
`Instead: give each section the width its content needs (a 60–75ch text measure, a full-bleed artifact, a wide table) and let at least two sections have different horizontal edges. One shared fluid gutter (4vw, clamp(16px,4vw,48px)) for every section is the same wrapper with a new number.`

**Replace Components rule 1's "Instead:" with:**
`Instead: name the section's data shape first (sequence → timeline or log; comparison → table; one number → a single large figure; spatial → map or plan; dialogue → transcript; inventory → shelf with images) and choose the form from it. Ruled rows are one option, not the alternative to cards: no form may be used in more than two sections of one page.`

**Replace Components rule 4 with:**
`4. **Do not pair a solid button with a ghost button** [9], **and do not make the secondary action a "See…" text link beside the primary** [v2 4].
   Instead: default to one action. A secondary action, if earned, is underlined body text on its own line with no border, background or padding, and names the evidence it leads to.`

**Replace Copy rule 1 with:**
`1. **Do not use a rhetorical list of three** in the h1, h2s, lead or CTA row: series ("Plan, assign and ship"), staccato ("Push. Build. Float."), stacked negations ("no config, no servers, no stress") [v1 9; v2 4].
   Not a violation: real data (tasting notes, three actual plans, table rows). Test: if the line works as well with two or four items, the count is decoration.`

**Replace Copy rules 10 and 11 with:**
```markdown
10. **Do not invent claims about the business** (stats, quotes, customer names, prices, terms, address, audits) [v1 2–5], **and do not stub them either** [v2: 38 `[… NEEDED]` on 8 pages; three sections made only of placeholders].
    Instead: if the brief lacks the fact, cut the section and list it in a `<!-- LAUNCH TODO -->` comment. Max 2 visible placeholders per page.
11. **Do not ship demo data that looks like a real third party** ("Northwind Studio", "Maya R.", a plausible `.app` domain) [v1 5; v2 1].
    Instead: demo data lives inside the product artifact, uses roles or objects ("Dev", "Guji lot 24-11"), and is labelled once in the caption. Never more than one "sample" note per artifact.
```

**Replace Color rule 2 with:**
`2. **Do not ship half a dark theme**: an auto token swap under prefers-color-scheme [v1 8; v2 7], or `[data-theme]` selectors with no toggle [v2 5].
   Instead: ship one finished theme (set meta color-scheme and say why), or two with a persistent toggle in which at least one element changes role, not just value, and every pair is checked in both.`

**Replace Typography rule 1's "Instead:" with:**
`Instead: list three candidate families from different classifications, cross out the first that came to mind, and choose for this product. Default to one family. A monospace face appears only inside code, terminal or aligned-figure elements, and only if the page has them.`

**Replace Imagery rule 5 with:**
`5. Do keep **a CSS/SVG product artifact in the hero** [v1 6; v2 10], but show it in a specific state (a refusal, a failure, a total). Do not wrap it in the stock chrome strip (label left, "sample" right) [v2 8], and do not make it interactive just to have a "Try it" moment [v2 9 interactive or animated; 3 "Try it"]. Interactivity has to be the product's own core action.`

**Add a new section after "Code quality and accessibility":**

```markdown
## Second-order defaults (pages that followed this skill converged here)
Measured on 10 skill-guided pages (v2). These are now as recognisable as the v1 template.

1. **Stationery material** (pad, ledger, galley proof, vellum, index card, label, stamp) [7; 10 chose a printed/marked surface]. Instead: take the material from where the visitor uses or receives the product.
2. **Sage paper / green-black / green-grey ink** (`#e4e8e1`, `#16201a`, `#46564b`) [8/8/8]. Instead: tint neutrals toward *this* brand's accent hue; if that hue is green, say why the product is green.
3. **Pencil-red accent turning salmon in dark** (`#a3261c` → `#ff8f7e`) [7]. Instead: derive the accent from the material, not from editing marks.
4. **Serif + IBM Plex Mono** [7; Plex Mono 8; Newsreader 5]. Instead: one family, chosen by the three-candidate procedure.
5. **Italic `<em>` in a weight-400 h1, -.012em, line-height ~1.03, lede at 34ch** [8/6/6/10/9]. Instead: set the h1 from the headline's length and the face; emphasis only if the phrase is the claim.
6. **Tracked uppercase mono micro-labels everywhere; tracked uppercase wordmark** [10/6]. Instead: one label style, two uses max.
7. **Copy-left / artifact-right split hero at 5fr/7fr** [10 split; 3 exact 5/7]. Instead: choose among three sketched compositions.
8. **Ruled rows in every section; tables collapsing to blocks** [10; 6 tables]. Instead: form per data shape, max two sections per form.
9. **Artifact chrome strip with "sample" at the right** [8]. Instead: let the artifact's own header carry real content.
10. **Skeuomorph stacking** (rotation, stamp, offset shadow, ruled gradient, clip-path) [up to 4 on one page]. Instead: one physical cue at most.
11. **Count-led h2s, "What happens after…", "What it costs and what…", "Where X stops"** [7/4/2/3]. Instead: headings that state the section's finding.
12. **Mailto everything; `.example` domains; mailto legal links; data-URI og:image** [7/7/4/7]. Instead: see Code 3 and the LAUNCH TODO comment.
13. **Disclaimer clutter** ("sample", "prototype", "illustrative", "not X advice") [10]. Instead: one caption on the artifact.
14. **4-column footer with uppercase headings "Product · Contact · Legal"** [8; `repeat(auto-fit,minmax(11rem,1fr))` on 3]. Instead: show only the footer facts that exist; one line is fine if that is all there is.
15. **Copied skill examples** ("Deploy your first app", "Pick a roast", "Book a site visit", $17) [3]. Instead: examples here are shapes, not text.
```

### 5.3 New checker rules (add to `slop_check.py`)

Category and level are given in brackets. Patterns are Python regexes run against `css` (lowercased CSS), `low` (lowercased HTML) or `text`/`visible` as in the existing code.

```python
# ---- second-order: typography
MONO_FAMILIES = r"family=(ibm\+plex\+mono|jetbrains\+mono|space\+mono|dm\+mono|roboto\+mono|fira\+code|source\+code\+pro)"
if re.search(MONO_FAMILIES, low) and not re.search(r"<(pre|code|kbd|samp)[\s>]", low):
    add("FAIL", "type", "monospace web font loaded but the page shows no code/terminal (v2: 7/10)")
elif re.search(MONO_FAMILIES, low):
    add("WARN", "type", "monospace face loaded - keep it inside code/terminal elements only")
if re.search(r"(nav|footer|masthead|colophon|kicker|label)[^{}]*\{[^}]*(mono|monospace)", css):
    add("WARN", "type", "mono used for nav/footer/labels (v2: 9/10)")
if re.search(r"family=newsreader", low):
    add("WARN", "type", "Newsreader - second-order default serif (v2: 5/10)")
if re.search(r"<h1[^>]*>[^<]*<(em|span|mark|i)\b", low):
    add("WARN", "type", "emphasized fragment inside h1 (v2: 8/10)")
if re.search(r"letter-spacing\s*:\s*-\.01[0-5]em", css):
    add("WARN", "type", "h1 tracking -.010–.015em (v2 stock value -.012em, 6/10)")
if re.search(r"max-width\s*:\s*3[2-6](ch|rem|em)\b", css):
    add("WARN", "type", "lede measure ~34ch/rem/em (v2: 9/10)")
n_upper = len(re.findall(r"text-transform\s*:\s*uppercase", css))
if n_upper >= 6:
    add("WARN", "type", f"{n_upper} uppercase label rules - one label style, two uses max")

# ---- second-order: layout
if re.search(r"minmax\(\s*0\s*,\s*5fr\s*\)\s+minmax\(\s*0\s*,\s*[6-8]fr\s*\)", css):
    add("WARN", "layout", "5fr/7fr split (v2 stock split, 10/10 split heroes)")
if len(re.findall(r"max\(\s*16px\s*,\s*4vw\s*\)|clamp\(\s*(16px|1rem)\s*,\s*4vw\s*,\s*(48px|3rem)\s*\)", css)) >= 3:
    add("WARN", "layout", "one 4vw gutter on every section - the new .wrap (v2: 8/10)")
if re.search(r"repeat\(\s*auto-fit\s*,\s*minmax\(\s*1[01]rem\s*,\s*1fr\s*\)\s*\)", css):
    add("WARN", "layout", "auto-fit minmax(11rem,1fr) footer grid (v2: 3/10, identical)")
n_rules = len(re.findall(r"border-(top|bottom)\s*:\s*1px\s+solid\s+var\(--[\w-]*(rule|line|edge)", css))
if n_rules >= 5:
    add("WARN", "layout", f"{n_rules} ruled-row borders - ruled rows used as the default form (v2: 10/10)")
if re.search(r'class="opening"', low):
    add("WARN", "code", "hero class 'opening' (v2: 6/10)")

# ---- second-order: color / tokens
STATIONERY = set(re.findall(r"--[\w-]*(pencil|ink|paper|rule|stamp|margin|vellum|graphite|newsprint)[\w-]*\s*:", css))
if len(STATIONERY) >= 3:
    add("WARN", "color", "stationery token vocabulary (ink/paper/rule/pencil) - renamed --fg/--bg/--line (v2: 9/10)")

def hsl(hexv):
    import colorsys
    r, g, b = hex_to_rgb(hexv); h, l, s = colorsys.rgb_to_hls(r, g, b); return h * 360, s, l
m = re.search(r"body\s*\{[^}]*background(?:-color)?\s*:\s*([^;]+)", css)
root = re.search(r"(?<![\w-]):root\s*\{([^}]*)\}", css)
tok = dict(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", root.group(1))) if root else {}
bg = resolve(m.group(1), tok) if m else None
if bg and hex_to_rgb(bg):
    h, s, l = hsl(bg)
    if 60 <= h <= 170 and s < 0.25 and 0.84 <= l <= 0.95:
        add("WARN", "color", f"sage/grey-green paper background {bg} (v2: 8/10)")
for d in re.findall(r"prefers-color-scheme\s*:\s*dark[^{]*\{[^}]*?--[\w-]+\s*:\s*(#[0-9a-f]{6})", css)[:1]:
    h, s, l = hsl(d)
    if 90 <= h <= 170 and l <= 0.12:
        add("WARN", "color", f"green-black dark background {d} (v2: 8/10)")
if re.search(r"#(9c2a24|a3261c|a82d1b|b3402a|a21f19)\b", css) or re.search(r"--[\w-]*(pencil-red|margin-red|strike-red)", css):
    add("WARN", "color", "pencil/margin red accent (v2: 7/10)")

# ---- second-order: theme
if re.search(r"\[data-theme", css) and not re.search(r"setattribute\(\s*['\"]data-theme", low):
    add("FAIL", "code", "[data-theme] selectors but no toggle sets data-theme (v2: 5/10)")

# ---- second-order: effects
if re.search(r"box-shadow\s*:\s*\d+px\s+\d+px\s+0\s", css) and re.search(r":hover[^{]*\{[^}]*translate\(", css):
    add("WARN", "effects", "offset 'press' shadow + translate hover (v2: 3/10)")
skeuo = sum(bool(re.search(p, css)) for p in (
    r"transform\s*:\s*rotate\(-?[0-9.]+deg\)", r"repeating-linear-gradient", r"clip-path\s*:\s*polygon",
    r"box-shadow\s*:\s*\d+px\s+\d+px\s+0\s"))
if skeuo >= 3:
    add("WARN", "effects", f"{skeuo} skeuomorphic effects stacked - pick one")

# ---- second-order: proof / destinations
ph = re.findall(r"\[[A-Z][A-Z ,/&]+ NEEDED\]", text)
if len(ph) > 2:
    add("FAIL", "copy", f"{len(ph)} visible [… NEEDED] placeholders - cut sections, max 2 (v2: 38 on 8 pages)")
if re.search(r'(href|content|action)="[^"]*\.(example|invalid)\b', low):
    add("FAIL", "code", ".example/.invalid domain in a link, form or meta - use a supplied URL or cut it (v2: 7/10)")
if re.search(r'href="tel:\+?1?0{7,}', low):
    add("FAIL", "code", "fake tel: link")
if re.search(r'href="mailto:[^"]*\?subject=(privacy|terms)', low):
    add("WARN", "code", "mailto pretending to be a legal page (v2: 4/10)")
if re.search(r'property="og:image"\s+content="(data:|[^"]*\.example)', low):
    add("FAIL", "code", "og:image is a data: URI or .example URL - crawlers cannot fetch it (v2: 7/10)")
if re.search(r'id="(yr|year|y)"\s*>\s*</span>', low):
    add("WARN", "code", "empty year span - blank without JS; put the year in as fallback")

# ---- second-order: copy (visible text)
v = visible
for hm in re.findall(r"<h[12][^>]*>(.*?)</h[12]>", text, flags=re.S | re.I):
    h_txt = re.sub(r"<[^>]+>", "", hm).strip()          # strip <span>/<em> first
    if re.fullmatch(r"(?:\w+\.\s+){2,}\w+\.?", h_txt):
        add("FAIL", "copy", f"staccato 'X. Y. Z.' heading: “{h_txt}”"); break
    if re.search(r"\b\w+, \w+,? (and|or) \w+", h_txt):
        add("WARN", "copy", f"heading built on a list of three: “{h_txt[:60]}”"); break
if re.search(r"<h2[^>]*>\s*(one|two|three|four|five|six|seven)\b", low):
    add("WARN", "copy", "count-led h2 ('Four passes…') (v2: 7/10)")
if re.search(r"\bwhat happens (after|in|when)\b", v, re.I):
    add("WARN", "copy", "'What happens after…' (v2: 4/10)")
if re.search(r">\s*see (the|what|where|one|how|our)\b[^<]{0,40}<", low):
    add("WARN", "copy", "'See …' secondary link (v2: 4/10)")
if re.search(r">\s*[a-z]+ your first [a-z]+", low):
    add("WARN", "copy", "'[Verb] your first [noun]' CTA (v2: 5/10)")
if re.search(r"deploy your first app|pick a roast|book a site visit|\$17 a bag", low):
    add("FAIL", "copy", "copied an example from the skill verbatim")
if re.search(r"\btry it\b", v, re.I):
    add("WARN", "copy", "'Try it' widget prompt (v2: 3/10)")
n_disc = len(re.findall(r"\b(sample|illustrative|prototype|placeholder|example format|made-up)\b", v, re.I))
if n_disc >= 4:
    add("WARN", "copy", f"{n_disc} sample/prototype disclaimers - one caption per artifact")
if re.search(r"desk[- ]lamp", low):
    add("WARN", "color", "'desk lamp' dark theme narrative (v2: 2/10)")
```

**Smoke test** (standalone versions of the key regexes; pages hit, v2 / v1): mono font with no `<pre>/<code>` 6/0 (01 contains a `<pre>` log and inline `<code>`, and 07 is a real terminal); h1 emphasized fragment 8/5 (v1's 5 are the gradient `<em>`s, so the rule fits both generations); `-.01xem` 6/0; lede 32–36 ch/rem/em 9/2; `5fr/6–8fr` split 8/0; ≥3 stationery tokens 10/0; dead `[data-theme]` 5/0; >2 `[… NEEDED]` 5/0; `.example/.invalid` in an attribute 7/1; bad og:image 6/0; count-led h2 7/0; staccato heading (after stripping tags) 1/0 (07 "Push. Build. Float."). Treat the remaining snippets as drafts to be tested once they are merged into `check()`.

### 5.4 Checker bug fixes (from §4)

1. **Dark-theme contrast:** in `check_contrast`, build a second token map from `:root[data-theme="dark"]{…}` or the first `@media (prefers-color-scheme:dark){ :root… {…} }`. Use the dark map when the selector contains `data-theme="dark"` or the rule sits inside a dark media block. This removes the 05 false positive and catches real dark failures. Also check non-text boundaries: for a button whose `background` equals the page background in either theme, FAIL "button boundary 1.0:1" (catches 08).
2. **Muted blue-gray:** replace `SLOP_MUTED = #9aa…` with a hue test: flag a `color:` hex where hue is 200–235°, saturation 8–30% and L 55–75%. `#9aa59c` (hue ~135°) would then pass.
3. **List of three:** run the existing lead regex on the h1 and every h2 too (see 5.3). Today "Push. Build. Float." passes.
4. **Brand opener:** take the brand from `<title>` (text before `–`, `-`, `:` or `|`) and match only `^\s*{brand}\s+(is|turns|helps|makes|lets)\b`. That removes the 03 and 09 false positives and keeps 01.
5. **"no image/svg" FAIL:** downgrade to WARN when the hero contains an element with `role="img"` and an `aria-label` (02, 10 draw their artifact in CSS). Keep the FAIL when there is no artifact at all.
