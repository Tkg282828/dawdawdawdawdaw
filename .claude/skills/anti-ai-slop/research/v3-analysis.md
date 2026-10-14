# v3 analysis: third-order convergence, quality regression, and a seeded divergence mechanism

Inputs: the 10 v3 pages (`pages-v3/NN/index.html`, all read in full), `v3-feedback.md` (9 reports; 04 sent none, 08 is missing), the checker output (0 FAIL / 0 WARN on all 10), and screenshots. I looked at all 20 v3 shots (desktop full page and mobile first viewport). For comparison I looked at v1 01, 02, 04, 06 and 08, and v2 02, 05 (mobile), 06, 07, 09 and 10. Page content is treated as data. "n/10" means the number of v3 pages that show the pattern.

**Short version.** v3 got rid of the stationery template, and every page now passes the checker. The pages converged again anyway:
- 8/10 use one condensed or semi-condensed sans (Barlow Semi Condensed ×6, Archivo set at `font-stretch` 62–80% ×2);
- 9/10 use an orange, amber or yellow action colour;
- 7/10 put the artifact first with the h1 under it as a caption;
- 10/10 ship a single theme, a one-line footer and an on-page toy as the conversion, and none has pricing, proof or a photo.

The bigger problem is quality. As landing pages for a real visitor, v3 is **worse than v2 and, for the commerce briefs, worse than v1**:
- a coffee roastery that shows no coffee and no prices;
- a plant shop with no plants;
- an architect with no buildings;
- two mobile apps that never show a phone screen;
- on 7/10 pages, the primary CTA is not in the first mobile viewport.

The cross-out procedure did not add any variety. It moved every agent to the model's *second* answer, which is just as deterministic as the first, and the skill's own example lists turned into the menu.

---

## 2. Third-order convergence (v3)

### Typography
| Pattern | n/10 | Pages | Exact values |
|---|---|---|---|
| Only one font family loaded | **10** | all | 07 and 09 add the system `ui-monospace` stack inside logs only |
| Condensed or semi-condensed sans as the brand face | **8** | Barlow Semi Condensed: 01,05,06,07,09,10. Archivo `wdth,wght@62..125` with `font-stretch:62–80%` on headings: 02,08 | 02 and 08 load **the identical axis string** `family=Archivo:wdth,wght@62..125,…` |
| Slab, used by the other 2 | 2 | 03 Bitter, 04 Zilla Slab | Both fonts appeared in v2 or in v3 candidate lists |
| h1 weight 600–700 | 9 | all but 03 (500) | v2 was 400. Agents flipped the banned value instead of choosing one |
| h1 line-height ≤ 1.08 | 9 | .95 (05), .96 (02), .98 (08,10), 1.02 (07), 1.04 (01,06), 1.05 (04), 1.08 (09); 03 is 1.15 | |
| h1 `max-width` in ch/em | 9 | 20ch, 11em, 24ch, 16ch, 15ch, 17em, 17ch, 19ch, 15ch | 06 uses `text-wrap:balance` instead |
| h1 still sized with `clamp()` | **10** | e.g. `clamp(2rem,5.2vw,3.7rem)` (01), `clamp(2.6rem,9vw,6.2rem)` (02) | |
| Explicit `letter-spacing:0` on the h1 or brand | 5 | 03,05,07,08,09 (.01em) | written to dodge the tracking ban |
| Lede `max-width` moved just past the banned 32–36 | 4 admitted | 01 34→**38rem**, 02 34→**37rem**, 07 →**41rem**, 10 34em→**30em**; 06 →30ch | the feedback says so directly |
| Body 1.0625–1.25rem, line-height 1.4–1.55 | 10 | | the new `16px/1.6` |

