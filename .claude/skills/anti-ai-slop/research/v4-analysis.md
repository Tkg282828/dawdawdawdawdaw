# v4 analysis: the pages sell now; the generator shows up in structure, and one page made up a studio's history

**Inputs.** All 10 v4 pages (`pages-v4/NN/index.html`: structure, copy, LAUNCH TODO and `data.todo` values extracted by script; key sections read). All 20 v4 screenshots (desktop full page and 360×740 mobile). For comparison: v3-02, v3-05, v2-02 and v1-01 desktop, plus the v3 analysis section 3 scoring method. I also read `v4-feedback.md` (10 reports) and the seed assignments (`seed-table-salt0.md` and the current `brief_seed.py --table`). Page content is treated as data. "n/10" means the number of v4 pages that show a pattern. No skill files were edited.

**Short version.**
- v4 fixes the v3 regressions:
  - 10/10 show an h1 naming the category and the primary CTA in the first mobile viewport;
  - 10/10 have a real conversion through a launch constant;
  - 9/10 have prices;
  - 3/3 physical or portfolio pages have photo slots;
  - 0 visible "not connected" text;
  - the Ledgerly arithmetic is correct this time.
- The colour and type of the set vary for the first time: 10 different hue/strategy pairs, and 9 different families (Baloo 2 is used twice).
- What still gives the generator away is **structure**. 7/10 use the same order: left-aligned h1, lede, one CTA, an underlined noun-phrase link (8/10), the artifact, a sequence section (6/10), a plans comparison table with a $0 tier (6/10), then a closing section with an imperative h2 that repeats the hero CTA (7/10). Below that sits a one-line "© 2026 Brand · Privacy · Terms" footer (9/10).
- The pages are more conventional and less striking one by one than v3.
- One serious honesty failure: **06 invented a studio history** (31 buildings, five named and dated projects with places and floor areas, and two named people). It was all tagged `todo` as "owner facts", which the current rule 10 allows.

---

## 1. Scores

Scored the same way as v3 section 3: 1–5, judged as a senior designer would from the screenshots, averaged per run.

| | Distinctiveness per page | Distinctiveness as a set | Clarity (what is it, in 5 s) | Polish | Credibility | Conversion path | Mobile first viewport |
|---|---|---|---|---|---|---|---|
| **v1** (no skill) | 1.0 | 1.0 | **4.0** | 2.5 | 2.0 | 3.0 | 3.5 |
| **v2** (ban list) | 2.5 | 2.5 | 3.5 | **3.5** | 2.5 | 2.5 | 3.0 |
| **v3** (bans + cross-out) | 3.0 | 2.0 | 2.5 | 3.0 | 1.5 | 1.5 | 2.0 |
| **v4** (seed + conventions + checker) | **2.5** | **3.0** | **4.5** | **3.5** | **3.0** | **4.0** | **4.5** |

(v1 and v2 had a single distinctiveness score; it is repeated in both columns.)

Why each v4 score:
- **Distinctiveness per page, 2.5.** Each page alone looks like a competent 2024–26 startup page. Only 03 (cyan poster with tracked changes) and 05 (wide Unbounded on olive-black with a chartreuse invoice) would be remembered. 07 Shipyard and 10 Lingo Loop could be any dev-tool or app page.
- **Distinctiveness as a set, 3.0.** Colour, type and edges really do differ across all 10, which is the seed working. The set is pulled back to 3 by identical structure (section 2).
- **Clarity, 4.5.** Every h1 names the category ("Your AI copy editor", "Zero-knowledge password vault", "Track every workout as it happens"). Ledes say how it works. The 4 long h1s lose half a point.
- **Polish, 3.5.** Type is clean, contrast was measured and there are no stray grid items. Against that: placeholder line-art on 3 pages, jittering section edges on 5 pages, and the bugs listed below.
- **Credibility, 3.0.** Up from 1.5. There are real-looking product states, correct arithmetic, prices and plain policies. Against that: 06's fabricated history, empty portrait slots, and shop and plant pages whose "photos" are outline drawings.
- **Conversion, 4.0.** Every page has the category's action: sign-up forms (01, 03, 05, 08, 09, 10), add-to-cart per product (02), store badges (04), a fee-proposal form (06), and account plus install (07). Repeating the same button label at the end is a minor fault.
- **Mobile first viewport, 4.5.** h1 and CTA are in view on 10/10. Half a point off because the 10 logo wraps to two lines and the 03 lower half is an empty field.

