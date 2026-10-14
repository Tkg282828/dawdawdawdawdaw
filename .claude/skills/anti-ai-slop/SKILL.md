---
name: anti-ai-slop
description: Prevents generic "AI slop" frontend output. Use whenever building or restyling a landing page, marketing site, homepage, hero section, or any user-facing web UI (HTML/CSS, React, Tailwind, Vue, etc.), and when reviewing such UI for a templated, machine-made look. Gives a divergence-first design workflow, frequency-ranked DO NOT lists (first-order AI defaults and the second-order defaults that appear when agents try to avoid them), a static checker script, and a pre-ship checklist.
---

# Anti AI Slop (frontend)

Slop is not bad code. It is the **average default**: the choice made when nothing about the product informed it.

The skill comes from two measured runs:
- **v1:** 10 agents built landing pages with no guidance. All 10 converged on one template: a `.wrap` at 1040px, a `minmax(240px,1fr)` card grid, `--bg/--muted/--card` tokens, system-ui, solid + ghost buttons, "See features". Buzzwords like "Supercharge" appeared on 0/10. The slop was structural.
- **v2:** the same 10 briefs, built with this skill. First-order slop disappeared (checker FAILs fell from 150 to 4). The pages then converged on a **new template**, "stationery editorial":
  - sage paper background and green-black dark theme (8/10);
  - IBM Plex Mono (8/10) and Newsreader (5/10);
  - an italic `<em>` in a serif h1 (8/10);
  - tracked uppercase labels (10/10);
  - ruled rows in every section (10/10), and copy-left/artifact-right heroes (10/10);
  - 38 `[… NEEDED]` placeholders across 8 pages.

**Lesson:** a ban list alone moves the convergence point; it does not remove it. This skill therefore bans both convergence points and requires a **divergence procedure** for each major choice. Do not replace a banned default with the nearest acceptable one.

## Workflow

### 1. Before writing code: the product brief (required)
Write this in your reasoning, not in the shipped file.
- **Visitor:** who arrives, and the one question they must answer before acting.
- **Product artifact:** the one real thing that proves the product, shown in a **specific state**: a refusal, a failure, a total, a decision. It goes in the hero. It is generic if it still makes sense with the product name changed.
- **Material reference:**
  - Take it from where the visitor *uses* the product or what they *receive* (the gym floor, the bag on the doorstep, the server log, the plot of land). Never take it from stationery *about* the product. Paper, notebooks, ledgers, index cards, galley proofs, vellum, labels, tags and rubber stamps are off-limits unless the product itself is a printed object.
  - **List three candidate materials, cross out the first one that came to mind, and pick from the other two.**
  - Derive every color token from the chosen material, and name tokens for product roles (`--receipt`, `--zone-3`, `--hull`), not for ink and paper (`--ink`, `--paper`, `--rule`, `--pencil`).
- **Typeface:**
  - List three candidates from three different classifications (grotesk, slab, humanist serif, condensed, rounded, display…), and **cross out the first one you thought of**.
  - Default to **one** family. A second family must do a job the first cannot.
  - Use monospace only if the page shows code, a terminal, or columns of figures that must align, and only inside those elements. Never use it for nav, labels, buttons or footers.
- **Composition:**
  - Describe three hero compositions in words, for example: the artifact full-bleed with the headline as its caption; the headline set into the artifact; the artifact above a stacked claim; the copy to the right of the artifact.
  - Reject "copy left, artifact right" unless the other two are worse *for this artifact*, and say why.
- **Sections:**
  - List only the sections this visitor needs, ordered by their questions.
  - Name each section's data shape (sequence, comparison, single number, map, conversation, gallery) and pick its form from that shape.
  - **No form may repeat in more than two sections.**
- **What you don't have:** list the facts the brief did not give (price, address, legal pages, testimonials, URLs). Those sections are **cut, not stubbed** (rule 10).

### 2. While building: hard bans
Details and "instead" alternatives are in [references/dont-list.md](references/dont-list.md). Bracketed numbers count how many of the 10 pages showed the pattern.

