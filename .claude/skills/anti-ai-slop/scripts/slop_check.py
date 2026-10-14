#!/usr/bin/env python3
"""Static slop checker for HTML/CSS frontend output.

Usage: python3 slop_check.py FILE_OR_DIR [...] [--json] [--strict] [--contrast]

Scans .html/.htm/.css/.jsx/.tsx/.vue/.svelte files for the patterns in
references/dont-list.md: first-order AI defaults (v1 run) and the
second-order defaults agents converge on when avoiding them (v2 run).
--contrast prints every resolvable text/background and button/page pair
for the light and (if present) dark theme. Each hit is a FAIL (hard ban) or WARN (smell,
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
MONO_FAMILIES = r"family=(ibm\+plex\+mono|jetbrains\+mono|space\+mono|dm\+mono|roboto\+mono|fira\+code|source\+code\+pro)"
STATIONERY_TOK = r"--[\w-]*(pencil|ink|paper|rule|stamp|margin|vellum|graphite|newsprint)[\w-]*\s*:"

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


def hls(hexv):
    import colorsys
    r, g, b = hex_to_rgb(hexv)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h * 360, l, s


def is_blue_gray(hexv):
    if not hex_to_rgb(hexv):
        return False
    h, l, s = hls(hexv)
    return 200 <= h <= 235 and 0.08 <= s <= 0.30 and 0.55 <= l <= 0.78


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


def split_media(css):
    """Return (top_level_css, dark_media_css). Removes every @media block from
    the top level; keeps the bodies of prefers-color-scheme:dark blocks."""
    top, dark, i = [], [], 0
    for m in re.finditer(r"@media[^{]*\{", css):
        if m.start() < i:
            continue
        depth, j = 1, m.end()
        while j < len(css) and depth:
            depth += {"{": 1, "}": -1}.get(css[j], 0)
            j += 1
        top.append(css[i:m.start()])
        if re.search(r"prefers-color-scheme\s*:\s*dark", m.group(0)):
            dark.append(css[m.end():j - 1])
        i = j
    top.append(css[i:])
    return "".join(top), "\n".join(dark)


def token_maps(css):
    top, dark_css = split_media(css)
    light = {}
    for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", top):
        if re.search(r"(:root|html|body)\s*$", sel.strip()) or sel.strip() in (":root", "html"):
            light.update(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", body))
    dark = dict(light)
    found_dark = False
    for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", dark_css):
        if re.search(r":root|html|body", sel) and "data-theme=\"light\"" not in sel:
            dark.update(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", body)); found_dark = True
    for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", top):
        if "data-theme=\"dark\"" in sel or "data-theme='dark'" in sel or ".dark" in sel.split()[0:1]:
            dark.update(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", body)); found_dark = True
    return top, dark_css, light, (dark if found_dark else None)


def page_bg(rules, tokens):
    for sel, body in rules:
        if sel.strip() in ("body", "html", "html,body", "html, body", ":root"):
            m = re.search(r"background(?:-color)?\s*:\s*([^;]+)", body)
            if m:
                return resolve(m.group(1), tokens)
    return resolve("var(--bg)", tokens)


def pairs(css):
    """Yield (theme, selector, fg, bg, ratio, kind) for resolvable pairs."""
    top, dark_css, light, dark = token_maps(css)
    top_rules = re.findall(r"([^{}]+)\{([^{}]*)\}", top)
    themes = [("light", light, top_rules)]
    if dark:
        dark_rules = [(s, b) for s, b in top_rules if "data-theme=\"light\"" not in s]
        dark_rules += re.findall(r"([^{}]+)\{([^{}]*)\}", dark_css)
        themes.append(("dark", dark, dark_rules))
    for theme, tokens, rules in themes:
        if theme == "light":
            rules = [(s, b) for s, b in rules if "data-theme=\"dark\"" not in s]
        base = page_bg(rules, tokens)
        # selectors (minus pseudo-classes) that get a visible edge somewhere
        edged = {re.sub(r":[\w-]+(\([^)]*\))?", "", s).strip() for s, b in rules
                 if re.search(r"border(-[a-z]+)?\s*:\s*(?!none|0)[^;]*(solid|dashed|double|\dpx)|box-shadow\s*:\s*(?!none)", b)}
        for sel, body in rules:
            if re.search(r":root|^\s*html", sel):
                continue
            bg = re.search(r"background(?:-color)?\s*:\s*([^;]+)", body)
            fg = re.search(r"(?<![-\w])color\s*:\s*([^;]+)", body)
            if bg:
                stops = (re.findall(r"var\(--[\w-]+\)|#[0-9a-f]{3,6}\b", bg.group(1))
                         if "gradient" in bg.group(1) else [bg.group(1)])
                backs = [b for b in (resolve(s, tokens) for s in stops) if b and hex_to_rgb(b)]
            else:
                # text without its own background sits on an unknown ancestor;
                # only the page-level body color is checked against the page
                backs = [base] if base and fg and sel.strip() in ("body", "main") else []
            f = resolve(fg.group(1), tokens) if fg else None
            if f and hex_to_rgb(f):
                for b in backs:
                    yield theme, sel.strip(), f, b, contrast(hex_to_rgb(f), hex_to_rgb(b)), "text"
            # non-text boundary: a filled button against the page, no border
            if (bg and backs and base and hex_to_rgb(base)
                    and re.search(r"(btn|button|cta)", sel) and "border" not in body
                    and re.sub(r":[\w-]+(\([^)]*\))?", "", sel).strip() not in edged):
                for b in backs:
                    yield theme, sel.strip(), b, base, contrast(hex_to_rgb(b), hex_to_rgb(base)), "boundary"


def check_contrast(css, hits):
    seen = set()
    for theme, sel, f, b, r, kind in pairs(css):
        key = (theme, f, b, kind)
        if key in seen:
            continue
        seen.add(key)
        if kind == "text" and r < 4.5:
            hits.append(("FAIL", "a11y", f"[{theme}] low contrast {r:.2f}:1 ({f} on {b}) in `{sel[:40]}`"))
        elif kind == "boundary" and r < 3:
            lvl = "FAIL" if r < 1.5 else "WARN"
            hits.append((lvl, "a11y", f"[{theme}] button boundary {r:.2f}:1 ({f} on page {b}) in `{sel[:40]}`"))


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
    blue_gray = sorted({h for h in re.findall(r"(?<![-\w])color\s*:\s*(#[0-9a-f]{6})\b", css)
                        + [v.strip() for k, v in re.findall(r"(--[\w-]*(?:muted|dim|soft|subtle|secondary)[\w-]*)\s*:\s*(#[0-9a-f]{6})", css)]
                        if is_blue_gray(h)})
    if blue_gray:
        add("FAIL", "color", "blue-gray muted text " + ", ".join(blue_gray[:4]) + " - tint neutrals toward the brand hue")
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
        if not re.search(r"<(img|svg|picture|video|canvas)[\s>]", low):
            if re.search(r'role="img"[^>]*aria-label|aria-label="[^"]+"[^>]*role="img"', low):
                add("WARN", "imagery", "no image/SVG - hero artifact is CSS-drawn (role=img); fine if it shows a real state")
            else:
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
        tm = re.search(r"<title>\s*([^<–|:-]+)", text, re.I)
        brand = tm.group(1).strip() if tm else None
        if brand and re.match(rf"\s*{re.escape(brand)}\s+(is|turns|helps|makes|lets)\b", lead, re.I):
            add("WARN", "copy", f"hero lead opens with '{brand} is/turns/helps…'")

    # =================== second-order defaults (v2 run) ===================
    if is_page:
        # ---- typography
        has_code = re.search(r"<(pre|code|kbd|samp)[\s>]", low)
        if re.search(MONO_FAMILIES, low):
            if not has_code:
                add("FAIL", "type", "monospace web font loaded but the page shows no code/terminal")
            else:
                add("WARN", "type", "monospace face loaded - keep it inside code/terminal elements only")
        if re.search(r"(nav|footer|masthead|colophon|kicker|eyebrow|label|tag)[^{}]*\{[^}]*(mono|monospace)", css):
            add("WARN", "type", "mono used for nav/footer/labels")
        if re.search(r"family=newsreader", low):
            add("WARN", "type", "Newsreader - second-order default serif")
        if re.search(r"<h1[^>]*>[^<]*<(em|i|mark)\b|<h1[^>]*>[^<]*<span class=\"[^\"]*(accent|em|hl|highlight)", low):
            add("WARN", "type", "emphasized fragment inside h1")
        if re.search(r"letter-spacing\s*:\s*-0?\.01[0-5]em", css):
            add("WARN", "type", "h1 tracking -.010–.015em (v2 stock value)")
        if re.search(r"max-width\s*:\s*3[2-6](ch|rem|em)\b", css):
            add("WARN", "type", "lede measure ~34ch/rem/em (v2 stock value)")
        n_upper = len(re.findall(r"text-transform\s*:\s*uppercase", css))
        if n_upper >= 4:
            add("WARN", "type", f"{n_upper} uppercase label rules - one label style, two uses max")

        # ---- layout
        if re.search(r"minmax\(\s*0\s*,\s*5fr\s*\)\s+minmax\(\s*0\s*,\s*[6-8]fr\s*\)", css):
            add("WARN", "layout", "5fr/7fr split hero (v2 stock split)")
        if len(re.findall(r"max\(\s*(16px|1rem)\s*,\s*4vw\s*\)|clamp\(\s*(16px|1rem)\s*,\s*4vw\s*,\s*[^)]+\)", css)) >= 3:
            add("WARN", "layout", "one 4vw gutter on every section - the old .wrap with a new number")
        if re.search(r"repeat\(\s*auto-fit\s*,\s*minmax\(\s*1[0-2]rem\s*,\s*1fr\s*\)\s*\)", css):
            add("WARN", "layout", "auto-fit minmax(11rem,1fr) multi-column footer grid")
        n_rules = len(re.findall(r"border-(top|bottom)\s*:\s*1px\s+solid", css))
        if n_rules >= 5:
            add("WARN", "layout", f"{n_rules} 1px row rules - ruled rows used as the default form?")

        # ---- color / tokens
        if len(set(re.findall(STATIONERY_TOK, css))) >= 3:
            add("WARN", "color", "stationery token vocabulary (ink/paper/rule/pencil) - renamed --fg/--bg/--line")
        top, dark_css, light_t, dark_t = token_maps(css)
        top_rules = re.findall(r"([^{}]+)\{([^{}]*)\}", top)
        bg = page_bg(top_rules, light_t)
        if bg and hex_to_rgb(bg):
            h, l, s = hls(bg)
            if 60 <= h <= 170 and s < 0.25 and 0.84 <= l <= 0.95:
                add("WARN", "color", f"sage/grey-green paper background {bg}")
        if dark_t:
            dbg = page_bg(top_rules, dark_t)
            if dbg and hex_to_rgb(dbg):
                h, l, s = hls(dbg)
                if 90 <= h <= 170 and l <= 0.12:
                    add("WARN", "color", f"green-black dark background {dbg}")
        if re.search(r"--[\w-]*(pencil|margin|strike|oxblood)[\w-]*\s*:\s*#", css):
            add("WARN", "color", "pencil/margin/oxblood red accent token")

        # ---- theme
        if re.search(r"\[data-theme", css) and not re.search(r"(setattribute\(\s*['\"]data-theme|dataset\.theme)", low):
            add("FAIL", "code", "[data-theme] selectors but no toggle sets data-theme")

        # ---- effects
        skeuo = [n for n, pat in (
            ("rotation", r"transform\s*:\s*rotate\(-?[0-9.]+deg\)"),
            ("ruled gradient", r"repeating-linear-gradient"),
            ("clip-path", r"clip-path\s*:\s*polygon"),
            ("offset shadow", r"box-shadow\s*:\s*-?\d+px\s+-?\d+px\s+0(px)?\s"),
            ("stamp", r"\.(stamp|seal)\b")) if re.search(pat, css)]
        if len(skeuo) >= 3:
            add("WARN", "effects", f"{len(skeuo)} skeuomorphic effects stacked ({', '.join(skeuo)}) - pick one")

        # ---- proof / destinations
        ph = re.findall(r"\[[A-Z][A-Z0-9 ,/&'.-]* NEEDED\]", text)
        if len(ph) > 2:
            add("FAIL", "copy", f"{len(ph)} visible [… NEEDED] placeholders - cut those sections, max 2")
        if re.search(r'(href|content|action|src)="[^"]*\.(example|invalid|test)\b', low):
            add("FAIL", "code", ".example/.invalid domain in a link, form or meta - use a supplied URL or cut it")
        if re.search(r'href="tel:\+?1?0{7,}', low):
            add("FAIL", "code", "fake tel: link")
        if re.search(r'href="mailto:[^"]*\?subject=(privacy|terms|legal)', low):
            add("WARN", "code", "mailto posing as a legal page")
        if re.search(r'property="og:image"\s+content="(data:|[^"]*\.example)|content="(data:[^"]*)"\s+property="og:image"', low):
            add("FAIL", "code", "og:image is a data: URI or .example URL - omit it until there is a host")
        if re.search(r'id="(yr|year|y)"\s*>\s*</span>', low):
            add("WARN", "code", "empty year span - blank without JS; put the year in as fallback")

        # ---- copy (headings + visible text)
        for hm in re.findall(r"<h[12][^>]*>(.*?)</h[12]>", text, flags=re.S | re.I):
            h_txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", hm)).strip()
            if re.fullmatch(r"(?:[\w'’]+\.\s+){2,}[\w'’]+\.?", h_txt):
                add("FAIL", "copy", f"staccato 'X. Y. Z.' heading: “{h_txt}”")
                break
            if re.search(r"\b\w+, \w+,? (and|or) \w+", h_txt):
                add("WARN", "copy", f"heading built on a list of three: “{h_txt[:60]}”")
                break
        n_count = len(re.findall(r"<h2[^>]*>\s*(?:<[^>]+>\s*)*(one|two|three|four|five|six|seven|eight)\b", low))
        if n_count:
            add("WARN", "copy", f"{n_count} count-led h2 ('Four passes…')")
        vl = visible.lower()
        if re.search(r"\bwhat happens (after|in|when|next)\b", vl):
            add("WARN", "copy", "'What happens after…' formula")
        if re.search(r">\s*see (the|what|where|one|how|our|a)\b[^<]{0,40}<", low):
            add("WARN", "copy", "'See …' secondary link")
        if re.search(r">\s*[a-z]+ your first [a-z]+", low):
            add("WARN", "copy", "'[Verb] your first [noun]' CTA formula")
        if re.search(r"deploy your first app|pick a roast|book a site visit|\$17 a bag|ships within 48 hours of roasting", low):
            add("FAIL", "copy", "copied an example from the skill verbatim")
        if re.search(r"\btry it\b", vl):
            add("WARN", "copy", "'Try it' widget prompt")
        n_disc = len(re.findall(r"\b(sample|illustrative|prototype|placeholder|made-up|fictional)\b", vl))
        if n_disc >= 3:
            add("WARN", "copy", f"{n_disc} sample/prototype disclaimers - one caption per artifact")
        if re.search(r"desk[- ]lamp", low):
            add("WARN", "color", "'desk lamp' dark theme narrative")

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
    if "--contrast" in argv:
        for f in walk([a for a in argv if not a.startswith("--")]):
            print(f"\n{f}")
            css = extract_css(open(f, encoding="utf-8", errors="replace").read(), f).lower()
            seen = set()
            for theme, sel, fg, bg, r, kind in pairs(css):
                if (theme, fg, bg, kind) in seen:
                    continue
                seen.add((theme, fg, bg, kind))
                need = 4.5 if kind == "text" else 3
                mark = "ok  " if r >= need else "FAIL"
                print(f"  {mark} {theme:5} {kind:8} {r:5.2f}:1  {fg} on {bg}  `{sel[:50]}`")
        return 0
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
