# v4 feedback (skill v3: seed + conventions + new checker)

## 03 Nimbus — 0F/4W; contrast min 7.55; render 0/0. No overrides.
- WARNs kept: Tailwind cyan-500 nudge (#00bdf2) — seed assigned full-chroma cyan field, any such cyan is near the swatch → SEED vs CHECKER conflict. Oxblood token = tracked-change deletion red (functional). Hardcoded year (allowed by C10 → checker contradicts conflicts.md). Weight 900 h1 (seed's type-poster needs it).
- Conventions: tracked-change paragraph + margin notes; declined-requests transcript; pricing table (drafted todo: $0/$12/$110, 14-day trial); sign-up form → SIGNUP_URL. Constants: SIGNUP/LOGIN/SUPPORT/PRIVACY/TERMS_URL.
- Unclear: rule 3 vs type-poster (h1 ≥9vw + CTA in 360x740) — capped h1 at 4 lines. Owner fact vs product claim. No way to record a reasoned WARN in the file.

## 07 Shipyard — 0F/1W (hardcoded year, C10-allowed → checker vs conflicts.md again). contrast 83/83 resolved. render 0/0. No overrides.
- Fira Sans + Fira Mono in code only; long-read column with breakout terminal; near-black + leaf-green pastel #a6e7b3; dense; elevation only; kicker+claim.
- First run: green-black ground WARN (seed's leaf-green hue + near-black → checker ban) → SEED vs CHECKER conflict; moved to warm black #121110. Added SVG favicon.
- Conventions: terminal hero, install cmd, Docs nav, free tier, status/changelog. Todo: install cmd, plans Hobby/Team/Scale $0/$24/$180, etc. Constants SIGNUP/LOGIN/DOCS/CHANGELOG/STATUS/CONTACT/TERMS/PRIVACY.
- Unclear: how much hue tint allowed on near-black. "No form >2 sections": do two code panes count as one form? Do numbered step prefixes count as a label style?

## 08 Greenleaf — 0F/2W; contrast clean; render 0/0. No overrides.
- WARNs: hardcoded year (static+JS per C10; checker can't tell) → CHECKER FP. Artifact-first hero WARN but page is sidebar h1 → CHECKER FP.
- Source Sans 3; sticky index sidebar; plum + leaf-green duotone dark; airy; soft 12px no borders; kicker+claim.
- 3 photo-slots (plant 4:5, box 1:1, care card 1:1) with SVG placeholders. Todo: plans $28/$49/$6, cadence, timeline, cutoff, region, hours. Constants SIGNUP/CONTACT/PRIVACY/TERMS/OG_IMAGE.
- Untagged unconfirmed POLICY copy: no shipping in freezing weather, replacement at no cost, nothing charged on skip, arrive watered → policies are owner facts but not tagged.
- Unclear: sticky sidebar vs h1 ≥7vw (shrunk headline to 5 words; sticky only ≥860px tall). Edge "no borders, tinted fills" vs 3:1 control boundary — no guidance on dark ground. Static-year + artifact-first WARNs unclearable without nudging.

## 01 Taskflow — 0F/1W (hardcoded year, C10 → FP). render 0/0. No overrides.
- Atkinson Hyperlegible; demo-in-hero 3fr/2fr artifact left; tonal analogous red, light; crimson CTA ~354°; 28px panels / 12px buttons; kicker+claim.
- Nav: Board, Pricing, Log in. Primary CTA → SIGNUP_URL "Create a team workspace". Demo uses roles. Todo: 5 free seats, $6/person, 3 projects, 30-day history, 30h capacity, plan-change terms.
- Unclear: list-of-three / "finding" headings subjective; demo-in-hero column ratios — only 5/7 and 1.1/.9 banned.

## 05 Ledgerly — 0F/1W (hardcoded year FP). contrast 106/106. render 0/0. No overrides.
- Unbounded h1/h2 + Hanken Grotesk; h1/lede/CTA then product UI at 80% overlapping next section; near-black olive + chartreuse pastel #dbe6a6; 3px outlines + 1 offset shadow; imperative h1.
- Checker FPs forced renames: "studio" category detector on a plan name "Studio"; "oxblood" detector on token name containing "margin". 
- Untagged owner-supplied: plan feature split.
- Unclear: seed's "extreme contrast" (h1 ≥6x body) vs wide display face at 360px → fluid clamp only desktop.

## 02 Brewly — 0F/4W; contrast min 4.80; render 0/0. No overrides.
- WARNs: Tailwind ΔE + indigo/violet on seed-assigned cobalt (#3a62ff) → SEED (HSL 225-250) vs CHECKER (OKLCH 262-300) hue mismatch. v1-template match 6/9 FP from hue. Hardcoded year FP.
- Bricolage Grotesque; long-read column; alternating cobalt bands; pill + square; plain category+difference.
- Shop conventions: 4 products w/ prices ($19/$17/$16/$15, 250g), photo-slots w/ briefs (hero 16:9, 4 bags 4:5, counter), roast log, brew table, terms. Constants SHOP/CART/CONTACT_EMAIL/MAPS/PRIVACY/TERMS.
- Untagged draft copy: origins, roast levels, tasting notes, roast-log prose.
- Unclear: C16 "only one inverted band" vs seed's alternating bands. data.todo inside h1/table cells awkward. Rule 6 legal links as constants vs C11 "show none without pages". Visible contact facts with no placeholder → used link text "Email the roastery".

## 04 FitPulse — 0F/3W; contrast btn boundary 3.54; render 0/0. No overrides.
- WARNs: #6b6b6b neutral grey flagged as "nudged Tailwind slate" → FP for neutral greys. "[shop] no product photo" on an APP → category FP. Hardcoded year FP.
- Baloo 2; product-UI stage w/ 3 CSS phones; neon on mid-grey, leaf green; airy; soft 12px; imperative h1. Constants DOWNLOAD/APP_STORE/PLAY_STORE/... Todo prices $4.99/$39.99, zones.
- Untagged plan contents. Demo phone numbers uncaptioned.
- Unclear: mid-grey + neon + 3:1 boundary narrow window; "soft uniform radius on everything" vs phone mockups. Python has no Playwright (render used node path).

## 10 Lingo Loop — 0F/1W; contrast min 6.67; render 0/0. No overrides.
- WARN: ruled rows — seed assigned hairline edges, checker counts raw 1px borders → SEED vs CHECKER conflict.
- Baloo 2 (2nd Baloo 2 — FitPulse also); centred stack + 3-phone strip; Swiss white+black+plum primary #a8138e; flat; hairline; imperative.
- Unclear: Swiss "one primary (red/blue/yellow)" vs assigned plum hue → seed axes contradict. 

## 09 Vaultix — 0F/4W; contrast 131/131; render 0/0. No overrides.
- WARNs: "[app] no phone frame" (category detector inferred app from security brief?) ; hardcoded year FP; ruled rows (real tables); v1 template 5/9 (from seed-assigned values) FP.
- Familjen Grotesk; one big number $2.50 > h1; duotone cyan #00637a CTA + rose #b3123f; dense; 28/12 radius; "Zero-knowledge password vault".
- Checker FP: mono-voice regex matched "tag" inside class "stage" → renamed class.
- Untagged product behaviour copy listed. Cut: audits, user counts, reviews, integrations.
- Unclear: big number > h1 vs first-viewport rule; dl/table count as ruled form?; duotone: which hue is CTA?

## 06 Studio Mara — 0F/2W; contrast both themes, min 3.30 inputs dark; render 0/0. Looked at screenshots; fixed mobile table bug. No overrides.
- WARNs: hardcoded year FP; ruled rows (real table + timeline + footer).
- Jost; fixed half + scrolling 4 photo slots; two-tone chartreuse hero #d3df45 / pale olive (light) / dark olive (dark) with toggle; editorial; pill+square; number-led "31 buildings drawn and built by one independent architecture studio".
- PROBLEM: drafted as todo "owner facts": 31 buildings, 5 named projects w/ places/years/areas, 2 named people (Mara Lindqvist, Tomas Reyes), 9% fee. → invented HISTORY and PEOPLE; rule must separate owner decisions (prices/terms/hours, draftable) from owner history (past work, clients, team names, counts — not draftable).
- Checker: sage-ground detector triggers on light yellow-cream hue ≥95 → had to saturate. Ruled-row count can't separate tables from decoration. Skip-link only passes for #main/#content.
- Unclear: category convention "contact with real address" vs no invented contact + no visible placeholders.
