# Rule conflicts and their resolutions

These came from the feedback of 10 agents that followed this skill (v2 run). Where two rules seem to pull against each other, apply the resolution here. The page numbers say which v2 pages raised each conflict.

**C1. "The primary CTA is the real conversion" vs a pre-launch product with no URLs.** (v2: 01,03–09; v3: all 10, which then built toy calculators as the CTA)
Resolution: the primary CTA is still the category's real action (sign up, buy, book, install, download). Point it to **one launch constant**: `<form action="SIGNUP_URL">` or `<a data-href="SIGNUP_URL" href="SIGNUP_URL">`, declared once in `<!-- LAUNCH TODO: SIGNUP_URL = … -->`. Name the constant in the hand-off. On-page tools (calculator, picker, paste box) are fine as *secondary proof*, never as the only conversion. Never invent a domain (`.example`, `.invalid`, a plausible `.app`) and never show "not connected" text on the page.

**C2. "No invented proof" vs "the page needs content".** (v2: 01,02,04,05,10; v3: 03,05,07,09,10)
Resolution: sort every missing fact by **who must supply it**.
- **Owner facts** (prices, plans, product names, trial terms, hours, shipping terms) may be **drafted** as plausible values, wrapped in `<data class="todo">…</data>`, listed in LAUNCH TODO and named in the hand-off. A shop without prices is worse than a marked draft price.
- **Third-party claims** (quotes, ratings, user counts, customer logos, press, audits, awards) are never drafted. Cut the section.
- **Contact facts** (address, phone, email, URLs) are never drafted. Use launch constants.
- **Demo data inside the product artifact** (tasks, invoice lines, terminal output) may be invented. Use roles or objects rather than fake people, with at most one short caption.

**C3. Placeholders and honesty notes make the page look unfinished.** (v2: 38 placeholders on 8 pages; v3: 7 pages said "not connected")
Resolution: no visible `[… NEEDED]`, "prototype", "pre-launch", "nothing is sent" or "not connected" text. The hand-off message and the LAUNCH TODO comment carry that information. Photo gaps become art-directed photo slots (`<figure class="photo-slot" data-todo="…">`): a flat tint from the palette at the photo's aspect ratio, with the real caption beneath. Do not put an outline drawing, clip-art or an icon of the object inside the slot; a drawn stand-in reads as the product image and looks worse than an empty frame. On a shop, a product's name, price and action take more space than its slot. [v4: all 3 photo pages drew outlines]

**C4. Text link vs ghost button; what a "specific secondary link" is.** (02,05,10)
Resolution: a ghost button is any secondary action with a border, a background, or padding over 0.25em, or one placed in the same flex row as the primary. A text link is inline in running text or on its own line below, uses the body font at body size, and carries only an underline. Default to no secondary action in the hero. Add one only when the visitor's first question is answered lower on the page *and* the hero cannot answer it. Do not add one by reflex: in v4 the same underlined noun-phrase link under the CTA appeared on 8/10 pages.

**C5. What counts as a "list of three".** (01,03)
Resolution: banned means three or more parallel items used *rhetorically* in one sentence, headline or button row: series of verbs, adjectives or nouns ("Plan, assign, ship"), staccato fragments ("Push. Build. Float."), or repeated negations ("no X, no Y, no Z"). Data is allowed (tasting notes, table rows, three real plans). Test: if the sentence stays equally true with two or four items, the count is decoration, so rewrite it. The rule applies to h1, h2, lead and CTA rows, not only the lead. A section with three rows is fine if there really are three things.

**C6. What a deliberate dark theme is; dark-only vs auto swap.** (01,09)
Resolution: one finished theme beats two half-made ones.
- *Single theme* is allowed when the seed assigns it or the colour strategy implies it. Set `<meta name="color-scheme" content="light">` and say why in the brief.
- *Two themes* count as deliberate only if (1) a visible toggle exists and persists, (2) at least one element is *not* a token swap (the artifact keeps its material, or the accent changes role), and (3) every text pair and button boundary was checked in both.
- Never ship `[data-theme]` selectors without a toggle. 5/10 did.

**C7. Material metaphors vs the product itself.** (v2: stationery on 7/10; v3: pegboard, container yard, concrete or safe-deposit steel on 8/10)
Resolution: there is no material requirement any more. For screen software, the material *is* the product UI. A metaphor is allowed only if a stranger in this category would read it without explanation, and it never replaces the product (terminal, phone screen, product photo, built work). Colour comes from the seed's strategy and hue family.

