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
# Colour strategies that only work on one ground fix the theme instead of the
# theme axis (a "near-black" strategy cannot ship as a light theme).
FIXED_THEME = {
    "near-black + pastel": "dark",
    "saturated field": "light (the field is the theme; no dark variant)",
    "Swiss white + black + one primary": "light",
    "pastel field + deep ink of the same hue": "light",
    "neon on mid-grey": "single theme (mid-grey ground)",
    "alternating light/dark bands": "single theme (the bands already alternate)",
}

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
    ("plain category + difference", "say what it is and how it differs, in the shape [category] for [visitor] that [one difference]"),
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
    ("app", r"\b(mobile|ios|android|iphone|phone app)\b",
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
    theme = FIXED_THEME.get(color[0]) or pick(brief, "theme", salt, THEMES)
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
