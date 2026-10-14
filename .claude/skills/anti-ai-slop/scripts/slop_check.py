#!/usr/bin/env python3
"""Static slop checker for HTML/CSS frontend output.

Usage: python3 slop_check.py FILE_OR_DIR [...] [--json] [--strict]

Scans .html/.htm/.css/.jsx/.tsx/.vue/.svelte files for the patterns in
references/dont-list.md. Each hit is a FAIL (hard ban) or WARN (smell,
needs a human reason). Exit code is 1 if any FAIL is found (or any WARN
with --strict). Stdlib only.
"""
import json
import os
import re
import sys

EXTS = (".html", ".htm", ".css", ".jsx", ".tsx", ".vue", ".svelte")

# Exact hexes that are Tailwind palette defaults commonly reached for.
TAILWIND_HEXES = {
    "#6366f1", "#4f46e5", "#4338ca", "#818cf8", "#a5b4fc",  # indigo
    "#8b5cf6", "#7c3aed", "#a78bfa", "#6d28d9",              # violet
    "#a855f7", "#9333ea", "#c084fc",                         # purple
    "#ec4899", "#db2777",                                    # pink
    "#3b82f6", "#2563eb", "#60a5fa",                         # blue
    "#06b6d4", "#22d3ee", "#0ea5e9",                         # cyan/sky
    "#10b981", "#14b8a6", "#2dd4bf", "#0f766e", "#4ade80", "#22c55e",
    "#f59e0b", "#f97316", "#ef4444",
    "#0f172a", "#1e293b", "#334155", "#64748b", "#94a3b8", "#cbd5e1",
    "#e2e8f0", "#f1f5f9", "#f8fafc",                         # slate
    "#111827", "#1f2937", "#374151", "#6b7280", "#9ca3af", "#e5e7eb",
    "#f3f4f6", "#f9fafb",                                    # gray
}
STOCK_NAVY = {"#0b1020", "#0b0f1a", "#141b33", "#131a30", "#0a0e1a", "#0d1117"}
SLOP_MUTED = re.compile(r"#9aa[0-9a-f]{3}\b", re.I)

COPY_FAIL = [
    (r"\bsupercharge", "buzzword 'Supercharge'"),
    (r"\bunlock (the|your)\b", "buzzword 'Unlock your/the'"),
    (r"\bseamless(ly)?\b", "buzzword 'seamless'"),
    (r"\brevolutioni[sz]e", "buzzword 'revolutionize'"),
    (r"\belevate your\b", "buzzword 'Elevate your'"),
    (r"\beffortless(ly)?\b", "buzzword 'effortless'"),
    (r"\bgame[- ]chang", "buzzword 'game-changer'"),
    (r"\bunleash\b", "buzzword 'unleash'"),
    (r"\bempower", "buzzword 'empower'"),
    (r"\bnext[- ]level\b", "buzzword 'next-level'"),
    (r"\bcutting[- ]edge\b", "buzzword 'cutting-edge'"),
    (r"\beverything you need\b", "'Everything you need…' heading"),
    (r">\s*ready to [^<]{1,40}\?\s*<", "'Ready to…?' closing heading"),
    (r"no credit card required", "'No credit card required.' filler"),
    (r">\s*see features\s*<", "generic secondary CTA 'See features'"),
    (r">\s*see how it works\s*<", "generic secondary CTA 'See how it works'"),
    (r">\s*get started( free| today| now)?\s*<", "generic CTA 'Get started'"),
    (r">\s*(start|try it) (for )?free\s*<", "generic CTA 'Start/Try free'"),
    (r"all rights reserved", "'All rights reserved' footer filler"),
    (r"\b(maya|sarah|alex|john|jane) [a-z]\.", "placeholder-looking testimonial name"),
    (r"northwind|acme corp|lorem ipsum", "placeholder company/text"),
]
COPY_WARN = [
    (r"\b(instant(ly)?|one[- ](click|tap))\b", "vague speed claim (instant/one click) - give a measured fact"),
    (r"\bsmart [a-z]+", "'Smart X' filler"),
    (r"\bsimple pricing\b", "'Simple pricing' heading"),
    (r"\b\d+(\.\d+)?[km]\+\s", "round '+' stat (2M+, 10K+) - is it real?"),
    (r"\b(join|trusted by) (thousands|millions|\d)", "social-proof claim - is it real?"),
]

EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF⭐⬆↔-⇿]"
)


def strip_tags(html):
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    return re.sub(r"<[^>]+>", " ", html)


def extract_css(text, path):
    if path.endswith(".css"):
        return text
    blocks = re.findall(r"<style[^>]*>(.*?)</style>", text, flags=re.S | re.I)
    inline = re.findall(r'style="([^"]*)"', text)
    return "\n".join(blocks) + "\n" + "\n".join("x{%s}" % s for s in inline)


