---
name: anti-ai-slop
description: Prevents generic "AI slop" frontend output. Use whenever building or restyling a landing page, marketing site, homepage, hero section, or any user-facing web UI (HTML/CSS, React, Tailwind, Vue, etc.), and when reviewing such UI for a templated, machine-made look. Gives a seeded design direction (scripts/brief_seed.py), category conventions a visitor needs, frequency-ranked DO NOT lists from three measured runs, a static checker, and a pre-ship checklist.
---

# Anti AI Slop (frontend)

Slop is an **unconsidered default**: a choice that nothing about this product or visitor informed. A default that serves this visitor (prices on a shop, a terminal on a deploy tool, a phone screen on an app, photos for an architect) is **not** slop. Removing it makes the page worse.

Three measured runs (same 10 briefs; details in `research/`):
- **v1, no skill.** One template on all 10 pages: a 1040px `.wrap`, a `minmax(240px,1fr)` card grid, system-ui, indigo, solid + ghost buttons, "Ready to…?". Clear and complete, but interchangeable, with invented stats and quotes.
- **v2, ban list.** The "stationery editorial" template: sage paper (8/10), IBM Plex Mono (8/10), an italic `<em>` in a serif h1 (8/10), ruled rows (10/10), 38 `[NEEDED]` placeholders.
- **v3, bans + "cross out your first idea".** Every page passed the checker and the pages converged again:
  - Barlow Semi Condensed or condensed Archivo (8/10);
  - an orange/amber CTA (9/10);
  - the artifact first with the h1 under it as a caption (7/10);
  - a single theme, a one-line footer and a toy calculator as the "conversion" (10/10);
  - no prices, photos or real CTA on any page;
  - the CTA below the fold on mobile (7/10).
  Pages got stranger and worse at selling.

**Lessons**
1. A ban moves the mode; it does not remove it. "Avoid your first idea" picks the model's *second* idea, and every agent shares it.
2. Any example in this skill becomes the next default. This file therefore names no fonts, palettes or layouts to use.
3. Divergence must come from **outside the model** (a seed). Conventions must come from **what the visitor needs** (a lookup). Neither should come from taste.

## Workflow

### 1. Get the seed (required, before any design reasoning)
```bash
python3 .claude/skills/anti-ai-slop/scripts/brief_seed.py "<Brand> - <one-line brief>"
```
Paste its output into your reasoning. It assigns: typeface class and shortlist, hero composition, colour strategy, hue family and theme, scale profile, edge language and headline shape. It also lists the **category conventions**.
- Use every axis as assigned.
- You may override **at most two** axes. Each override needs one sentence naming a visitor need or category convention ("buyers of architecture need large photographs, so full-bleed image beats long-read column"). "Looks better" or "fits the vibe" is not a reason.
- An override may not land on a converged value (see rule 15).
- Want options? Run `--salt 1` and `--salt 2`, then pick by visitor fit.

### 2. Product brief (in your reasoning, not in the shipped file)
- **Visitor and their first question.** Answer that question in the h1 and lede.
- **Category conventions.** Take the list from the seed. Each item must appear on the page. These are the defaults that are right.
- **Hero artifact.** The product itself in a specific state: the real UI, terminal, phone screen, product photo or built work. Use a metaphor only if a stranger would read it without explanation. A metaphor never replaces the product.
- **Sections.** Order them by the visitor's questions. Name each section's data shape (sequence, comparison, single figure, gallery, plans, conversation) and choose the form from it. **No form may be used in more than two sections.**
- **Facts.** Sort what the brief lacks into three kinds (rule 10).

### 3. Build: hard rules
Bracketed numbers are pages out of 10 in [v1; v2; v3].

**Structure and conversion**
1. Do not use one wrapper width or one gutter for every section. Use `<main>`, and give sections widths that fit their content. [10; 8; —]
2. Do not use the `auto-fit minmax(240px,1fr)` grid of icon + h3 + muted line, or equal cards for everything. [10; 0; 0]
3. **First mobile viewport (360×740)** must contain an h1 that lets a stranger name the category, plus the primary CTA. An artifact-first hero is allowed only if this still holds. [—; —; CTA missing on 7]
4. **Primary CTA = the category's real conversion** (sign up, buy, book, install, download). Name the action and its object.
   - It points to one launch constant: a form `action="SIGNUP_URL"`, or `data-href="SIGNUP_URL"`, declared once in the LAUNCH TODO comment.
   - On-page tools (a calculator, a picker, a live demo) are welcome as *proof*. They are never the only conversion. [v3: 9 toy CTAs, 0 real]
   - At most one secondary action: underlined body text on its own line, naming the evidence it leads to.
5. The nav links to destinations this buyer checks (Pricing, Docs, Shop, Work, Log in), or to in-page sections with plain noun labels. No phrase-labels ("A request it turns down"). The nav must not wrap word by word at 360px. [v3: 4 phrase navs; 6 bad wraps]
6. The footer gives a contact route, legal links (as launch constants) and the real facts that exist. Not just "© Brand"; not a 4-column grid of placeholders. [9; 8; 10 one-liners]

**Facts and honesty**

10. Facts fall into three kinds:
   - **Owner facts** (prices, plans, trial terms, product names, hours, shipping terms): if missing, draft plausible values. Wrap each in `<data class="todo">…</data>`, list it in `<!-- LAUNCH TODO -->`, and name it in your hand-off message. A shop without prices is worse than a marked draft price.
   - **Third-party claims** (quotes, ratings, user counts, customer logos, press, audits): never invent them. Cut the section.
   - **Contact facts** (address, phone, email, URLs): never invent them; use launch constants. No `.example`, `.invalid`, plausible `.app` domains, `href="#"` or fake `tel:`.
