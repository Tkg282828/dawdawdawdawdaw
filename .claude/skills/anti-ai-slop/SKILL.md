---
name: anti-ai-slop
description: Prevents generic "AI slop" frontend output. Use whenever building or restyling a landing page, marketing site, homepage, hero section, or any user-facing web UI (HTML/CSS, React, Tailwind, Vue, etc.), and when reviewing such UI for a templated, machine-made look. Gives a design-before-code workflow, a frequency-ranked DO NOT list derived from 10 real AI-generated landing pages, and a pre-ship checklist.
---

# Anti AI Slop (frontend)

Slop is not bad code. It is the **average default**: the choice you make when nothing about the product informed it.
This skill comes from an experiment. Ten agents each built a "simple landing page" for a different product, from a coffee roaster to a password manager to an architecture firm. All ten came out as nearly the same page.

**Key finding:** buzzwords like "Supercharge", "Unlock" and "Seamless" appeared on 0 of 10 pages. The slop was in the **structure and CSS**: the same skeleton, the same `.wrap` at 1040px, the same `minmax(240px,1fr)` card grid, the same `--bg/--muted/--card/--line` tokens, the same `12px 24px` buttons, no typeface choice, no real images. Avoiding a word list is not enough; avoid the template.

## Workflow

### 1. Before writing code: the product brief (required)
Write these down, briefly, in your reasoning or a comment:
- **Visitor:** who arrives and what question they must answer before acting.
- **Product artifact:** the one real thing that proves the product (an invoice, a terminal session, a bag of beans, a floor plan, a lesson card). It goes in the hero.
- **Material reference:** one real-world source for color and type (kraft paper, terminal theme, leaf, blueprint, bank statement). Derive tokens from it, and name them for their role in this product.
- **Typeface:** chosen for this product, with a one-sentence reason. Not system-ui and not "Inter because it's safe".
- **Sections:** list only the sections this visitor needs, in the order of their questions. Do not start from nav → hero → 3 cards → "Ready to…?" → footer.

### 2. While building: hard bans (most frequent slop)
Rule-by-rule details and "instead" alternatives are in [references/dont-list.md](references/dont-list.md). The bracketed numbers are how many of the 10 pages showed each pattern.
1. No single `.wrap{max-width:1000–1080px;margin:0 auto}` for everything; choose widths per section, and use `<main>`. [10]
2. No `repeat(auto-fit,minmax(240px,1fr))` card grid of icon + h3 + muted sentence; pick the form for the content (table, ruled rows, spec list, annotated screenshot). [10]
3. No default typography: system-ui only, `16px/1.6`, `clamp(2.2rem,6vw,3.8rem)` h1 at `-.03em`, weight-800 logo. [10]
4. No generic tokens `--bg/--fg/--muted/--card/--line/--accent` with a card one shade off the background, no blue-gray muted `#9aa4bd`, no raw Tailwind hexes (`#4f46e5`, `#8b5cf6`…), no `#0b1020` navy, no `accent → accent2` 135deg gradient or gradient-clipped `<em>`. [10/6/4/4/5]
5. No solid + ghost hero buttons labeled "Get started" / "See features" / "See how it works"; use one specific action ("Deploy your first app", "Pick a roast"). [9]
6. No hero paragraph built on a list of three, and no "[Brand] is the…" opener; write one concrete claim with a number, place or mechanism. [9/8]
7. No two-tone split wordmark (`Task<span>flow</span>`). [8]
8. No one-line centered footer with a hardcoded "© 2026 Brand"; give contact, address, docs and legal links, and generate the year. [9]
9. No emoji as icons or decoration, and no giant emoji or gradient box in place of a photo. [6]
10. No invented stats, testimonials or real-looking placeholders ("2M+ users", "Maya R.", "Northwind Studio"). If proof is missing, mark it `[TESTIMONIAL NEEDED]`. [2–5]
11. No `href="#"` or self-linking CTAs. [6]
12. No missing `transition`, `:focus-visible` or `prefers-reduced-motion`, and no text under 4.5:1 contrast (white on orange or coral buttons failed on 7 pages). [10/10/10/7]
13. No "Everything you need…", "Ready to…?", "No credit card required.", or puns on the brand name. [5/4/4/5]
14. No section added "because landing pages have one": 3-tier pricing with "Most popular", 3-step circles, a stats row, a fake email form. [2–3]

### 3. Before shipping: self-check (every answer must be yes)
1. **Swap test:** if I put another product's name and copy into this layout and color scheme, would it look *wrong*? If not, it is a template; go back to step 1.
2. Does the hero show this product's real artifact, and not an emoji, a gradient box or a generic mock?
3. Was every color derived from the material reference, with no stock Tailwind hex, no indigo-to-violet and no stock navy?
4. Was a typeface chosen and loaded for this product (`font-display:swap`)?
5. Does the hero copy contain one concrete fact, with no list of three and no "[Brand] is the…"?
6. Is every stat, quote, name and company real, or clearly marked as a placeholder?
7. Does every CTA name its action and go to a real destination?
8. Do all text/background pairs meet 4.5:1 in both light and dark themes?
9. Do interactive elements have hover, `:focus-visible` and transition states, with motion gated by `prefers-reduced-motion`?
10. Does the page have `header/nav`, `main`, `footer`, a skip link, h1 → h2 → h3 order, and `aria-hidden` on decoration?
11. Does it work at 360px, with a mobile menu if nav links are hidden?
12. Has every section earned its place for this visitor?

If any answer is "no", fix it before presenting the work.

## What the good outliers did
- **Studio Mara (architecture)** was the only page that did not look templated. It used square corners, a weight-400 serif h1 up to 5rem, services as ruled rows instead of cards, tracked uppercase as the logo, and no emoji or stats.
- On the other pages, the distinctive parts were always **a piece of the product itself**: Brewly's tasting notes and prices, Shipyard's terminal snippet, Ledgerly's sample invoice, Greenleaf's Sprout/Bloom/Jungle plan names. Build the page outward from that piece, not around a template.

## Reference files
- [references/dont-list.md](references/dont-list.md): the full DO NOT list in 8 categories with frequencies and alternatives. Read it during reviews.
- [references/slop-notes.md](references/slop-notes.md): the raw observation tables, with exact hex, CSS and copy snippets per page.
- `research/pages/01–10.html`: the 10 source pages (examples of what **not** to produce).