def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        return None
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def luminance(rgb):
    def ch(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


NAMED = {"white": "#ffffff", "#fff": "#ffffff", "black": "#000000", "#000": "#000000"}


def resolve(value, tokens, depth=0):
    value = value.strip().lower()
    m = re.match(r"var\(\s*(--[\w-]+)", value)
    if m and depth < 5:
        tok = tokens.get(m.group(1))
        return resolve(tok, tokens, depth + 1) if tok else None
    value = NAMED.get(value, value)
    m = re.match(r"#[0-9a-f]{3,6}\b", value)
    return m.group(0) if m else None


def check_contrast(css, hits):
    """Approximate: per rule block with both a solid background and a color."""
    # light-theme tokens only (first :root block outside media queries)
    root = re.search(r"(?<![\w-]):root\s*\{([^}]*)\}", css)
    tokens = dict(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", root.group(1))) if root else {}
    for sel, body in re.findall(r"([^{}@]+)\{([^{}]*)\}", css):
        bg = re.search(r"background(?:-color)?\s*:\s*([^;]+)", body)
        fg = re.search(r"(?<![-\w])color\s*:\s*([^;]+)", body)
        if not (bg and fg):
            continue
        f = resolve(fg.group(1), tokens)
        if "gradient" in bg.group(1):
            # check text against every color stop; the worst stop counts
            stops = re.findall(r"var\(--[\w-]+\)|#[0-9a-f]{3,6}\b", bg.group(1))
            backs = [resolve(s, tokens) for s in stops]
        else:
            backs = [resolve(bg.group(1), tokens)]
        rf = hex_to_rgb(f) if f else None
        if not rf:
            continue
        worst = None
        for b in backs:
            rb = hex_to_rgb(b) if b else None
            if rb:
                r = contrast(rb, rf)
                if worst is None or r < worst[0]:
                    worst = (r, b)
        if worst and worst[0] < 4.5:
            hits.append(("FAIL", "a11y", f"low contrast {worst[0]:.2f}:1 ({f} on {worst[1]}) in `{sel.strip()[:40]}`"))


def check(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    low = text.lower()
    css = extract_css(text, path).lower()
    is_page = path.endswith((".html", ".htm"))
    hits = []

    def add(level, cat, msg):
        hits.append((level, cat, msg))

    # ---- Layout
    for m in re.finditer(r"max-width\s*:\s*(\d+)px", css):
        if 1000 <= int(m.group(1)) <= 1100 and re.search(r"\.(wrap|container|wrapper)\b", css):
            add("WARN", "layout", f"one global wrapper at max-width:{m.group(1)}px - choose widths per section")
            break
    if re.search(r"repeat\(\s*auto-(fit|fill)\s*,\s*minmax\(\s*2[0-9]{2}px\s*,\s*1fr", css):
        add("FAIL", "layout", "auto-fit minmax(2xxpx,1fr) card grid - pick a form for the content")
    if re.search(r"grid-template-columns\s*:\s*1\.1fr\s+\.9fr", css):
        add("WARN", "layout", "split hero 1.1fr .9fr")

    # ---- Color
    if all(re.search(rf"--{t}\s*:", css) for t in ("bg", "muted", "card")):
        add("FAIL", "color", "generic token set --bg/--muted/--card - name tokens for this product's roles")
    found = sorted({h for h in re.findall(r"#[0-9a-f]{6}\b", css) if h in TAILWIND_HEXES})
    if found:
        add("FAIL", "color", "stock Tailwind hexes: " + ", ".join(found[:8]))
    navy = sorted({h for h in re.findall(r"#[0-9a-f]{6}\b", css) if h in STOCK_NAVY})
    if navy:
        add("FAIL", "color", "stock dark navy: " + ", ".join(navy))
    if SLOP_MUTED.search(css):
        add("FAIL", "color", "blue-gray muted text #9aa*** - tint neutrals toward the brand hue")
    if re.search(r"--accent-?2\s*:", css):
        add("WARN", "color", "--accent2 token (usually exists only for a gradient)")
    if re.search(r"linear-gradient\(\s*1[23]5deg\s*,\s*var\(--accent", css):
        add("FAIL", "color", "135deg accent→accent2 gradient")
    if re.search(r"background-clip\s*:\s*text", css):
        add("FAIL", "effects", "gradient-clipped text")

    # ---- Typography
    if is_page:
        has_font = re.search(r"fonts\.googleapis|fonts\.bunny|@font-face|use\.typekit|fontshare", low)
        if not has_font:
            add("FAIL", "type", "no typeface loaded - system-ui only")
        elif re.search(r"family=inter[:&\"']", low):
            add("WARN", "type", "Inter loaded - is it chosen for this product or a safe default?")
    if re.search(r"clamp\(\s*2\.[0-9]+rem\s*,\s*[56](\.\d+)?vw\s*,\s*3\.[5-9]+rem", css):
        add("WARN", "type", "stock h1 clamp(2.xrem, 5-6vw, 3.5-4rem)")
    if re.search(r"font-weight\s*:\s*800", css):
        add("WARN", "type", "weight 800 used - by choice or by reflex?")

    # ---- Components
    if re.search(r"padding\s*:\s*1[23]px\s+2[2-6]px", css):
        add("WARN", "components", "stock button padding 12-13px x 22-26px")
    if re.search(r"\.(btn-?)?ghost\b|\.btn-outline\b|\.btn\.secondary", css):
        add("WARN", "components", "solid + ghost button pair")
    if re.search(r'class="[^"]*logo[^"]*"[^>]*>[^<]*<span', low):
        add("FAIL", "components", "split two-tone wordmark (Brand<span>name</span>)")
    if re.search(r"©\s*20\d\d", text) or re.search(r"&copy;\s*20\d\d", low):
        add("WARN", "copy", "hardcoded copyright year")

    # ---- Motion / a11y
    if is_page:
        if "transition" not in css:
            add("FAIL", "motion", "no transition on interactive states")
        if ":focus-visible" not in css:
            add("FAIL", "a11y", "no :focus-visible style")
        if "prefers-reduced-motion" not in css and re.search(r"animation|@keyframes|scroll-behavior", css):
            add("FAIL", "a11y", "motion without prefers-reduced-motion")
        if not re.search(r"<main[\s>]", low):
            add("FAIL", "a11y", "no <main> landmark")
        if not re.search(r'href="#(main|content)', low):
            add("WARN", "a11y", "no skip link")
        if not re.search(r'<meta[^>]+name="description"', low):
            add("WARN", "code", "no meta description")
        if not re.search(r'property="og:', low):
            add("WARN", "code", "no Open Graph tags")
        if not re.search(r'<link[^>]+rel="[^"]*icon', low):
            add("WARN", "imagery", "no favicon")
        if not re.search(r"<(img|svg|picture|video)[\s>]", low):
            add("FAIL", "imagery", "no image, SVG or video anywhere")
        n = len(re.findall(r'href="#"', low))
        if n:
            add("FAIL", "code", f'{n} dead link(s) href="#"')
        levels = [int(h) for h in re.findall(r"<h([1-6])[\s>]", low)]
        for a, b in zip(levels, levels[1:]):
            if b > a + 1:
                add("WARN", "a11y", f"heading level skip h{a} → h{b}")
                break
        if len(re.findall(r"<h1[\s>]", low)) != 1:
            add("WARN", "a11y", "page should have exactly one <h1>")
        n = len(re.findall(r'\sstyle="', low))
        if n >= 3:
            add("WARN", "code", f"{n} inline style patches")

    # ---- Copy / emoji (visible text only)
    visible = strip_tags(text) if is_page or path.endswith((".jsx", ".tsx", ".vue", ".svelte")) else ""
    emojis = EMOJI.findall(visible)
    if emojis:
        add("FAIL", "imagery", f"{len(emojis)} emoji in visible text ({''.join(sorted(set(emojis))[:8])})")
    for pat, msg in COPY_FAIL:
        if re.search(pat, low):
            add("FAIL", "copy", msg)
    for pat, msg in COPY_WARN:
        if re.search(pat, visible.lower()):
            add("WARN", "copy", msg)
    # list of three in the first paragraph after the h1
    m = re.search(r"</h1>.*?<p[^>]*>(.*?)</p>", text, flags=re.S | re.I)
    if m:
        lead = re.sub(r"<[^>]+>", "", m.group(1))
        if re.search(r"\b\w+, \w+,? (and|or) \w+", lead) or len(re.findall(r"\b[Nn]o \w+[,.]", lead)) >= 3:
            add("WARN", "copy", f"hero lead built on a list of three: “{lead.strip()[:70]}”")
        if re.match(r"\s*[A-Z][\w ]{1,20} (is|turns|helps|makes|lets) ", lead):
            add("WARN", "copy", "hero lead opens with '[Brand] is/turns/helps…'")

    check_contrast(css, hits)
    return hits


def walk(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "dist", "build")]
                for f in sorted(files):
                    if f.endswith(EXTS):
                        yield os.path.join(root, f)
        elif p.endswith(EXTS):
            yield p


def main(argv):
    as_json = "--json" in argv
    strict = "--strict" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        print(__doc__)
        return 2
    report, bad = {}, False
    for f in walk(paths):
        hits = check(f)
        report[f] = [{"level": l, "category": c, "message": m} for l, c, m in hits]
        fails = sum(1 for h in hits if h[0] == "FAIL")
        warns = len(hits) - fails
        if fails or (strict and warns):
            bad = True
        if not as_json:
            print(f"\n{f}  —  {fails} FAIL, {warns} WARN")
            for l, c, m in sorted(hits, key=lambda h: (h[0] != "FAIL", h[1])):
                print(f"  {l:4} [{c}] {m}")
    if as_json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