### Composition
| Pattern | n/10 | Pages |
|---|---|---|
| Vertically stacked hero (no split) | **10** | all |
| **Artifact full-bleed first, h1 below as its caption** | **7** | 01,02,03,04,07,09,10 |
| h1 above, then a full-width artifact | 2 | 05, 08 |
| Headline set into the artifact | 1 | 06 (and on desktop it overlaps the drawing's dimension text) |
| Everything left-aligned, nothing centred | 10 | |
| h1 not visible in the first 360×740 viewport | 2 | 01, 03 |
| h1 visible only in the bottom quarter of that viewport | 4 | 02, 07, 09, 10 |
| **Primary CTA not in the first mobile viewport** | **7** | 01,02,03,05,07,09,10 (visible only on 04, 06, 08) |
| Number of `<section>`s in main | avg 3.7 | 3: 05,06,10; 4: the rest |
| Visible words | avg 268 | 197 (10) to 317 (03). v1 was 156, v2 424 |

In the agents' own reports, the composition candidate lists are **the skill's four example compositions, in the skill's order**: "full-bleed artifact with the headline as caption / headline set into the artifact / artifact above a stacked claim / copy right of artifact". 10/10 crossed out copy-left. 7/10 then took the first example still allowed.

### Nav, logo, footer
| Pattern | n/10 | Notes |
|---|---|---|
| Nav is the logo plus 1–3 in-page anchors only | **10** | none links to Pricing, Docs, Log in, Shop or Work |
| Nav labels are phrases, not destinations | 4 | "A request it turns down" (03), "One task, start to finish" (01), "Where the key lives" (09), "Write the brief" (06) |
| Logo is a small square or circle SVG glyph plus the name in the body face | 8 | 02 and 06 are text only |
| Nav wraps badly at 360px | 6 | 01, 03, 05, 06, 09 wrap to two lines. 04 breaks per word ("The / session") |
| **One-line footer: name + © year (± one link)** | **10** | the v1 footer is back without "All rights reserved". 0/10 show contact, address or legal |
| "Back to the X" footer link | 2 | "Back to the roast log" (02), "Back to the bar" (04) |

### Colour
| Pattern | n/10 | Exact values |
|---|---|---|
| Single theme, no toggle | **10** | 5 dark (01,02,03,04,08), 5 light (05,06,07,09,10) |
| **CTA/accent in the orange-amber-yellow band (hue ≈ 15–50°)** | **9** | `#f2c14e` (01), `#ff8a3d` (02), `#f2b25c` (03), `#f2c230` (04), `#e0501a` (05), `#ec5a24` (06), `#f08a3c` (07), `#b88a2e`/`#d9a93f` (09), `#f5b800` (10). 08 is chartreuse `#c9dc5c`. This is the new indigo |
| Dark text on that accent button | 9 | |
| Pastel green "ok" + salmon "fail" status pair | 4 | 03 `#a9c9a4`/`#e8959a`, 05 `#9fd3a9`/`#ff9a6b`, 07 `#86d9a6`/`#ff8a6b`, 09 refused `#ff9d8a`. The v2 dark-mode salmon came back as the "failure" colour |
| Light pages on a cool grey or greige ground | 4 of 5 | `#eeece9` (07, nudged from the banned `#ebebe8`), `#cfd4d6` (09), `#e8ebed` (10), `#b9b5ab` (06). Only 05 (ply `#c9a273`) is not grey |
| Dark pages on a warm brown-black | 3 of 5 | `#1c1917` (02), `#161412` (04), `#241a14` (08) |

### Tokens
| Pattern | n/10 | Example |
|---|---|---|
| Material-noun token names | 10 | `--wall --peg-hole --safety-outline` (01), `--formwork --shutter --tie-hole --setting-out` (06), `--galvanized --container-steel --lashing-orange --hold` (07) |
| **Same 7-slot structure (ground, ground-deep, text, text-quiet, accent, on-accent, edge)** | **10** | 01: `wall / wall-deep / enamel-white / steel-label / safety-outline / on-safety / tool-edge` is `bg / card / fg / muted / accent / on-accent / line` |
| `-deep/-raised/-soft/-dim/-quiet/-lit` suffix for the second step | 10 | |
| An `-edge` (line) token | 6 | `--tool-edge`, `--tray-edge`, `--room-edge`, `--ply-edge`, `--plate-edge`, `--hinge` |
| The same token name on two pages | 2 | `--platform` (04 and 10) |

Renaming tokens for the material changed the names. It did not change the structure.

### Materials
| Pattern | n/10 | Pages |
|---|---|---|
| Industrial, signage or hard-surface material | **8** | pegboard (01), roasting drum (02), bumper plates on rubber (04), birch ply and cable tie (05), board-formed concrete (06), container yard (07), safe-deposit steel (09), enamel station signage (10) |
| "Safety/marking orange or yellow" from that material | 5 | `--safety-outline`, `--setting-out` (spray paint), `--lashing-orange`, `--cable-tie`, `--ring-line` |
| First candidate crossed out (from the reports) | | terminal (07, 09), paper (03, 06), kraft (02), bank-app feed (05), kitchen ticket (01), phone glass (10) |

### Typeface candidate lists (7 reports)
- **Crossed out:** Inter (01,03,05), Space Grotesk (07,09), "Space Grotesk/Inter" (06), a Fraunces-style serif (02), a Helvetica-style grotesk (10).
- **Barlow Semi Condensed appears in 6 of 7 lists.** A slab appears in 5 (Bitter ×2, Zilla Slab ×2, Roboto Slab ×1).

So even the "divergent" candidates came from one shared distribution.

### Sections, forms and CTA
| Pattern | n/10 | Pages |
|---|---|---|
| A sequence/timeline section (dated or numbered rows on a vertical line) | **7** | 01 day log, 04 set log, 05 chase, 06 programme, 07 track, 08 thread, 10 ring table |
| A comparison `<table>` | 5 | 02, 04, 05 (hero), 09, 10 |
| A `<dl>` readout or legend | 6 | 01, 02, 04, 05, 08, 09 |
| **Last `<main>` section is an on-page widget** | **9** | all but 07 |
| …a calculator, picker or generator | 6 | 02 bag builder, 03 length checker, 05 tax calculator, 08 plant picker, 09 passphrase generator, 10 card-count calculator |
| …an email or brief form with no endpoint | 3 | 01, 04, 06 |
| **Hero CTA scrolls to that widget** | **9** | 07 copies a command to the clipboard |
| A CTA that leads to signing up, buying, booking or downloading | **0** | |
| Visible "not connected / nothing is sent / pre-launch / NEEDED" text | **7** | 01 "Nothing is sent yet…", 02 "Online checkout is not connected yet" ×2, 03 "The full editor is not connected", 04 `[SIGN-UP NOT CONNECTED YET: nothing is sent]`, 06 `[studio email NEEDED]`, 08 `[ORDER LINK NEEDED]`, 09 "pre-launch" |
| Pricing, plans or any price | **0** | v1 had 3 pricing blocks; v2 Brewly had $17/$15/$14 |
| Social proof of any kind | **0** | |
| `<img>` or photo | **0** | coffee, plants and architecture are categories where photos *are* the content |
| Mobile app that shows a phone screen | **0 of 2** | 04 shows a barbell; 10 shows a ring diagram. v1 04 at least drew a phone |
| "Sample/demo/invented" caption on the artifact | 10 | "Demo session, invented for this page." (04), "Demo figures from an invented October." (05) |

### Copy
| Pattern | n/10 | Examples |
|---|---|---|
| **The h1 restates the artifact's demo state as a narrative sentence** | **7** | "The invoice run is due Thursday and nobody's hook is holding it." (01), "It marked two of your forty-one sentences…" (03), "Set four was four reps." (04), "The release that failed its health check never got a single request." (07), "Damp at the second knuckle, so this week's message says skip the watering." (08), "Our servers hold 412 KB of noise…" (09), "The roof stops where your neighbour's light begins." (06) |
| The h1 never names the product category | 6 | 01, 03, 04, 07, 08, 09. A visitor has to read the lede to learn it is a task app, a writing tool, a fitness app… |
| h1 ends with a period | 9 | all but 02 |
| h2 is a full declarative sentence of 6+ words | 9 | "Each outline answers who has it and whether it is still open", "Each stop is later than the last, and a miss costs you the distance" |
| "X, not Y" | 3 | "the weight you can move, not the one you planned" (04), "in ten minutes, not next week" (10), "too much water, not too little" (08) |
| The CTA is an imperative with a possessive | 5 | "Reserve a board for your team", "Write down your site's constraint", "Match a plant to my window", "Work out my daily card count", "Put me on the launch list" |

### Components and effects
| Pattern | n/10 |
|---|---|
| Button radius 0–3px | 7. 04, 08 and 09 use an asymmetric "material" radius (`2px 14px 2px 14px`, `2px 2px 16px 16px`, `0 18px 18px 0`) |
| Bottom-border "keycap press" button (`border-bottom:4px solid` darker) | 2 (02, 05) |
| `transition … .15s` | 10 |
| Skip link `top:-60px` or `left:-999px` | 10 |
| Base layer identical to v2 (`button,input{font:inherit;color:inherit}`, `img,svg{max-width:100%;display:block}`) | 10 |

### Visible bugs the checker cannot see
- **07:** every `<li>` in the hero log is `display:grid` with `white-space:pre`. The bare text after each `<span>` becomes an extra grid item, so on desktop and mobile "503" and "attempt 1 of 6" break onto separate rows and ", 0 requests dropped" is orphaned. The hero artifact looks broken.
- **06 desktop:** the absolutely positioned h1, lede and CTA sit on top of the "Ridge 3,780" and "Eaves 2,160" dimension text.
- **10:** "missed at 7 days, back at 10 min" runs over the green ring stroke.
- **05:** the hero table says "Still owed 4,750.00, of which already tax (21%) 997.50". 997.50 is 21% *of* 4,750. The page's own calculator treats invoice totals as gross, so the tax inside 4,750 is 4,750 × 21/121 = 824.38. An accounting product with wrong arithmetic in its hero loses credibility.
- **Contrast pairs the checker never tested:**
  - 05 cable-tie button `#e0501a` on ply `#c9a273` is **1.67:1** (non-text boundary). The checker skips it because the rule contains `border-bottom`.
  - 02 radio and level-picker borders `#4a413a` on `#12100e` are **1.76:1**.
  - 10 has yellow `#f5b800` sections on `#e8ebed`; that one is fine, it is a band.

---

## 3. Quality, as a senior designer would judge it from the screenshots

### Scores (1–5, averaged per run)
| | Distinctiveness | Clarity (what is it, in 5 s) | Polish | Credibility | Conversion path | Mobile first viewport |
|---|---|---|---|---|---|---|
| **v1** (no skill) | 1.0 | **4.0** | 2.5 | 2.0 (looks credible, but the stats and testimonials are invented) | 3.0 (structure there, links dead) | 3.5 (1 overflow) |
| **v2** (skill v1) | 2.5 (one template across the set) | 3.5 | **3.5** | 2.5 (honest, but red `[NEEDED]` makes pages look broken) | 2.5 | 3.0 |
| **v3** (skill v2) | 3.0 per page, **2.0 as a set** | **2.5** | 3.0 (clean type; 3 visible bugs; flat single-font pages read as wireframes) | **1.5** | **1.5** | **2.0** (CTA missing on 7/10, h1 missing on 2) |

### Verdict
**v3 is not a better landing page than v2 for a real visitor. On the commerce and portfolio briefs it is worse than v1.**

What v3 did well:
- Each page, seen alone, is more distinctive than v1 and less obviously templated than v2.
- Hero artifacts are product-specific: the 07 failed-health-check log, the 05 overdue invoice with its tax line, the 03 marked draft, the 10 ring.
- Placeholder clutter fell from 38 to 3.
- 05 Ledgerly, 03 Nimbus and 07 Shipyard (once its log bug is fixed) are decent pages.

What regressed:
1. **Product-shaped content was removed.**
   - Brewly v3 is a roastery page with a roast-temperature curve and **no coffees, no origins and no prices**. The v2 and v1 Brewly pages both had three named coffees with prices, which is the thing a coffee buyer came for.
   - Greenleaf v3 is a plant shop with **no plants** on a peat-brown page.
   - Studio Mara v3 is an architect with **no built work**. The single most important section for that buyer is missing.
   - FitPulse and Lingo Loop are mobile apps whose pages never show the app.
2. **Artifact-first heroes hide what the product is.** On mobile, Taskflow and Nimbus show only the artifact in the first viewport. Brewly, Shipyard, Vaultix and Lingo Loop push the h1 to the bottom edge, and 7/10 push the CTA below the fold. The narrative h1 ("Set four was four reps.") then makes the reader infer the category.
3. **The conversion path was removed.**
   - 0/10 let you sign up, buy, book or download.
   - 9/10 send the CTA to a toy (a passphrase generator for a password manager, a sentence-length checker for an AI writer, a card-count calculator for a language app).
   - 7/10 then tell the visitor in plain text that the product is not connected.
   - Honesty belongs in the hand-off to the user, not on the page.
4. **Literal metaphors replace the product.**
   - Taskflow becomes a "pegboard" whose tasks hang on "hooks", and the h1 talks about hooks.
   - Shipyard *crossed out the terminal*, which is the correct artifact for a deploy tool, picked "container yard", and the only trace of the container yard is an orange.
   - The material procedure produced metaphors a visitor has to decode, and for screen software the material should be the UI itself.
5. **The set reads as one template.** One condensed sans, a grey or brown ground, an orange button, artifact-then-caption, a timeline section, a widget, and a one-line footer.

### Rough ranking (best to worst; pages I did not view are placed from v1-notes and v2-analysis)
1. v2-02 Brewly (products, prices, roast date, strong typography)
2. v2-07 Shipyard
3. v2-09 Vaultix
4. **v3-05 Ledgerly**
5. **v3-07 Shipyard** (if the log bug were fixed)
6. **v3-03 Nimbus**
7. v2-10 Lingo Loop
8. v2-06 Studio Mara (the drawing is excellent; ruined by 10 placeholders)
9. v2-05 Ledgerly
10. v1-02 Brewly (generic but sells coffee)
11. v1-08 Greenleaf (generic, invented proof, but a complete funnel)
12. **v3-10 Lingo Loop**
13. **v3-04 FitPulse**
14. **v3-09 Vaultix**
15. v2-01, v2-03, v2-04, v2-08 (stationery template)
16. v1-04 FitPulse
17. v1-06 Studio Mara
18. v1-05, v1-09, v1-07, v1-03, v1-10 (interchangeable)
19. **v3-01 Taskflow**
20. **v3-06 Studio Mara**
21. v1-01 Taskflow
22. **v3-08 Greenleaf**
23. **v3-02 Brewly**

The v3 pages sit in two places. The software pages with a real UI artifact (05, 07, 03) are among the best of all 30. The physical-product and portfolio pages (02, 08, 06) are among the worst, because the skill told them to avoid exactly what those visitors came to see.

---

## 4. Mechanism: why bans plus cross-out still converge, and what to do instead

### Diagnosis
1. **Conditional mode collapse.** Every agent is the same model reading the same skill and a near-identical brief. Banning the argmax gives `argmax P(x | x ∉ banned)`, a new mode that is just as sharp and is shared by every agent. "List three, cross out the first" just makes this explicit:
   - the first candidate is the old mode (Inter or Space Grotesk, 6/7);
   - the second is the next mode (Barlow Semi Condensed, in 6/7 lists);
   - the pick lands there (6/10).
   Asking the model for "variety" draws on the same distribution that produced the sameness.
2. **Examples are a menu.** Any concrete example in the skill becomes a candidate:
   - the four composition examples were copied verbatim and taken in order (7/10 took the first allowed one);
   - `--hull` became 07's "hull red-oxide" candidate;
   - "where the visitor uses it" became physical workplaces (8/10 industrial).
   v2 showed the same thing ("Pick a roast", $17).
3. **Numeric bans invite nearest-neighbour edits.** 34rem became 37 or 38rem and `#ebebe8` became `#eeece9`. The checker became the objective; the visitor did not. Exact-value bans measure the proxy, not the shape.
4. **Only negative pressure.** Every rule says what *not* to do and nothing says what the visitor needs, so the optimum drifts toward "maximally unlike a landing page". Pricing, photos, signup, nav to Docs or Pricing and a real footer were all removed because they look like defaults. Some defaults are defaults because they are right.
5. **No shared memory between parallel agents.** Ten agents running at once cannot avoid each other's choices. Without entropy from outside the model, they will land on the same answer.

### Design: separate *content* from *style*, and use different mechanisms for each
- **Content (what a visitor of this category must see) is deterministic and conventional.** Look it up from a category table: a shop shows products with photos and prices, an app shows a phone screen and store links, a dev tool shows a terminal, install steps and docs, a studio shows built work. This is where the default is right, so the skill must *require* it instead of banning it.
- **Style (type class, face, hero composition, colour strategy, hue, theme, scale, edges, headline shape) gets external entropy.** `brief_seed.py` hashes the brief and assigns one option per axis from large curated pools. The pools leave out every value already seen to converge. The agent must use the assignment, and may override at most two axes, each with one sentence that names a visitor need or a category convention (not taste). An override may not land on a converged value.
- **Verification checks shapes and corpus similarity, not exact numbers** (see §5).

### Evaluation of the deterministic seed
**Pros**
- The entropy comes from SHA-256 of the brief, which is uncorrelated with the model's priors, so the second-mode problem disappears.
- Deterministic: the same brief always gives the same seed. That makes runs reproducible and diffable, and makes the skill regression-testable. Run the 10 briefs again after any skill change and the style assignments stay fixed, so any new convergence is caused by the rules, not by chance.
- Cheap: no web access, no extra generations.
- Pools are curated by a human once, so they contain good options (real Google Fonts families in a coherent class, colour *strategies* rather than hexes) instead of random values.
- `--salt N` gives alternative directions on request.

**Measured spread** (`brief_seed.py --table briefs.txt`, same 10 briefs):
- 9 distinct lead fonts out of 10 (max 2 repeats), against v3's 6/10 Barlow Semi Condensed;
- 6–7 distinct type classes (max 3);
- 6 distinct hero compositions (max 3), against v3's 7/10 artifact-first;
- 6–7 distinct colour strategies (max 3), against 9/10 orange CTAs;
- 7–8 distinct hue families (max 2);
- both light and dark themes plus toggles.

No two briefs get the same combination. This holds for salts 0, 1 and 2 (table in §7.3).

**Risks and mitigations**
- *A bad fit for the product* (a rounded face for an architect). Pools carry `avoid`/`only` category filters (rounded avoids studio, legal and security; mono appears only for devtool or AI; catalogue-first appears only for shop or delivery; product-UI stage only for software). Two reasoned overrides remain.
- *Agents override everything with invented reasons.* The cap is two axes. Each reason must name a visitor need, and the override may not land on any converged value. The checker can verify the second part.
- *The pools become the next template.* With about 11 type classes × 6 faces, 13 compositions, 11 strategies, 11 hues, 4 themes, 5 scales, 6 edge languages and 6 headline shapes, there are millions of combinations. Even so, keep a fingerprint registry and retire or add options whenever a corpus run shows more than 30% on one value.
- *Randomness does not equal quality.* Correct. The seed only sets direction. Quality comes from the category conventions, the visitor-first workflow and the checks, which is why content is not randomised.
- *The same brief always gets the same look.* For one product that is a feature (stable). For a second direction, use `--salt`.

**Alternatives considered**
- **"Generate 3 full divergent directions, then pick."** The three directions come from the same distribution, so they are correlated across agents. The pick drifts toward the safest. It costs about three times as much. Worth it only *on top of* the seed (salts 0, 1 and 2 give three uncorrelated directions, and the agent picks by visitor fit), and only when the user wants options.
- **A moodboard from real category leaders.** Very good for *conventions* (what sections a buyer expects), and that is exactly what the category table encodes cheaply and offline. As a *style* source it is risky: category leaders converge among themselves (every SaaS looks alike), the model's memory of "what Stripe looks like" is itself averaged, it needs web access, and it invites near-copies of real brands. Use it for conventions only.
- **Higher temperature or "be creative" prompting.** It is not under the skill's control, it raises errors, and the mode is still there.
- **Cross-run fingerprint memory alone.** Good for detecting convergence, but it is post hoc and does not help parallel agents. Keep it as the check, not as the generator.

**Recommendation:** use the seed for the style axes, a category-convention table for content, and a checker with shape rules, near-miss detection, a fingerprint registry and an optional render check. Remove the cross-out procedure and every concrete example list from SKILL.md.

---

## 5. Checker weaknesses and fixes

| Weakness | Evidence | Fix |
|---|---|---|
| Patterns match comments | 03 had to reword a CSS comment ("desk lamp" → "single bulb"); the `desk[- ]lamp` rule runs on raw `low` | Strip `<!-- -->`, `/* */` and `//` comments before every pattern check. Run copy rules on visible text only |
| Lede-measure rule matches any `max-width:32–36` | 05 changed a *form* width and 06 a grid column just to clear it; `max-width\s*:\s*3[2-6](ch\|rem\|em)` | Delete it. Replace with the shape fingerprint below |
| Exact-value bans get gamed by 2–4 units | 34→37/38/41rem; `#ebebe8`→`#eeece9`; h1 tracking forced to `0` | Express bans as **shapes and distances**. Colours: OKLab ΔE < 0.05 from any banned swatch, or the same (hue bucket, chroma bucket, lightness bucket) cell, counts as a hit. Layout and type: a fingerprint, not a value |
| No cross-page view | Barlow Semi Condensed 6/10 and orange CTA 9/10 pass silently | Add `--corpus DIR`: compute a per-page fingerprint and WARN on any value shared by more than 30% of pages. Add `references/fingerprints.json` with the v1, v2 and v3 template fingerprints; WARN when a page matches 5 or more of 9 features of any known template |
| `--contrast` covers 2–4 pairs per page | 01 printed 3 pairs, 02 and 03 printed 2 | Parse the DOM with `html.parser`. Match simple selectors (tag, class, id, descendant) to rules. For every text node, take the nearest ancestor background (including SVG `fill` on `<text>`, `:hover` and `::placeholder`). Report coverage ("checked 41/47 text elements; 6 unresolved"). Unresolved counts as WARN, not as silence |
| The button-boundary check skips any rule that contains `border` | 05 `border-bottom` only, so the 1.67:1 fill on ply passes | Count only a full `border:` or `outline` with ≥ 3:1 as an edge. Also check form controls (input, select, radio labels) at 3:1 against their background (02 1.76:1) |
| No convention or content checks | 0/10 pricing, 0/10 photos, 0/2 phone UI, 0/10 real CTA, all passed | Add category inference (reuse `brief_seed.categories` on `<title>`, `meta description` and h1). WARN when: a shop or delivery page has no price pattern or `<img>`/photo slot; an app page has no phone frame or store link; a studio has no `<img>`; any category has no CTA leading to a URL constant or form `action` |
| No disclaimer check for "not connected" | 7/10 tell visitors the product does not work | FAIL on more than one visible `not (yet )?connected\|nothing is sent\|pre-launch\|not released\|NEEDED` phrase. The hand-off message carries that information |
| No first-viewport or rendering check | CTA below the fold on 7/10; h1 missing on 2; overlaps on 06 and 10; grid stray-text bug on 07 | (a) Static: WARN on a `display:grid` element whose children include bare non-whitespace text nodes (catches 07). WARN when the first `<section>` in `<main>` has its h1 after a figure, svg or pre larger than about 40% of its text. (b) Optional `--render` (only if Playwright is installed): at 360×740 assert the h1 and the primary CTA are in the viewport, there is no horizontal overflow, and no two text boxes intersect |
| Copy rules miss the new formula | 7/10 narrative-instance h1s | WARN if the h1 contains none of the category nouns from the meta description, and FAIL in the self-check if a stranger cannot name the category from the h1 plus lede |
| Second-order WARNs became a to-do list of values to flip | weight 400→600–700, `-.012em`→`0` | Make the WARN text describe the shape ("the h1 restates the demo"), never the value |

**Fingerprint features** (9, each bucketed):
1. family set and class;
2. width class (condensed / normal / wide);
3. h1 weight bucket;
4. ground: light, dark or field, plus hue bucket;
5. accent hue bucket;
6. theme count;
7. hero order (artifact before or after the h1; split or stack);
8. last-section type (widget, form, contact, footer);
9. footer shape (one line or multi-column).

A page is "on template" if it matches 5 or more features of a known template. All 10 v3 pages match the "v3 template" (condensed or single family, orange accent, single theme, stack or artifact-first, widget last, one-line footer) on 5 or more features.

---

## 6. Over-corrections, and the defaults to restore

| Rule in skill v2 | What it produced | Change |
|---|---|---|
| "Material from where the visitor uses the product; cross out the first" | Pegboard, container yard, safe-deposit steel; a literal metaphor a visitor must decode | **Drop the material requirement.** For screen software, the material *is* the product UI. A metaphor is allowed only if a visitor of this category would recognise it without explanation |
| Cross out the first typeface, composition and material | The first idea was crossed out even when it was right (terminal for a deploy tool) | Remove it. The seed handles style; conventions handle content. The terminal, phone screen and product photo are **required** where the category calls for them |
| "Cut, not stub" + "never invent claims" + no placeholders | No pricing anywhere, no photos, no proof, 7/10 "not connected" notes | Split facts by **who must supply them**: <br>• **Owner facts** (price, plans, trial terms, opening hours, product names, shipping terms) may be *drafted* as plausible sample values. Wrap each one in `<data class="todo">`, list it in LAUNCH TODO, and name it in the hand-off. <br>• **Third-party claims** (quotes, ratings, user counts, logos, press, audits) are never drafted; that section is cut. <br>• **Contact facts** (address, phone, email) are never drafted; use a LAUNCH constant |
| "Every CTA must advance the visitor's action on this page" | Every CTA became a toy calculator | The primary CTA is the category's real conversion (sign up, buy, book, download, install). It points to one LAUNCH constant (`data-href="SIGNUP_URL"` or a form `action`) that the user fills. On-page tools are allowed as a *secondary* proof. No visible "not connected" text |
| Artifact first, headline as caption (the skill's example) | CTA below the fold on 7/10 mobile | Any hero is allowed, as long as the first 360×740 viewport holds an h1 that names the category, plus the primary CTA |
| Nav made of in-page anchors only | Nav labels like "A request it turns down" | The nav links to what this buyer checks: Pricing, Docs, Shop, Work, Log in. Labels are destinations, not phrases |
| Footer "only facts that exist" | A one-line footer on 10/10 | Footer = contact route + legal links (as LAUNCH constants) + the one or two facts that exist. Placeholders stay in source, not on the page |
| "Specific state" artifact plus a narrative h1 | 7/10 h1s restate the demo | The h1 says what it is and why it is different. The artifact shows the state; the h1 does not narrate it |
| Single theme preferred, toggle hard | 10/10 single theme | Fine. Keep it; the seed may assign a toggle |
| A banned list of v2 numeric values | Values flipped or nudged | Replace with shape rules and fingerprints |

**Principle to state in the skill:** *slop is an unconsidered default. A default that serves this visitor (price on a shop, terminal on a dev tool, phone on an app, photos for a studio) is not slop. Removing it is.*

---

## 7. Exact proposed text

### 7.1 SKILL.md (complete replacement)

````markdown
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
````

*(About 150 lines. Rules are numbered 1–6, 10–11, 12–16 and 20–23 on purpose, so the groups stay stable as rules are added.)*

### 7.2 dont-list.md changes (replacement text)

**Replace Typography item 1 with:**
```markdown
1. **Do not ship with no typeface decision** (system-ui only, or Georgia plus system-ui) [v1 10], **and do not pick by "anything but my first idea"** [v3: 6/10 landed on the same second idea, Barlow Semi Condensed].
   Instead: take the class and shortlist from `scripts/brief_seed.py`. Load with `font-display:swap`. Monospace appears only inside code, terminal or aligned-figure elements.
```

**Replace Copy items 10 and 11 with:**
```markdown
10. **Sort missing facts by who supplies them.**
    - Never invent **third-party claims** (quotes, ratings, user counts, customer logos, press, audits) [v1 2–5]; cut the section.
    - Draft **owner facts** (prices, plans, product names, trial terms, hours, shipping) as plausible values in `<data class="todo">`, listed in LAUNCH TODO and named in the hand-off. Do not cut them: v3 cut pricing on 10/10, and a shop without prices cannot sell.
    - **Contact facts** are launch constants, never invented.
11. **Do not put honesty notes on the page** ("not connected", "nothing is sent", "pre-launch", "[… NEEDED]") [v2 38 placeholders; v3 7/10 pages]. One short caption on a demo artifact is the maximum. The hand-off message carries the rest.
```

**Replace Imagery items 1, 4 and 5 with:**
```markdown
1. **Do not ship a physical-product, delivery or portfolio page without photographs** [v1 10; v2 10; v3 10 had zero `<img>`].
   Instead: use real photos when supplied; otherwise use art-directed photo slots (`<figure class="photo-slot" data-todo="photo: 250 g bag, kraft, top-lit">`) with correct aspect ratios and alt text. The slot is designed space, not a grey box with "[PHOTO]".
4. **Do not use gradient boxes or abstract objects as stand-ins for the product** (gradient "project photos", a barbell instead of the app screen, a ring diagram instead of the lesson screen) [v1 1; v3 2/2 apps showed no phone].
5. Do show the product itself in a specific state in the hero: the real UI, terminal session, phone screen, product photo or built work. Give it `role="img"` and an `aria-label`, or real semantic markup. A metaphor (pegboard, container yard, station signage) never replaces the product [v3 8/10 metaphors].
```

**Replace Code item 3 with:**
```markdown
3. **Do not ship `href="#"`, invented domains, or a conversion that goes nowhere** [v1 6; v2 7; v3 9 toy CTAs, 0 real].
   Instead: the primary CTA is the category's real action and points to one launch constant (`<form action="SIGNUP_URL">` or `data-href="SIGNUP_URL"`), declared in `<!-- LAUNCH TODO -->`. On-page calculators and pickers are secondary proof, not the conversion. No visible "not connected" text; no fake "Thanks!" state.
```

**Replace the whole "Second-order defaults" section with:**
```markdown
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
```

### 7.3 The seed script

The full source is below and in `scratchpad/brief_seed.py`. Put it in the skill at `scripts/brief_seed.py`.

Output on the 10 briefs (`briefs.txt`, salt 0). It is also saved as `scratchpad/seed-table-salt0.md`.

| brand | category | typeface (class) | hero | colour strategy | hue | theme | scale | edges | headline |
|---|---|---|---|---|---|---|---|---|---|
| Taskflow | saas | Antonio (condensed display) | product-UI stage | two-tone split | brown-oxide | dark | airy poster | soft uniform | short name-like phrase |
| Brewly | shop | Syne (wide / extended sans) | type poster | image-sampled | rose / magenta | light | airy poster | pill controls + square containers | short name-like phrase |
| Nimbus AI | ai | Alegreya Sans (humanist sans) | type poster | saturated field | cyan | light | editorial medium | heavy outline | short name-like phrase |
| FitPulse | app | Baloo 2 (rounded sans) | product-UI stage | neon on mid-grey | leaf green | dark | airy poster | soft uniform | imperative to the visitor |
| Ledgerly | finance | League Gothic (condensed display) | demo-in-hero | high-chroma duotone | olive-chartreuse | two themes | airy poster | hairline sharp | number-led |
| Studio Mara | studio | Urbanist (geometric sans) | fixed half + scrolling half | two-tone split | olive-chartreuse | two themes | editorial medium | pill controls + square containers | number-led |
| Shipyard | devtool | Questrial (geometric sans) | bento of unequal tiles | tonal analogous | cobalt / ultramarine | dark | catalogue dense | hairline sharp | short name-like phrase |
| Greenleaf | delivery | League Gothic (condensed display) | asymmetric split, artifact bleeds off the edge | saturated field | rose / magenta | light | extreme contrast | soft uniform | imperative to the visitor |
| Vaultix | security | Aleo (slab serif) | product-UI stage | two-tone split | teal | dark | editorial medium | hairline sharp | the visitor's question, answered |
| Lingo Loop | app | Bricolage Grotesque (characterful grotesque) | demo-in-hero | saturated field | yellow-lime | two themes | editorial medium | soft uniform | the visitor's question, answered |

Spread per axis (distinct values / maximum repeats, over the 10 briefs):

| Axis | salt 0 | salt 1 | salt 2 | v3 actual |
|---|---|---|---|---|
| Lead font | 9 / 2 | 9 / 2 | 9 / 2 | 4 / **6** |
| Type class | 7 / 3 | 7 / 3 | 6 / 2 | 2 / **8** |
| Hero | 6 / 3 | 6 / 3 | 6 / 3 | 3 / **7** |
| Colour strategy | 6 / 3 | 6 / 2 | 7 / 3 | ≈1 / **9** |
| Hue | 8 / 2 | 7 / 2 | 7 / 2 | ≈2 / **9** |

No two briefs share a full combination.

**Known limits of the seed:**
- Repeats of 2–3 per axis across 10 independent briefs are expected from hashing (birthday effect). They do not add up to a template, because the other 8 axes differ.
- Some assignments will feel wrong, for example "number-led" headlines for an architect. That is what the two-override budget is for.
- Category inference is a keyword regex. Unknown briefs fall back to `saas`; let the agent correct the category in the override line.

Full source:

```python
#!/usr/bin/env python3
"""brief_seed.py - deterministic design-direction seed for a landing page brief.

Why: an LLM asked to "avoid the default" picks its *second* most likely answer,
and every agent picks the same one (v3: Barlow Semi Condensed on 6/10 pages,
orange/amber CTA on 9/10, artifact-first hero on 7/10). This script injects
entropy that does not come from the model: it hashes the brief and assigns one
option per style axis from large curated pools. Content conventions (what a
visitor of this category needs to see) are NOT randomised; they are looked up.

Usage:
  python3 brief_seed.py "Brewly - local specialty coffee roastery, whole beans online"
  python3 brief_seed.py --salt 2 "..."      # an alternative direction for the same brief
  python3 brief_seed.py --json "..."        # machine-readable
  python3 brief_seed.py --table briefs.txt  # one brief per line, summary table

Same brief + same salt -> same output, on any machine and Python 3.6+.
Stdlib only.
"""
import hashlib
import json
import re
import sys

# --------------------------------------------------------------------------
# Never assigned (already shown to converge in v1-v3, or ubiquitous AI picks).
# The agent may still use one ONLY via an override with a product reason.
CONVERGED_FONTS = [
    "Inter", "Space Grotesk", "Newsreader", "IBM Plex Mono", "IBM Plex Sans",
    "JetBrains Mono", "Barlow Semi Condensed", "Barlow", "Archivo", "Fraunces",
    "Bitter", "Zilla Slab", "Roboto Slab", "Roboto", "Poppins", "Montserrat",
    "DM Sans", "Manrope", "Plus Jakarta Sans", "Playfair Display", "Oswald",
    "Open Sans", "Lato", "Geist", "Satoshi",
]

# --------------------------------------------------------------------------
# Typeface classes. Each: fonts (Google Fonts family names), what the class
# is good at, and categories it is a poor fit for (filtered out, not banned).
TYPE_CLASSES = [
    {"cls": "characterful grotesque",
     "fonts": ["Schibsted Grotesk", "Bricolage Grotesque", "Familjen Grotesk",
               "Hanken Grotesk", "Instrument Sans", "Host Grotesk"],
     "use": "headlines at weight 600-800 with tight but not negative tracking; body in the same family",
     "avoid": []},
    {"cls": "geometric sans",
     "fonts": ["Jost", "Urbanist", "Red Hat Display", "Kumbh Sans", "League Spartan", "Questrial"],
     "use": "round counters, even colour; big h1 at 500-700, generous letter-spacing on small sizes only",
     "avoid": []},
    {"cls": "humanist sans",
     "fonts": ["Alegreya Sans", "Cabin", "Fira Sans", "Source Sans 3", "Asap", "Atkinson Hyperlegible"],
     "use": "warm, readable; good for long body copy and dense UI mocks",
     "avoid": []},
    {"cls": "wide / extended sans (display only) + a plain text face",
     "fonts": ["Unbounded", "Syne", "Krona One", "Michroma", "Lexend Exa", "Dela Gothic One"],
     "use": "h1/h2 only, short headlines (<= 8 words); pair with a humanist or grotesque text face",
     "avoid": ["legal", "health"]},
    {"cls": "condensed display (display only) + a plain text face",
     "fonts": ["Big Shoulders Display", "Sofia Sans Condensed", "Saira Condensed",
               "Antonio", "League Gothic", "Encode Sans Condensed"],
     "use": "very large h1 set tight, uppercase allowed only in the h1; text face from another class",
     "avoid": []},
    {"cls": "rounded sans",
     "fonts": ["Fredoka", "Varela Round", "M PLUS Rounded 1c", "Baloo 2", "Quicksand", "Nunito"],
     "use": "friendly, consumer; pair with soft or big-round corners; weights 500-700",
     "avoid": ["studio", "legal", "security"]},
    {"cls": "old-style / transitional text serif",
     "fonts": ["Libre Caslon Text", "Crimson Pro", "Literata", "Gelasio", "EB Garamond", "Source Serif 4"],
     "use": "body and headlines in one serif, upright headlines (no italic fragment in the h1)",
     "avoid": ["devtool"]},
    {"cls": "high-contrast display serif (display only) + a sans text face",
     "fonts": ["Bodoni Moda", "Gloock", "Instrument Serif", "DM Serif Display", "Abril Fatface", "Rozha One"],
     "use": "h1 large (>= 4rem desktop), body in a sans from another class",
     "avoid": ["devtool", "security"]},
    {"cls": "slab serif",
     "fonts": ["Arvo", "Rokkitt", "Aleo", "Josefin Slab", "Podkova", "Alfa Slab One"],
     "use": "sturdy headlines; body can stay in the slab if the text face is not Alfa Slab One",
     "avoid": []},
    {"cls": "soft / wonky display serif + a sans text face",
     "fonts": ["Young Serif", "Corben", "Caprasimo", "Domine", "Petrona"],
     "use": "warm, food/retail/consumer; one weight for display, sans for UI",
     "avoid": ["devtool", "security", "finance"]},
    {"cls": "monospace as the brand voice (code products only)",
     "fonts": ["Martian Mono", "Fragment Mono", "DM Mono", "Red Hat Mono", "Azeret Mono", "Spline Sans Mono"],
     "use": "headline + code in mono, body in a sans; only where the product is used through text",
     "only": ["devtool", "ai"]},
]

TEXT_FACES = ["Hanken Grotesk", "Instrument Sans", "Source Sans 3", "Fira Sans",
              "Cabin", "Literata", "Public Sans", "Onest", "Figtree", "Albert Sans"]

# --------------------------------------------------------------------------
COMPOSITIONS = [
    ("product-UI stage", "h1 + one-line lede + CTA on top (left or centred), then a large product UI/screen at >= 70% width that overlaps the next section", ["saas", "ai", "app", "finance", "security", "devtool", "learning", "fitness"]),
    ("asymmetric split, artifact bleeds off the edge", "copy in the narrow third, artifact in two thirds and cropped by the viewport edge; NOT the 5fr/7fr or 1.1fr/.9fr grid"),
    ("type poster", "the h1 fills most of the first viewport (>= 9vw); the artifact starts at the fold and peeks in"),
    ("catalogue first", "the hero IS the first row of products/plans with images and prices; the h1 is a short shelf label above it", ["shop", "delivery"]),
    ("single long-read column", "one 60-70ch column like an article; artifacts are inline figures that break out wider"),
    ("sticky index sidebar", "a sticky left column (name, h1, CTA, section index) and content scrolling on the right; collapses to top-stacked on mobile"),
    ("full-bleed image with a headline block", "photo/illustration edge to edge; h1 + CTA in a solid block anchored to one corner (never centred over a gradient scrim)", ["shop", "delivery", "studio", "fitness", "app"]),
    ("fixed half + scrolling half", "left half holds the claim and CTA fixed; right half scrolls through 3-4 proofs; stacks on mobile"),
    ("bento of unequal tiles", "one dominant tile (product) plus 3-5 tiles of different sizes, each a different kind of proof; NOT equal cards"),
    ("centred stack with an oversized artifact", "centred h1 + CTA, then one artifact wider than the text column; allowed: this is a fine default when the artifact is strong"),
    ("horizontal strata", "every section is a full-bleed band with its own background and its own alignment (left, right, centred, wide)"),
    ("demo-in-hero", "the input of the product is above the fold (paste box, search, calculator, command); the h1 sits beside it", ["ai", "devtool", "finance", "learning", "saas"]),
    ("one big number", "a single figure (price, time, count) set larger than the h1 dominates the hero; h1 explains it", ["finance", "fitness", "devtool", "saas", "delivery"]),
]

COLOR_STRATEGIES = [
    ("monochrome + one spot", "every neutral derived from ONE hue (bg, text, lines); a single spot colour of a different hue used on <= 3 elements (CTA + one datum)"),
    ("high-chroma duotone", "two saturated hues roughly 120-180 deg apart carry the page; neutrals are near-white/near-black; no third accent"),
    ("near-black + pastel", "dark ground (L 8-14%), text off-white, ONE light pastel (L 80-88%) for CTA, highlights and the artifact"),
    ("saturated field", "the page background itself is the brand colour at full chroma; text is black or white for >= 4.5:1; sections may switch to white"),
    ("Swiss white + black + one primary", "pure white, true black text, one primary (red, blue or yellow) used big, not as a tiny accent"),
    ("tonal analogous", "3-4 neighbouring hues at mid lightness form bands and surfaces; no grey anywhere"),
    ("pastel field + deep ink of the same hue", "light tinted background (L 92-96%, visible chroma) and text in the same hue at L 15-25%"),
    ("image-sampled", "the palette is sampled from the hero photo/illustration; UI is neutral so the image carries colour"),
    ("alternating light/dark bands", "sections alternate a light and a dark ground of the same hue family; the CTA keeps one colour in both"),
    ("neon on mid-grey", "mid-grey ground (L 45-60%) with one fluorescent accent and black or white text; check contrast per pair"),
    ("two-tone split", "the page is literally split: hero in colour A, the rest in colour B; A and B are the brand"),
]

# Hue sectors (OKLCH-ish degrees). 20-50 (orange/amber) and 250-290 (indigo/violet)
# are where v1 and v3 converged; low-chroma 100-160 is the v2 sage. Excluded by default.
HUE_SECTORS = [
    ("red", 0, 20), ("rose / magenta", 330, 360),
    ("yellow-lime", 95, 115), ("leaf green (high chroma)", 130, 150),
    ("teal", 175, 195), ("cyan", 195, 215), ("cobalt / ultramarine", 225, 250),
    ("purple-plum", 300, 330), ("brown-oxide (only with a real reason)", 50, 70),
    ("olive-chartreuse", 70, 95),
]

THEMES = ["light", "light", "dark", "two themes with a persistent toggle"]

DENSITY = [
    ("airy poster", "few elements, h1 >= 7vw, section gaps >= 120px, body 18-20px"),
    ("catalogue dense", "body 15-16px, tight rows, many items visible, tables and lists; section gaps ~64px"),
    ("editorial medium", "body 17-18px, 1.333 type scale, 60-70ch measure"),
    ("extreme contrast", "h1 at >= 6x body size, everything else small; one dramatic jump in scale"),
    ("flat hierarchy", "h1 only ~1.6x body; hierarchy by weight, colour and position, not size"),
]

EDGES = [
    ("hairline sharp", "radius 0, 1px lines, no shadows"),
    ("soft uniform", "radius 10-14px on everything, no borders, tinted fills instead"),
    ("pill controls + square containers", "buttons/inputs fully rounded, panels and images radius 0"),
    ("big round", "containers 24-32px radius, generous padding, buttons 12px"),
    ("elevation only", "no borders anywhere; one shadow level for raised things, none otherwise"),
    ("heavy outline", "2-3px solid outlines on controls and panels; at most one offset shadow on the page"),
]

HEADLINE_SHAPES = [
    ("plain category + difference", "say what it is and how it differs: 'Invoicing for freelancers that keeps the tax apart'"),
    ("imperative to the visitor", "an instruction the visitor wants to follow"),
    ("number-led", "a true figure first (time, count, price, size)"),
    ("short name-like phrase", "2-5 words; the lede does the explaining"),
    ("the visitor's question, answered", "the h1 is the question; the lede answers it in one sentence"),
    ("kicker + claim", "a small category line above (NOT tracked uppercase) and a claim h1"),
]

# --------------------------------------------------------------------------
# Category conventions: these are NOT randomised. They are what a visitor of
# this category expects to see before acting. Missing facts -> see SKILL.md.
CATEGORIES = [
    ("devtool", r"\b(deploy|cli|api|sdk|developer|devops|hosting|ci\b|git|database|infra|server)",
     ["terminal or code is the right hero artifact - do not avoid it",
      "install / first command visible", "docs link in nav", "pricing or free-tier line", "status/changelog link if known"]),
    ("ai", r"\b(ai|gpt|llm|assistant|copilot|model)\b",
     ["the product's real input -> output shown", "what it will not do", "pricing or plan line", "sign-up CTA"]),
    ("app", r"\b(mobile app|ios|android|app\b|tracker)",
     ["a phone screen with the real UI (not an abstract object)", "store badges/links (LAUNCH TODO if missing)",
      "2-3 screens or states", "price / free tier"]),
    ("shop", r"\b(shop|store|roaster|roastery|beans|coffee|bakery|merch|buy|sells?|e-?commerce)",
     ["product photos (or art-directed photo slots)", "named products with prices", "add-to-cart / shop CTA",
      "shipping / pickup facts"]),
    ("delivery", r"\b(delivery|subscription|subscribe|box|plants?)\b",
     ["photo of what arrives", "plans with prices", "how delivery/cancel works", "start-subscription CTA"]),
    ("studio", r"\b(architect|architecture|studio|agency|design firm|practice|consultancy)",
     ["built/real work with photographs - the portfolio is the product", "services", "contact with a real address/email",
      "who is behind it"]),
    ("finance", r"\b(invoice|invoicing|accounting|bank|tax|payments?|finance|ledger|bookkeeping)",
     ["product UI with correct arithmetic", "pricing", "security / compliance facts if known", "sign-up CTA"]),
    ("security", r"\b(password|vault|encrypt|encryption|security|privacy|2fa|vpn)",
     ["the app UI the visitor will use daily (autofill, vault list)", "how encryption works in one diagram",
      "platforms supported", "pricing", "audit/proof only if real"]),
    ("learning", r"\b(learn|learning|language|course|lesson|study|flashcard|school)",
     ["a real lesson/card screen", "languages/subjects offered", "price / free tier", "start-learning CTA"]),
    ("fitness", r"\b(fitness|workout|gym|training|running|health|lifting)\b",
     ["the app screen during a workout", "what is tracked", "price / free tier", "download CTA"]),
    ("saas", r"\b(task|project|team|crm|saas|manager|board|collaborat|workflow)",
     ["product UI screenshot in a specific state", "pricing or 'free for N seats' line", "sign-up CTA", "integrations if known"]),
]


def norm(s):
    return re.sub(r"\s+", " ", s.strip().lower())


def h(brief, axis, salt):
    d = hashlib.sha256(("%s|%s|%s" % (norm(brief), axis, salt)).encode("utf-8")).digest()
    return int.from_bytes(d[:8], "big")


def pick(brief, axis, salt, pool):
    return pool[h(brief, axis, salt) % len(pool)]


def categories(brief):
    b = norm(brief)
    found = [c for c, pat, _ in CATEGORIES if re.search(pat, b)]
    return found or ["saas"]


def fits(entry_cats_only, entry_avoid, cats):
    if entry_cats_only and not set(entry_cats_only) & set(cats):
        return False
    if entry_avoid and set(entry_avoid) & set(cats):
        return False
    return True


def seed(brief, salt=0):
    cats = categories(brief)
    primary = cats[0]
    tclasses = [t for t in TYPE_CLASSES if fits(t.get("only"), t.get("avoid"), cats)]
    t = pick(brief, "type", salt, tclasses)
    fonts = sorted(t["fonts"], key=lambda f: h(brief, "font:" + f, salt))
    display_only = "display only" in t["cls"] or "brand voice" in t["cls"]
    text_face = None
    if display_only:
        tf = [f for f in TEXT_FACES if f not in t["fonts"]]
        text_face = pick(brief, "textface", salt, tf)
    comps = [c for c in COMPOSITIONS if len(c) < 3 or set(c[2]) & set(cats)]
    comp = pick(brief, "composition", salt, comps)
    color = pick(brief, "color", salt, COLOR_STRATEGIES)
    hue = pick(brief, "hue", salt, HUE_SECTORS)
    theme = pick(brief, "theme", salt, THEMES)
    dens = pick(brief, "density", salt, DENSITY)
    edge = pick(brief, "edges", salt, EDGES)
    head = pick(brief, "headline", salt, HEADLINE_SHAPES)
    conv = []
    for c, _, items in CATEGORIES:
        if c in cats:
            conv += [i for i in items if i not in conv]
    return {
        "brief": brief.strip(), "salt": salt, "categories": cats,
        "type": {"class": t["cls"], "shortlist": fonts[:5], "use": t["use"], "text_face": text_face},
        "composition": {"name": comp[0], "how": comp[1]},
        "color": {"strategy": color[0], "how": color[1], "hue": "%s (%d-%d deg)" % hue, "theme": theme},
        "density": {"name": dens[0], "how": dens[1]},
        "edges": {"name": edge[0], "how": edge[1]},
        "headline": {"shape": head[0], "how": head[1]},
        "conventions": conv,
        "primary_category": primary,
    }


def render(s):
    t = s["type"]
    lines = [
        "DESIGN SEED (brief_seed.py, salt %d) - paste into your reasoning" % s["salt"],
        "Brief: %s" % s["brief"],
        "Category: %s" % ", ".join(s["categories"]),
        "",
        "Type      : %s. Pick ONE of: %s." % (t["class"], ", ".join(t["shortlist"])),
        "            %s." % t["use"],
    ]
    if t["text_face"]:
        lines.append("            Text face: %s (or another face from a different class)." % t["text_face"])
    lines += [
        "Hero      : %s - %s." % (s["composition"]["name"], s["composition"]["how"]),
        "Colour    : %s - %s." % (s["color"]["strategy"], s["color"]["how"]),
        "            Hue family: %s. Theme: %s." % (s["color"]["hue"], s["color"]["theme"]),
        "Scale     : %s - %s." % (s["density"]["name"], s["density"]["how"]),
        "Edges     : %s - %s." % (s["edges"]["name"], s["edges"]["how"]),
        "Headline  : %s - %s." % (s["headline"]["shape"], s["headline"]["how"]),
        "",
        "Category conventions (required, not randomised):",
    ]
    lines += ["  - " + c for c in s["conventions"]]
    lines += [
        "",
        "Rules: use every axis as assigned. You may override at most TWO axes, each with one",
        "sentence naming a visitor need or category convention (not taste). An override may not",
        "land on: " + ", ".join(CONVERGED_FONTS[:12]) + "..., an orange/amber or",
        "indigo/violet CTA, a sage/grey paper ground, or artifact-first-with-h1-below.",
    ]
    return "\n".join(lines)


def main(argv):
    salt, as_json, table = 0, False, None
    args = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--salt":
            salt = int(argv[i + 1]); i += 2; continue
        if a == "--json":
            as_json = True; i += 1; continue
        if a == "--table":
            table = argv[i + 1]; i += 2; continue
        args.append(a); i += 1
    if table:
        briefs = [l.strip() for l in open(table, encoding="utf-8") if l.strip()]
        print("| brand | category | typeface (class) | hero | colour strategy | hue | theme | scale | edges | headline |")
        print("|---|---|---|---|---|---|---|---|---|---|")
        for b in briefs:
            s = seed(b, salt)
            cls = s["type"]["class"].split(" (")[0].split(" +")[0]
            print("| %s | %s | %s (%s) | %s | %s | %s | %s | %s | %s | %s |" % (
                b.split(" - ")[0], s["primary_category"], s["type"]["shortlist"][0], cls,
                s["composition"]["name"], s["color"]["strategy"], s["color"]["hue"].split(" (")[0],
                s["color"]["theme"].split(" with")[0], s["density"]["name"], s["edges"]["name"],
                s["headline"]["shape"]))
        return 0
    if not args:
        print(__doc__)
        return 2
    s = seed(" ".join(args), salt)
    print(json.dumps(s, indent=2) if as_json else render(s))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```
