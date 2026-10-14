# Rule conflicts and their resolutions

These came from the feedback of 10 agents that followed this skill (v2 run). Where two rules seem to pull against each other, apply the resolution here. The page numbers say which v2 pages raised each conflict.

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
Resolution: the banned palettes are banned as *unmotivated defaults*. A material may land near one if the brief names the physical object and the sampled hex. But the material must come from where the visitor *uses* the product or what they *receive* (gym floor, the coffee bag that arrives, a server log, the building site). It must not come from stationery about the product. See SKILL.md step 1 (material reference).

**C8. How far tokens must differ from `--bg/--card`.** (08)
Resolution: renaming is not the test, structure is. Allowed: at most one "surface" token that is a small lightness shift of the page, and it is used for one component type at most. Token names describe the product role (`--receipt`, `--hull`, `--zone-3`), not ink/paper metaphors (`--ink`, `--ink-soft`, `--rule`, `--paper-deep`).

**C9. OG image in a single file.** (01,07,10)
Resolution: `og:image` must be an absolute https URL that exists. With no host, omit it and add it to the LAUNCH TODO comment. `data:` URIs and `.example` URLs are not allowed. `og:title`/`og:description` are always required.

**C10. "Generate the year" leaves it blank without JS.** (05)
Resolution: write the current year as static text and let JS update it: `<span id="y">2026</span>`. The v1 ban was on a footer made of *only* "© 2026 Brand. All rights reserved.", not on a static year.

**C11. Legal links with no destination.** (05,01,02,04)
Resolution: if there are no legal pages, show no legal links and list them in LAUNCH TODO. `mailto:?subject=Privacy` is not a privacy policy.

**C12. Contrast and 360px "checked by eye", no tool available.** (01,02,05,06,08,09)
Resolution: ship a runnable check. Extend `slop_check.py` to resolve dark-theme tokens (dark tokens are resolved) and add `--contrast-table`, which prints every resolved text/bg pair for both themes. The skill should require running it and pasting the FAIL lines, which must be empty.

**C13. "Real screenshot" vs CSS mock.** (04)
Resolution: a CSS/SVG artifact is "real" if it shows a specific state the product produces: a number, a refusal, a failure, a decision. It is generic if it would still make sense with the product name changed.

**C14. Ruled rows becoming the new default.** (04, confirmed 10/10)
Resolution: no single content form (ruled rows, table, dl, cards) may be used for more than 2 sections on a page. Each section's form is chosen from its data shape (see dont-list.md, Components 1).

**C15. Studio Mara is praised, but the swap test says don't copy it.** (06; and 6/10 copied its logo and h1)
Resolution: remove the outlier's concrete traits from SKILL.md (done in SKILL.md). Describe *why* it worked: every choice came from drawing-sheet conventions. Do not describe *what* it did.

**C16. Does a mid-tone section background count as a card?** (01)
Resolution: no. A card is a bounded box repeated three or more times as siblings. A full-bleed band is a section. Only one inverted band per page (see dont-list.md).