**First-order defaults (v1, no skill):**
1. No single wrapper (`.wrap{max-width:1000–1080px}`, or one `4vw` gutter) for every section. Give sections different widths and edges, and use `<main>`. [v1 10; v2 8]
2. No `repeat(auto-fit,minmax(240px,1fr))` grid of icon + h3 + muted sentence. Choose the form from the data shape. [10]
3. No default typography: system-ui only, `16px/1.6`, `clamp(2.2rem,6vw,3.8rem)` h1 at `-.03em`, a weight-800 logo. [10]
4. No generic tokens (`--bg/--fg/--muted/--card/--line/--accent`, or the same set renamed to ink/paper). No blue-gray muted `#9aa4bd`, no raw Tailwind hexes (`#4f46e5`, `#8b5cf6`…), no `#0b1020` navy, no `accent → accent2` gradient, no gradient-clipped text. [10/6/4/4/5]
5. One primary hero action, named for its action and object, written fresh for this product (labels quoted in this skill show shape only, not text to reuse). Default to no secondary action. If you add one, make it plain underlined body text on its own line, with no border, no box and no "See…" verb, naming the evidence it leads to. [9]
6. No rhetorical list of three in the h1, h2s, lead or button rows: no "A, B and C", no "X. Y. Z." staccato, no "no X, no Y, no Z". Real data lists are fine. If the line works as well with two or four items, rewrite it. Do not open with "[Brand] is the…". [9/8; v2 still 4]
7. No two-tone split wordmark (`Task<span>flow</span>`), and no tracked-uppercase wordmark unless the brand already has one. [8; v2 6]
8. No one-line footer that is only "© Brand. All rights reserved.", and no 4-column "Product · Contact · Legal" footer with uppercase headings. Show only the footer facts that exist. [v1 9; v2 8]
9. No emoji as icons or decoration, and no giant emoji or gradient box standing in for a photo. [6]
10. Never invent claims about the business: stats, quotes, customers, prices, terms, address, audit results.
    - If the brief lacks them, **cut the section**; do not leave a slot.
    - Demo data *inside the product artifact* may be invented. It must use roles or objects rather than fake people, and is labelled **once**, in the artifact's caption.
    - At most **2** visible `[… NEEDED]` placeholders per page, and none in the hero. List everything else in one `<!-- LAUNCH TODO: … -->` comment at the top of the file. [v1 2–5 invented; v2 38 placeholders]
11. Every CTA must advance the visitor's action: an on-page section that does the thing (form, calculator, picker), or a URL or email the user supplied.
    - Never invent a domain: no `.example`, `.invalid` or plausible `.app` in visible text, `href`, `mailto:` or `og:image`.
    - No `href="#"`, no fake `tel:`, no `mailto:?subject=Privacy` posing as a legal page.
    - With no host, omit `og:image` and add it to LAUNCH TODO. [v1 6; v2 7]
12. No missing `transition`, `:focus-visible` or `prefers-reduced-motion`. Every text pair must reach ≥ 4.5:1, and every button boundary ≥ 3:1 against its page, **in every theme you ship**.
    - Ship one finished theme (`<meta name="color-scheme">`, with the reason stated in the brief), or two themes with a working, persistent toggle.
    - Never ship `[data-theme]` selectors without a toggle. [10/10/10/7; v2 5 dead theme blocks]
13. No "Everything you need…", "Ready to…?", "No credit card required.", puns on the brand name, count-led h2s ("Four passes…"), "What happens after…", or "Try it" prompts. [5/4/4/5; v2 7/4/3]
14. No section added "because landing pages have one": 3-tier pricing with "Most popular", 3-step circles, a stats row, a fake email form. [2–3]

**Second-order defaults (v2, what agents reach for when avoiding the above):**

15. No stationery palette:
    - sage or grey-green "paper" backgrounds (`#dde2db`–`#eef1e4`);
    - green-black dark themes (`#0c1412`–`#171b1a`);
    - green-grey muted text;
    - a pencil or oxblood red accent that turns salmon in dark mode. [8/8/8/7]