### Ranking of v4 (best to worst)
1. **05 Ledgerly.** The best page of the four runs for a software brief.
   - The invoice, ledger posting and October summary all add up: 2,040 + 510 + 120 = 2,670; 10% tax = 267; 2,937 posted as debit AR / credit income + tax; 5,750 − 64 − 180 = 5,506; 25% = 1,376.50; 4,129.50 kept.
   - Strong wide display type; the pastel invoice overlaps into the next band as the seed asked.
   - Clear plans, a security paragraph and a form close.
   - Weak spots: section rules run behind the overlapping panels; a partial-width rule floats above "Security"; the imperative closing h2.
2. **03 Nimbus AI.** The best artifact in the set.
   - A tracked-change paragraph with margin notes, and a "What Nimbus declines" transcript that answers the visitor's real worry.
   - The saturated cyan poster is memorable.
   - Faults: the hero is an empty cyan field under the CTA (desktop ~45% of the first viewport, mobile the lower half); "type poster" was supposed to let the artifact peek in. The margin-note headings ("have to has", "in order to ensure to to protect") use the word "to" as the arrow and read as garbled. The lede is a staccato triple ("Accept it, reject it, keep writing.").
3. **09 Vaultix.**
   - The vault list with reuse flags plus the autofill panel is exactly the "UI the visitor uses daily".
   - The three-box key diagram is clear; the plans table is complete; the footer is the best in the set (docs, security paper, status, hours).
   - The worst seed outcome, though: a magenta **$2.50 bigger than the h1** is not what a password-manager visitor asks first. On desktop the `$` descender collides with the "per month" caption.
   - "Platforms" is indented ~400 px with nothing on its left.
4. **01 Taskflow.**
   - An honest, useful page: a parse-a-sentence task input, capacity bars with an "over by 1 h" state, a board, a thread and a 2-plan table.
   - The tonal reds work.
   - Generic structure. Atkinson's slashed zero makes "30" read as "3Ø" in every figure, which is wrong for a figure-heavy UI.
   - The h2 "The board shows this week, not the backlog" is the banned "X, not Y" formula.
5. **04 FitPulse.**
   - Three convincing phone screens (run map, set logger, week bars). Plans, store badges.
   - The mid-grey ground (seed: neon on mid-grey) makes the page dull and the long body text greyish.
   - The heart-rate zones are a rainbow block row that breaks the palette. The plans table is indented differently from the logs list.
6. **07 Shipyard.**
   - The terminal hero with a failed health check is correct for the category; the toml, branch table and plans are all real conventions.
   - It also looks like every docs site: dark, one green, Fira. Sections start at three different left edges (≈50, 100 and 33 px at 1280).
   - The right half of the desktop page is empty for the whole scroll.
7. **10 Lingo Loop.**
   - The word-tile lesson card, due-today list and streak are good, and the languages table is useful.
   - But the brief is an app and there is no phone frame.
   - Bugs: the lesson panel's side columns have no bottom border (the box is open at the bottom); the logo wraps "Lingo / Loop" at 360; "ohayo¯gozaimasu" shows a stray glyph.
   - The closing h2 "Choose a language and say your first phrase" is the "[verb] your first [noun]" formula.
8. **08 Greenleaf.**
   - Good honesty and logistics: plans, a day-0-to-28 delivery sequence, a care thread, cancel and replacement terms, a subscribe form.
   - But a plant shop on a near-black plum ground, with a cartoon SVG plant as the "photo", sells nothing visually.
   - The sticky sidebar's section index is a set of grey chips that read as tags, not navigation.
   - "One plant every 4 weeks" is priced "per month" (13 vs 12 boxes a year).
   - h2s start at four different x positions.