11. No visible "prototype / not connected / nothing is sent / pre-launch / [… NEEDED]" text. Honesty goes in the hand-off and in LAUNCH TODO. Demo data inside an artifact gets **one** short caption at most. [v2: 38 placeholders; v3: 7 pages with "not connected"]

**Visual (each was a measured template; ban the shape, not the number)**

12. No reflex typography:
    - system-ui only, or an unchosen family;
    - the italic or coloured `<em>` fragment in the h1;
    - tracked-uppercase micro-labels as the page's voice (at most one label style, used twice);
    - mono outside code, terminals or aligned figures. [10; 8/10/8; 0/0/0]
13. No generic or renamed token sets. Seven slots (ground, ground-2, text, text-quiet, accent, on-accent, line) renamed `--bg/--card/--fg/--muted…` or `--ink/--paper/--rule…` or `--wall/--wall-deep/--tool-edge…` are the same template. Name tokens for their product role, and use different structures where the product has different surfaces. [10; 9; 10]
14. No stacked skeuomorphism (rotation + stamp + offset shadow + ruled gradient + clip-path: at most one). No asymmetric "material" radius gimmicks. [—; 4; 3]
15. **Converged values: never use these without a seed override and a product reason.**
    - **Fonts:** Inter, Space Grotesk, Newsreader, IBM Plex Sans/Mono, JetBrains Mono, Barlow (Semi Condensed), Archivo, Fraunces, Bitter, Zilla Slab, Roboto Slab, Poppins, Montserrat, DM Sans, Manrope, Plus Jakarta Sans, Playfair Display, Oswald.
    - **Accents:** indigo/violet (hue ~250–290); orange/amber/safety-yellow CTA (hue ~15–50) [v3 9/10].
    - **Grounds:** sage/grey-green paper; green-black dark; cool-grey "galvanized" grounds.
    - **Compositions:** copy-left/artifact-right 5fr/7fr or 1.1fr/.9fr; artifact-first-with-h1-as-caption.
16. Visual polish:
    - every text pair ≥ 4.5:1, and every control boundary ≥ 3:1, in every theme you ship;
    - `:focus-visible`, `transition`, `prefers-reduced-motion`;
    - no emoji as icons;
    - no gradient-clipped text;
    - no `display:grid` row with bare text nodes (they become stray grid items);
    - no text boxes overlapping a drawing.

**Copy**

20. The h1 says what this is and why it differs. It must not narrate the demo state ("Set four was four reps.", "The invoice run is due Thursday and nobody's hook…") [v3 7]. Do not open with "[Brand] is the…".
21. No rhetorical list of three, no "X. Y. Z." staccato, no "no X, no Y, no Z", no "X, not Y" as a formula. Real data lists are fine. [9; 4; 3]
22. Avoid all of these:
    - "Everything you need…", "Ready to…?", "No credit card required.";
    - brand puns;
    - count-led h2s ("Four passes…");
    - "What happens after…";
    - "Try it";
    - "[Verb] your first [noun]";
    - h2s that are 12-word sentences on every section.
    Headings state a finding in as few words as it takes.
23. Do not reuse any label, number or phrase from this skill. Examples here show shape only.

### 4. Run the checker
```bash
python3 .claude/skills/anti-ai-slop/scripts/slop_check.py path/to/page.html            # one page
python3 .claude/skills/anti-ai-slop/scripts/slop_check.py --corpus dir/                # many pages: shared-value report
python3 .claude/skills/anti-ai-slop/scripts/slop_check.py --contrast path/to/page.html # every resolved pair + coverage
```
- Fix every FAIL.
- Give a reason for each WARN you keep.
- **Never clear a WARN by nudging a value**; change the shape or keep the WARN with a reason.
- Passing is necessary, not sufficient.

### 5. Self-check before shipping (every answer yes)
1. At 360×740, does the first screen show an h1 naming the category and the primary CTA?
2. Is every category convention from the seed on the page (prices on a shop, photos for physical things or built work, a phone screen for an app, a terminal/install/docs for a dev tool)?
3. Did you use the seed, with at most two reasoned overrides, and none landing on rule 15?
4. Would this page look *wrong* with another product's name? (swap test)
5. Would it go unnoticed among the v1, v2 or v3 templates? If yes, change the axis that matches.
6. Are owner facts drafted and marked, third-party claims absent, contact facts constants, and the page free of visible "not connected" text?
7. Does the primary CTA lead to the real conversion through a launch constant?
8. Are landmarks, a skip link, the heading order and `aria-hidden` on decoration correct, with contrast measured in every theme?
9. Did you look at the page rendered, desktop and mobile, for overlaps, stray grid items and nav wrapping?
10. Is anything copied from this skill's wording? Replace it.

Hand-off message to the user: list every `<data class="todo">` value and every launch constant to fill in.

## Reference files
- `scripts/brief_seed.py`: the seed and the category conventions (pools are curated; edit them when a corpus run shows > 30% on one value).
- `scripts/slop_check.py`: the static checker (`--contrast`, `--corpus`).
- [references/dont-list.md](references/dont-list.md): the full DO NOT list with frequencies, plus "defaults that are right".
- [references/conflicts.md](references/conflicts.md): how to resolve rules that pull against each other.
- `research/`: v1, v2 and v3 pages, notes and analyses. These are examples of what **not** to produce. Never borrow their forms.