**C8. How far tokens must differ from `--bg/--card`.** (08)
Resolution: renaming is not the test, structure is. Allowed: at most one "surface" token that is a small lightness shift of the page, and it is used for one component type at most. Token names describe the product role (`--receipt`, `--hull`, `--zone-3`), not ink/paper metaphors (`--ink`, `--ink-soft`, `--rule`, `--paper-deep`).

**C9. OG image in a single file.** (01,07,10)
Resolution: `og:image` must be an absolute https URL that exists. With no host, omit it and add it to the LAUNCH TODO comment. `data:` URIs and `.example` URLs are not allowed. `og:title`/`og:description` are always required.

**C10. "Generate the year" leaves it blank without JS.** (05)
Resolution: write the current year as static text and let JS update it: `<span id="y">2026</span>`. The v1 ban was on a footer made of *only* "© 2026 Brand. All rights reserved.", not on a static year.

**C11. Legal links with no destination.** (05,01,02,04)
Resolution: legal links point to launch constants (`PRIVACY_URL`, `TERMS_URL`) listed in LAUNCH TODO, because a business needs those pages before launch. `mailto:?subject=Privacy` is not a privacy policy. For a visible contact fact you do not have (address, phone), use a link labelled by its purpose ("Studio address and directions" → `MAP_URL`), and never invent the fact itself.

**C12. Contrast and 360px "checked by eye", no tool available.** (01,02,05,06,08,09)
Resolution: ship a runnable check. Extend `slop_check.py` to resolve dark-theme tokens (dark tokens are resolved) and add `--contrast-table`, which prints every resolved text/bg pair for both themes. The skill should require running it and pasting the FAIL lines, which must be empty.

**C13. "Real screenshot" vs CSS mock.** (04)
Resolution: a CSS/SVG artifact is "real" if it shows a specific state the product produces: a number, a refusal, a failure, a decision. It is generic if it would still make sense with the product name changed.

**C14. Ruled rows becoming the new default.** (04, confirmed 10/10)
Resolution: no single content form (ruled rows, table, dl, cards) may be used for more than 2 sections on a page. Each section's form is chosen from its data shape (see dont-list.md, Components 1).

**C15. Studio Mara is praised, but the swap test says don't copy it.** (06; and 6/10 copied its logo and h1)
Resolution: remove the outlier's concrete traits from SKILL.md (done in SKILL.md). Describe *why* it worked: every choice came from drawing-sheet conventions. Do not describe *what* it did.

**C16. Does a mid-tone section background count as a card?** (01)
Resolution: no. A card is a bounded box repeated three or more times as siblings. A full-bleed band is a section. Only one inverted band per page, unless the seed assigned "alternating light/dark bands" or "horizontal strata".

**C17. Product-behaviour copy vs "invented claims".** (v3: 03,05,07,09)
Resolution: describing what the product **does** ("rolls back when the health check fails", "encrypts on your device before upload") is product copy, not a claim, so write it plainly. Describing how **well** it does it compared with others, or what **others say** about it ("10× faster", "trusted by 2,000 teams", "audited by…"), is a third-party claim. Do not write those unless they were supplied.

**C18. The seed assigns something that fights the category.** (anticipated, e.g. "number-led" headline for an architect)
Resolution: use one of your two overrides, with one sentence naming the visitor need. An override may not land on a converged value (SKILL.md rule 15). If more than two axes fight the brief, run `--salt 1` and `--salt 2` and take the direction that fits best, rather than overriding everything.

**C19. "Don't nudge values to clear the checker".** (v3: lede 34→37/38/41rem, `#ebebe8`→`#eeece9`, h1 weight 400→700)
Resolution: a WARN describes a shape. Change the shape (a different composition, ground or type class), or keep the WARN and write the reason in a comment. Moving a number a few units past a threshold is a fail of the self-check, even if the checker is quiet.

**C20. A seed axis vs rule 3 (first mobile screen) or rule 16 (boundaries).** (v4: 03, 04, 05, 08, 09)
Resolution: these are not overrides.
- "No borders" edge languages (soft uniform, elevation only) apply to containers. Inputs, selects and secondary buttons keep a 3:1 boundary, either a line or a fill that is 3:1 against its ground.
- Scale and hero specs are desktop specs. At 360px the h1 takes at most 4 lines and the CTA stays in view.
- "Type poster" and "one big number" still need the artifact's top edge in the first 1280×800 viewport, and the h1 must still name the category.

**C21. Keeping a WARN with a reason.** (v4: 9/10 pages kept WARNs with reasons, but only in their hand-off message)
Resolution: write the reason in the page as `<!-- slop-ok: <rule-key> <reason> -->`, using the rule key the checker prints. The checker then lists that WARN as kept-with-reason. A FAIL can never be kept. The reason must name the visitor need or the seed axis; "intentional" is not a reason.