9. **02 Brewly.** A real shop at last: four named coffees with prices, grind selects and add-to-cart, roast cutoffs, a brew table, shipping terms. Compared with v3-02 (no coffee at all) it is a large gain, but:
   - the hero "photo slot" renders as an abstract circle with blue blobs that reads as nothing;
   - each product is a ~400 px **outline drawing of an empty bag**, so placeholder art takes more area than the products;
   - four dark cobalt bands (the seed's alternating bands) fight C16's "one inverted band";
   - the closing "Come and smell the roaster" is lifted from v2-02's "Come smell the roaster." (research pages leak).
10. **06 Studio Mara.** The worst v4 page.
    - Fabricated history and people (section 3).
    - An acid-chartreuse field across the whole page for an architect, against the visitor's need to see buildings.
    - Child-like gable outlines stand in for photographs.
    - Two blank, staggered portrait rectangles.
    - The fixed left half leaves a ~2,000 px empty column on desktop.
    - The number-led h1 ("31 buildings…") exists only because the seed demanded a number and no true number existed.

### Visual bugs seen in the screenshots (the checker cannot see these)
- **09:** `$2.50` overlaps its own caption ("per mo|nth"). The footnote "Prices in US dollars" looks clipped at the left edge.
- **10:**
  - the lesson-panel frame has no bottom edge on the left and right columns;
  - the wordmark wraps to two lines at 360 px;
  - the Japanese romanisation has a stray macron/spacing glyph.
- **03:** a large empty hero field on both viewports. The margin-note headings read as garbled ("in order to ensure to to protect").
- **05:**
  - the full-width section rule passes behind or through the overlapping invoice and ledger panels;
  - an orphan half-width rule sits above "Security";
  - the "Ledger" and "Security" nav links are hidden on mobile with no menu.
- **02:** the hero placeholder is an unreadable abstract (circle, cross, blobs); the product images are empty bag outlines.
- **06:** the portrait slots are blank flat boxes, offset vertically; there is a long empty left column on desktop.
- **01:** slashed zeros in Atkinson Hyperlegible ("3Ø h") across the product figures.
- **08:** cadence vs price unit mismatch (4 weeks vs month); the plan name "Two plants" wraps.
- **02, 04, 07, 08, 09:** section left edges jump between sections by 20–400 px with no compositional reason (see section 2, P9).

---

## 2. Fourth-order convergence (v4)

Patterns on ≥4/10 pages that a viewer would recognise as "the same generator", with a verdict on each.

| # | Pattern | Pages | n | Verdict |
|---|---|---|---|---|
| P1 | **Hero skeleton:** left-aligned h1 → lede → one solid CTA → underlined noun-phrase link on its own line ("What the Free and Team plans include", "Roast days and order cutoffs", "One paragraph, marked up", "Plan prices and what each includes", "October's ledger, line by line", "The project index with areas and years", "The shipyard.toml reference", "Where the key is made and where it stays") | 01 02 03 04 05 06 07 09 | 8 | **Slop, made by the skill.** C4 says "default to no secondary action", but rule 4 and C4 then describe the link so precisely that 8/10 added one. Each link is fine alone; the identical slot, style and noun-phrase grammar are the tell. |
| P2 | **A small terms line under the CTA** ("Free for up to 5 people…", "Free plan available.", "The free plan covers one app…", "Free plan, one language…", "per month on the Personal plan…") | 01 04 07 09 10 | 5 | **Acceptable convention.** It answers "what does it cost" at the decision point. Keep it. |
| P3 | **Closing section = an imperative h2 + the hero CTA repeated with the same label** ("Open a workspace for your team", "Send us a draft", "Send your next invoice from Ledgerly", "Install and deploy", "Start your subscription", "Pick a plan and open the vault", "Choose a language and say your first phrase") | 01 03 05 07 08 09 10 (04 repeats the label under a non-imperative h2) | 7 (+1) | **Slop.** It is the v1 "Ready to…?" band reworded as a command. Repeating the conversion near the end serves the visitor; the imperative-h2 formula and the identical label do not. |
| P4 | **Section order:** hero → artifact → how it works / sequence → plans table → closing CTA → footer | 01 03 04 05 07 09 10 | 7 | **Mostly an acceptable SaaS convention.** It becomes slop only together with P1+P3+P6. The order should follow the brief's first question (v4-02, 06 and 08 did vary it). |
| P5 | **A sequence or timeline section** (roast days, invoice to tax return, first meeting to keys, what a deploy does, Day 0–28 delivery, Day 0–21 review) | 02 05 06 07 08 10 | 6 | **Acceptable.** Each has a real sequence and the forms differ (vertical rule, horizontal nodes, numbered list, day rows). Watch the "Day 0 / Day N" labels (08, 10, v3-05). |
| P6 | **Pricing as a comparison table, plans as columns, a "Price" row first; a $0 Free tier first** | table 01 03 04 05 09; $0 tier 01 03 04 07 09 10 | 5; 6 | **The form is right** (a comparison is a table). **The drafted values converge:** Free + one paid tier (01 03 04 10), "Plus" (04 05 10), 7- or 14-day trials (03 04 05 10), "cancel from (account/billing) settings" (01 03 05 08 10). A free tier is a business decision the model is making for 6 owners. |
| P7 | **Nav = [one product noun] + Pricing/Plans + Log in**, 3–4 items (Log in boxed on 03 05 09) | 01 03 05 07 09 10 | 6 | **Acceptable convention.** It is what rule 5 asks for and what a buyer checks. Not slop. |
| P8 | **Footer = "© 2026 Brand" on the left, an underlined row (Contact · Privacy · Terms) on the right, on one line** | 01 02 03 04 05 06 07 08 09 | 9 | **Thin convention.** Better than v3's bare line, but the business facts that exist (hours on 06/08/09, docs, status) appear on only 4. Fine for SaaS; weak for a shop or studio (no address, which is a launch constant only). |
| P9 | **Section left edges jitter** (each section indented differently) | 02 04 07 08 09 | 5 | **Slop / visual bug, made by rule 1** ("give sections widths that fit their content"). Agents met it by changing each section's left inset, which reads as misalignment, not composition. |
| P10 | **Long sentence h1 (10–15 words), shaped "[category] that/and [difference clause]"** | 01 (11) 02 (14) 06 (10) 07 (15) | 4 | **Borderline slop.** These are ledes set at h1 size. The "plain category + difference" and "kicker + claim" shapes push agents to put the whole claim in the h1. The short h1s (03, 08, 09) are stronger. |
| P11 | **One typeface for the whole page** | 01 02 03 04 06 08 09 10 | 8 | **Acceptable.** The families differ, so a viewer does not see "same generator", but single-family plus single-weight pages read flat (04, 07, 10). |
| P12 | **Green / lime / chartreuse accent** (neon green, chartreuse pastel, chartreuse field, leaf pastel, mint CTA) | 04 05 06 07 08 | 5 | **Seed artefact** (section 4). Not a model default this time, but it reads as one in the set. |
| P13 | **"Sample …" one-line caption under the demo artifact** | 01 05 08 09 (+07 descriptive) | 4–5 | **Acceptable.** It is the one caption C2 allows. |
| P14 | **Dark or grey ground** | 04 05 07 08 | 4 | **Acceptable** (seed-assigned). Noted only because 08 put a plant shop on near-black. |
| P15 | **LAUNCH constants** SIGNUP_URL / LOGIN_URL / PRIVACY_URL / TERMS_URL / CONTACT or SUPPORT_URL | 10/10 (SIGNUP 8) | 10 | **Invisible to visitors; correct.** The visible labels "Privacy" and "Terms" (10/10) and "Contact support" (03 04 09 10) are conventions. |

**Copy formulas below the 4-page threshold** (still rule breaches, so listed):
- "X, not Y": 01 h2.
- Staccato triple: 03 lede.
- "your first/next [noun]": 05, 08, 10.
- An outline-drawn "photo slot": 02, 06, 08. That is 3/3 of the pages that needed photographs, so it is a 100% convergence within its category.

**Ranked by how badly they give the generator away:** P1 > P3 > P9 > P6 (values) > P10 > P8. P2, P5, P7 and P13 are conventions that serve the visitor; keep them.

---

## 3. Honesty / fabrication audit

| Page | Drafted "owner facts" (data.todo / LAUNCH TODO) | Verdict |
|---|---|---|
| 01 | Free seat limit 5, $6/person, 3 projects, 30-day history, 30 h default capacity, plan-change terms | All **decisions**. OK. |
| 02 | Product names (Guji Natural, Huila Washed, Cerrado Honey, House Espresso), origins, roast levels, tasting notes, $19/$17/$16/$15 per 250 g, roast days, Sunday 23:59 cutoff, Wednesday dispatch, $5 shipping / free over $40, pickup hours, 14-day returns | **Decisions** (the line-up on sale now is an owner decision). OK. The tasting notes and roast-log prose were left untagged (agent admits it). "We only roast what has been ordered" is a process decision; fine if tagged. |
| 03 | $0/$12/$110, document and length limits, 14-day trial | **Decisions**. OK. |
| 04 | Free/Plus, $4.99/$39.99, 7-day trial, history length, plan contents, zone percentages | **Decisions**, plus general knowledge (zones). OK. The plan contents were untagged. |
| 05 | Solo $12 / Plus $24, 14-day trial, currencies and bank-feed limits; **"Data is encrypted in transit and at rest. Card numbers go to the payment processor and never reach Ledgerly servers."** | Prices are OK. The security sentences are **product-behaviour claims about an existing system** (C17 allows describing what it does). But "card numbers never reach our servers" is a PCI-scope assertion. It is tagged, but it should be listed in the hand-off as *verify, not decide*. |
| 06 | **"31 buildings drawn and built"; five projects with names, types, places, years and floor areas (Orchard House, Sutton Hill, 2023, 186 m²; Hallmoor Primary School, 2021, 2,340 m²; Kiln Lane extension 2022; Quay Street Library 2019; Ferry Row studios 2017); two named people (Mara Lindqvist, founding architect; Tomas Reyes, project architect) with bios**; stage durations; 9% fee; hours | **Fabricated history and identity.** The count, projects, places, years, areas, names and bios are true only if they already happened or the people exist. A `todo` tag does not make them honest: a launch reviewer would correct a price, but would not notice that "Hallmoor Primary School" is fiction until a client asks to visit it. The stage durations, 9% fee basis and hours are **decisions**, so OK. |
| 07 | Install command, plans Hobby/Team/Scale $0/$24/$180, limits, regions, preview retention | **Decisions / product spec**. OK. |
| 08 | 4-week cadence, plans $28/$49/$6, dispatch Monday, 3–5 day window, Friday 5 pm cutoff, 7-day damage replacement, mainland US, no shipping in freezing weather, support hours | **Decisions**. OK. Several policies were untagged (agent admits it). |
| 09 | $2.50/$4.90, seats/devices/limits, platform list, **Argon2id + AES-256-GCM**, recovery behaviour, support hours; a **"Security paper"** footer link (SECURITY_DOC_URL) | Prices and limits are **decisions**. The cipher names are a product spec (a decision before launch, a fact after). They are tagged, which is OK, but they need *verify* in the hand-off. The "Security paper" link implies a document exists; it is a constant, so it is acceptable only if the owner has one. The page correctly cut audits, user counts and reviews. |
| 10 | Lesson length, the 1/3/7/21-day schedule, 6 languages and levels (Japanese to N4), Free / $9.99 / $59.99, 7-day trial | **Decisions** (the catalogue on offer). OK. |

**Summary.** 9/10 stayed on the right side. One page (06) fabricated an entire practice history, and it did so *because of the rules*:
- rule 10 calls "owner facts" draftable and lists only commercial examples;
- the seed's "number-led" headline demanded a figure;
- the studio convention asks for "built work" and "who is behind it".

Two smaller problems:
- **Untagged drafts** on 02, 04 and 08.
- **Verify-not-decide claims** (security architecture, compliance) on 05 and 09, which the hand-off should separate from prices.

### Proposed rule: decisions vs history

> **Owner decisions** are what the owner can make true tomorrow by deciding it: prices, plans and their limits, trial, cancel and refund terms, hours, cadence, cutoffs, shipping fees and regions, the products or services on offer now (names, origins, sizes), fee basis, process stages and durations, supported platforms. If missing, draft plausible values in `<data class="todo">`, list them in LAUNCH TODO and name them in the hand-off.
>
> **Owner history and identity** is true only if it already happened or the person exists: past projects and clients, case studies, team names, bios and portraits, the founding year, years in business, counts of work done ("31 buildings", "2,000 orders"), awards, certifications and audits. Never draft these, even marked. Show the shape instead:
> - portfolio: photo slots captioned by **type only** ("Timber-frame house", "School courtyard"), no name, place, year or area;
> - people: **role labels** with a portrait slot ("Founding architect"), no invented name;
> - the real list: one LAUNCH TODO item (`PROJECTS: name, place, year, area, photo for each`);
> - headlines: use a decided figure (fee basis, stage length, price), never a count of past work.
>
> **Verify, don't decide:** claims about how an existing system is built (encryption scheme, where card data goes, compliance scope) may be drafted only as product behaviour, tagged, and listed separately in the hand-off as "confirm with engineering".

---

## 4. Seed quality

| Seed assignment | Page | What happened | Edit |
|---|---|---|---|
| **Swiss white + black + one primary (red, blue or yellow)** + hue **purple-plum** | 10 | The two axes contradict each other. The agent kept plum, so "Swiss" became a plum page with hairlines, and nothing Swiss is left but white. | Strategy text: `"pure white, true black text, the assigned hue at full chroma used big (a band, the h1 block, the CTA), never as a small accent"`. The strategy no longer names hues; the hue axis owns hue. Apply the same rule to every strategy: no strategy description may name a hue. |
| **type poster** (h1 ≥ 9vw, artifact peeks in at the fold) | 03 | At 360 px, rule 3 capped the h1 at 4 lines. On desktop the artifact did *not* peek in, leaving an empty cyan field under the CTA. | `"the h1 fills the top of the first viewport (>= 9vw on desktop; at 360px max 4 lines with the CTA in view); the artifact's top edge must be visible in the first 1280x800 viewport"`. |
| **extreme contrast** (h1 ≥ 6× body) | 05 | Impossible at 360 px with a wide display face; the agent applied it to desktop only. | `"h1 >= 6x body on desktop; at 360px h1 >= 2.5x body, one dramatic jump in scale per page"`. |
| **one big number** (larger than the h1) | 09 | A price larger than the h1 on a password manager pushes the category below a magenta figure, and the visitor's first question is "is it safe", not "$2.50". | Limit the categories to `["finance", "delivery", "fitness"]`, and change the text to: `"a single figure the visitor's first question is about (price for delivery, time or money for finance, a workout stat) set larger than the h1; the h1 still names the category and sits above it on mobile"`. Remove "security", "devtool" and "saas". |
| **number-led** headline | 06 | Demanded a figure. The only "true" figures for a studio are history, so the agent invented "31 buildings". | `"a figure the owner decides or the product produces (price, time, size, schedule) first; never a count of past work, customers or years"`. |
| **soft uniform** / **elevation only** ("no borders") vs 3:1 control boundaries | 04, 07, 08 | Agents were unsure whether inputs may have borders; 08 on a dark ground had no guidance. 04 ended at a 3.54 boundary in a narrow window. | Append to both: `"; 'no borders' applies to containers: inputs, selects and secondary buttons keep a 3:1 boundary (a line, or a fill that is 3:1 against its ground)"`. |
| **alternating light/dark bands** vs C16 "only one inverted band" | 02 | 4 dark bands; conflicts.md contradicts the seed. | Fix C16 (change 11). |
| **Hue sectors**: yellow-lime 95–115, leaf green 130–150, olive-chartreuse 70–95 | 04, 05, 06, 07, 08 | 3 of 10 sectors (30%) are yellow-green, beyond the script's own ">30% → edit" rule. 5/10 pages got a green, lime or chartreuse accent (06 olive-chartreuse field, 05 olive-chartreuse pastel, 04 leaf green, 07 leaf-green pastel, 08 mint as the duotone partner). | Merge into **one** sector `("green / lime (high chroma)", 95, 150)` and drop olive-chartreuse. Add two sectors the corpus has never used, `("deep blue-green / petrol, low L", 200, 215)` and `("achromatic: black, white, grey + the photo", None)`, for 9 sectors with at most one per hue family. Also forbid `near-black + pastel` with any hue 95–160 (that is green-on-black, the v2 dark), since the checker rejects it anyway (07). |
| **Hue sectors defined loosely** ("OKLCH-ish degrees") | 02, 03 | 02's seed cobalt (#3a62ff, HSL 225–250) is flagged by the checker's indigo band (OKLCH 262–300). 03's full-chroma cyan field lands on the Tailwind cyan swatch. | State that sectors are **OKLCH hue**, print one reference hex per sector in the seed output, and have the seed skip a strategy/hue pair the checker would flag (saturated field + cyan → use L ≤ 70% or a different strategy). Seed and checker must share one hue table. |
| **sticky index sidebar** | 08 | Pushed the h1 to 5 words (fine), but the index became grey chips that read as tags. | `"…a sticky left column (name, h1, CTA, a plain-text section index styled as links)…"`. |
| **fixed half + scrolling half** | 06 | The empty fixed half dominates a full-page view; workable live. | Keep it. Add `"the fixed half also carries one live element (contact, hours, the current project's caption)"`. |
| **rounded sans** shortlist | 04, 10 | Both took Baloo 2 (the shortlist is 5 of 6 fonts, so the shortlist hardly varies). | Print **one** assigned font plus one alternate, not five. |
| **kicker + claim**, **plain category + difference** | 01, 02, 07, 08 | Produced the long "[category] that [clause]" h1s (P10). | Add to both: `"h1 <= 9 words; the difference may move to the lede"`. |

**Seed ↔ checker contradictions** reported by the agents, for the scripts editor:
- the static-year WARN on 9/10 pages, while C10 *requires* a static year;
- the "artifact-first" WARN on a sidebar hero (08);
- the shop "no product photo" WARN on an app (04);
- the "app: no phone frame" WARN on a security product (09);
- "studio" detected from a plan named "Studio" (05);
- "oxblood" and "mono-voice" matched inside class and token names (05, 09);
- neutral grey #6b6b6b flagged as Tailwind slate (04);
- the sage detector firing on light yellow cream (06);
- ruled rows counting real tables (06, 09, 10);
- the v1-template match driven only by seed-assigned values (02, 09).

Agents kept 0 FAIL by renaming classes. That is harmless, but it is checker noise that teaches agents to ignore WARNs.

---

## 5. Prioritized change list (exact text)

SKILL.md grows by about 10 lines net. Most of the changes replace existing text.

**1. SKILL.md rule 10, replace the "Owner facts" bullet** (fixes the 06 fabrication):
```
   - **Owner decisions** (prices, plans and limits, trial/cancel/refund terms, hours, cadence, cutoffs, shipping terms, the products or services on offer now, fee basis, process durations): if missing, draft plausible values. Wrap each in `<data class="todo">…</data>`, list it in `<!-- LAUNCH TODO -->`, and name it in your hand-off. Test: the owner could make it true tomorrow by deciding it.
   - **Owner history and identity** (past projects, clients, team names and bios, founding year, counts of work done, years in business, awards, certifications): never draft, even marked. Caption portfolio photo slots by type only ("Timber-frame house"), show people by role ("Founding architect"), and put the real list in LAUNCH TODO. [v4: one page invented 31 buildings, five dated projects and two named people]
```

**2. SKILL.md rule 10, append to the "Third-party claims" bullet:**
```
 Claims about how an existing system is built (encryption scheme, where card data goes, compliance scope) are product behaviour: write them only if supplied or tagged, and list them in the hand-off under "confirm", apart from prices.
```

**3. SKILL.md rule 4, replace the line "At most one secondary action: underlined body text on its own line, naming the evidence it leads to."** (P1):
```
   - No secondary action in the hero unless the hero artifact is not visible at 1280×800. [v4: 8/10 put the same underlined noun-phrase link under the CTA]
```
Also in **conflicts.md C4**, replace from "Default to no secondary action." to the end with:
```
Default to no secondary action. Add one only if the hero artifact is not visible in the first 1280×800 viewport. Do not write it as a noun phrase on its own line by reflex: in v4 that exact slot appeared on 8/10 pages.
```

**4. SKILL.md, add as rule 7** (after rule 6, in the empty 7–9 range) (P3):
```
7. The page may repeat the conversion at the end, but not as an imperative h2 over the hero button with the same label [v4 7/10]. The closing block states what happens after the action (what arrives, when, what it costs), and its heading states that fact.
```

**5. SKILL.md rule 1, replace** (P9):
```
1. Do not use one wrapper width for every section. Use `<main>`. Sections may differ in width, but their left edges sit on at most two lines (the text edge, or full bleed). A different inset per section reads as misalignment. [v1 10 one wrapper; v4 5 jittering edges]
```

**6. SKILL.md rule 20, append** (P10):
```
 Keep it to 9 words or fewer; the difference can move to the lede. [v4: 4/10 h1s were 10–15-word "[category] that [clause]" sentences]
```

**7. SKILL.md rule 22, replace the bullet "[Verb] your first [noun]";** (01, 03, 05, 08, 10):
```
    - "[Verb] your first/next [noun]", "cancel from settings" as the only terms;
```
and append to rule 21: ` [v4: "X, not Y" h2 on 01; "Accept it, reject it, keep writing." on 03]`.

**8. SKILL.md rule 23, replace** (02 lifted v2-02's closing line):
```
23. Do not reuse any label, number or phrase from this skill or from any page in `research/`. Examples show shape only. [v4-02 reused v2-02's "Come smell the roaster"]
```

**9. conflicts.md C3, replace the last sentence** (02, 06, 08 outline art):
```
Photo gaps become art-directed photo slots (`<figure class="photo-slot" data-todo="…">`): a flat tint from the palette at the photo's aspect ratio, with the real caption beneath. No outline drawing, clip-art or icon of the object inside the slot; a drawn stand-in reads as the product image and looks worse than an empty frame. On a shop, a product's name, price and action take more space than its slot. [v4: 3/3 photo pages drew outlines]
```

**10. conflicts.md, add C20** (edge language vs boundaries; seed vs viewport):
```
**C20. A seed axis vs rule 3 or rule 16.** (v4: 03, 04, 05, 08)
Resolution: these are not overrides. "No borders" (soft uniform, elevation only) applies to containers; inputs, selects and secondary buttons keep a 3:1 boundary (a line, or a fill 3:1 against its ground). Scale and hero specs are desktop specs: at 360px the h1 takes at most 4 lines and the CTA stays in view. "Type poster" and "one big number" still need the artifact's top edge in the first 1280×800 viewport, and the h1 still names the category.
```

**11. conflicts.md C16, replace the last sentence:**
```
Only one inverted band per page, unless the seed assigned "alternating light/dark bands" or "horizontal strata".
```

**12. brief_seed.py pools** (for the scripts editor; text only):
- `HEADLINE_SHAPES` "number-led" → `"a figure the owner decides or the product produces (price, time, size, schedule) first; never a count of past work, customers or years"`.
- `HEADLINE_SHAPES` "plain category + difference" and "kicker + claim": append `"; h1 <= 9 words, the difference may move to the lede"`.
- `COMPOSITIONS` "one big number" → categories `["finance", "delivery", "fitness"]`; description `"a figure the visitor's first question is about, larger than the h1; the h1 names the category and sits above it on mobile"`.
- `COMPOSITIONS` "type poster" → `"the h1 fills the top of the first viewport (>= 9vw desktop; <= 4 lines at 360px with the CTA in view); the artifact's top edge is visible in the first 1280x800 viewport"`.
- `DENSITY` "extreme contrast" → `"h1 >= 6x body on desktop, >= 2.5x at 360px; everything else small"`.
- `COLOR_STRATEGIES` "Swiss white + black + one primary" → `"pure white, true black text, the assigned hue at full chroma used big (a band, the h1 block, the CTA), never as a small accent"`. No strategy description may name a hue.
- `EDGES` "soft uniform" and "elevation only": append `"; controls keep a 3:1 boundary"`.

**13. brief_seed.py hue table** (P12): replace the three yellow-green sectors with `("green / lime", 95, 150)`, and add `("petrol / deep blue-green", 200, 215)` and `("achromatic + photo", None)`. Declare all sectors as OKLCH hue and print a reference hex. Skip `near-black + pastel` × hue 95–160 and `saturated field` × cyan at L > 70%. Seed and checker read one shared hue table.

**14. brief_seed.py output:** print one assigned font plus one alternate instead of a 5-font shortlist (04 and 10 both took Baloo 2).

**15. SKILL.md intro, replace the v3 bullet list with a tighter v3 line plus one v4 line** (keeps the history current without growing):
```
- **v3, bans + "cross out your first idea".** Every page passed the checker and converged again: one condensed sans (8/10), an orange CTA (9/10), artifact-first heroes, toy calculators instead of a conversion, no prices or photos. Pages got stranger and worse at selling.
- **v4, seed + conventions.** Every page sold something with its h1 and CTA on the first mobile screen, and colour and type varied. Structure converged: h1, lede, CTA, an underlined link (8/10), a plans table with a $0 tier (6/10), an imperative closing h2 over the same button (7/10). One page invented a studio's history.
```