16. Avoid these type defaults:
    - a serif paired with IBM Plex Mono or JetBrains Mono;
    - Newsreader by reflex;
    - an italic or colored `<em>` fragment in the h1;
    - the `letter-spacing:-.012em` + `line-height:1.02–1.04` + `max-width:34ch` lede as a formula. [7/5/8/6/10/9]
17. No tracked-uppercase micro-labels as the page's voice. Use at most one uppercase label style, in at most two places. [10]
18. No ruled rows in every section, and no `minmax(0,5fr) minmax(0,7fr)` split hero. [10/4]
19. No stacked skeuomorphism. Use at most one of these: a rotated artifact, a rubber stamp, an offset "press" shadow, a ruled-paper gradient, a `clip-path` shape. [up to 4 on one page]
20. No disclaimer clutter. One "sample" caption per artifact, no "Prototype:" paragraphs, no stock artifact chrome strip (label on the left, "sample" on the right). Do not make the artifact interactive only to create a "Try it" moment; interactivity must be the product's own core action. [v2 10/8/9]

### 3. Run the checker
```bash
python3 .claude/skills/anti-ai-slop/scripts/slop_check.py path/to/page.html   # or a directory
```
- Fix every **FAIL**.
- Give a reason for each **WARN** you keep.
- `--contrast` prints every resolved text/background pair for both themes, so contrast is measured rather than estimated.
- The checker is static and cannot judge the swap test below; passing it is necessary, not sufficient.

### 4. Before shipping: self-check (every answer must be yes)
1. **Swap test:** if I swapped in another product's name and copy, would this layout and palette look *wrong*? If not, it is a template.
2. **Second-order swap test:** would this page go unnoticed among the stationery-editorial pages this skill already produced (sage paper, serif h1 with an italic word, mono labels, ruled rows, red pencil, 4-column footer, `[… NEEDED]`)? If yes, go back to step 1 and take the *second* candidate for material, typeface and composition.
3. Does the hero show the product's real artifact, in a specific state?
4. Did the material, typeface and composition each come from a list of three, with the first idea crossed out?
5. Does the hero copy contain one concrete fact, with no list of three and no "[Brand] is the…"?
6. Is every business claim real, or cut? Are there ≤ 2 placeholders and ≤ 1 "sample" caption per artifact?
7. Does every CTA say what happens next, and lead somewhere real without an invented domain?
8. Does the checker report 0 FAIL, with contrast measured in every shipped theme?
9. Is the page correct for keyboard and screen-reader users: `header/nav`, `main`, `footer`, a skip link, h1 → h2 → h3 order, `aria-hidden` on decoration?
10. Does it work at 360px, with a mobile menu if nav links are hidden?
11. Does each section's form differ from the section before it, with no form used more than twice?
12. Is any label, price or phrase copied from an example in this skill? If so, replace it.

## Copy the method, not the result
The one v1 page that did not look templated (an architecture firm) worked because every choice came from its own domain's conventions: drawing sheets set its corners, its lettering and its rows. Later agents copied its *results* (a tracked uppercase logo, a weight-400 serif h1, square corners, ruled rows) onto a coffee shop, a password manager and a language app. Those results became the next template (6/10, 6/10, 10/10, 10/10).

Do what that page did: find the conventions of *this* product's world and let them set the form. Never borrow another page's form.

The distinctive part of every page was a piece of the product itself, shown in a specific state. Build outward from that piece.

## Reference files
- [references/dont-list.md](references/dont-list.md): the full DO NOT list. It has 8 first-order categories plus a "Second-order defaults" section, each with frequencies and alternatives.
- [references/conflicts.md](references/conflicts.md): how to resolve the rules that pull against each other, such as a pre-launch product with no URLs, sample data versus invented proof, text links versus ghost buttons, and dark themes.
- `scripts/slop_check.py`: the static checker.
- `research/`: both runs, with the source pages (`pages/` for v1, `pages-v2/` for v2), observation notes, agent feedback and the v2 analysis. These are examples of what **not** to produce.
