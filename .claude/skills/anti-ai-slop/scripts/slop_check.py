#!/usr/bin/env python3
"""Static slop checker for landing pages and other HTML/CSS frontend output.

Usage:
  python3 slop_check.py FILE_OR_DIR [...]          per-page FAIL/WARN report
        [--json]      machine-readable report
        [--strict]    exit 1 on any WARN too
  python3 slop_check.py --contrast FILE_OR_DIR     every resolved text/background
                                                   pair per theme + coverage
  python3 slop_check.py --corpus DIR [DIR ...]     per-page fingerprints, values
                                                   shared by >30% of pages, and
                                                   matches against known templates
  python3 slop_check.py --render FILE_OR_DIR       load each page at 360x740 in
                                                   Chromium (Playwright) and check
                                                   the first viewport

What it checks: the first-order AI defaults (v1 run), the later-order
defaults agents converged on when avoiding them (v2, v3 runs), colour bans by
OKLab distance and region (not exact hex), converged fonts, DOM-based contrast
for every text element, category conventions (prices, photos, phone screen,
terminal) and the presence of a real conversion. Patterns run on code with
comments removed; copy rules run on visible text only.

Each hit is a FAIL (hard ban) or a WARN (a smell that needs a human reason).
Never clear a WARN by nudging a value: WARNs describe shapes, and the colour
and font rules match by distance.

Seed stamp: paste the last line of brief_seed.py's output into the page,
  <!-- seed: "<brief>" salt=N -->
The checker recomputes that seed and (a) does not WARN on values the seed
assigned (colours inside the assigned OKLCH hue range, its edges, fonts,
template features), (b) WARNs "seed not followed" [seed:font] / [seed:hue]
when the page uses another font or accent hue without a
<!-- seed override: <axis> <reason> --> comment. No stamp: WARN [seed:none].

Keeping a WARN: every WARN prints a key, e.g. WARN [color:tailwind-near].
  <!-- slop-ok: color:tailwind-near <reason of >= 4 words> -->
turns that WARN into an OK* line showing the reason. A FAIL is never kept. Exit code 1 if any FAIL (or WARN with
--strict). Python 3.7+ stdlib only; --render optionally uses Playwright.
"""
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
EXTS = (".html", ".htm", ".css", ".jsx", ".tsx", ".vue", ".svelte")

try:  # optional: share the converged-font list with the seed script
    sys.dont_write_bytecode = True
    sys.path.insert(0, HERE)
    import brief_seed as _seed  # noqa: E402
except Exception:  # pragma: no cover - the checker must work without it
    _seed = None
finally:
    if sys.path and sys.path[0] == HERE:
        sys.path.pop(0)


# =============================================================================
# 1. Constants
# =============================================================================

# Exact hexes that are Tailwind palette defaults commonly reached for.
TAILWIND_HEXES = {
    "#6366f1": "indigo-500", "#4f46e5": "indigo-600", "#4338ca": "indigo-700",
    "#818cf8": "indigo-400", "#a5b4fc": "indigo-300",
    "#8b5cf6": "violet-500", "#7c3aed": "violet-600", "#a78bfa": "violet-400", "#6d28d9": "violet-700",
    "#a855f7": "purple-500", "#9333ea": "purple-600", "#c084fc": "purple-400",
    "#ec4899": "pink-500", "#db2777": "pink-600",
    "#3b82f6": "blue-500", "#2563eb": "blue-600", "#60a5fa": "blue-400",
    "#06b6d4": "cyan-500", "#22d3ee": "cyan-400", "#0ea5e9": "sky-500",
    "#10b981": "emerald-500", "#14b8a6": "teal-500", "#2dd4bf": "teal-400", "#0f766e": "teal-700",
    "#4ade80": "green-400", "#22c55e": "green-500",
    "#f59e0b": "amber-500", "#f97316": "orange-500", "#ef4444": "red-500",
    "#0f172a": "slate-900", "#1e293b": "slate-800", "#334155": "slate-700", "#64748b": "slate-500",
    "#94a3b8": "slate-400", "#cbd5e1": "slate-300", "#e2e8f0": "slate-200", "#f1f5f9": "slate-100",
    "#f8fafc": "slate-50",
    "#111827": "gray-900", "#1f2937": "gray-800", "#374151": "gray-700", "#6b7280": "gray-500",
    "#9ca3af": "gray-400", "#e5e7eb": "gray-200", "#f3f4f6": "gray-100", "#f9fafb": "gray-50",
}
# Swatches that converged in earlier runs. A colour within DELTA_E of one is
# the same choice, nudged.
BANNED_SWATCHES = {
    "#0b1020": "stock navy", "#0b0f1a": "stock navy", "#141b33": "stock navy",
    "#131a30": "stock navy", "#0a0e1a": "stock navy", "#0d1117": "stock navy (GitHub dark)",
    "#ebebe8": "v2 grey paper", "#e9eee0": "v2 sage paper", "#121c17": "v2 green-black",
}
STOCK_NAVY = {k for k, v in BANNED_SWATCHES.items() if v.startswith("stock navy")}
DELTA_E = 0.05

CONVERGED_FONTS = [
    "inter", "space grotesk", "newsreader", "ibm plex sans", "ibm plex mono",
    "jetbrains mono", "barlow", "barlow semi condensed", "barlow condensed",
    "archivo", "fraunces", "bitter", "zilla slab", "roboto slab", "poppins",
    "montserrat", "dm sans", "manrope", "plus jakarta sans", "playfair display",
    "oswald",
]
if _seed is not None:
    try:
        CONVERGED_FONTS += [f.lower() for f in _seed.CONVERGED_FONTS if f.lower() not in CONVERGED_FONTS]
    except Exception:
        pass
CONVERGED_PREFIXES = ("ibm plex", "barlow", "archivo")

MONO_FAMILIES = r"family=(ibm\+plex\+mono|jetbrains\+mono|space\+mono|dm\+mono|roboto\+mono|fira\+code|source\+code\+pro)"
STATIONERY_TOK = r"--[\w-]*(pencil|ink|paper|rule|stamp|margin|vellum|graphite|newsprint)[\w-]*\s*:"

# (pattern, message, whole) - whole=True: must be the whole text of a
# button/link/heading/paragraph; otherwise searched in the visible text.
COPY_FAIL = [
    (r"\bsupercharge", "buzzword 'Supercharge'", False),
    (r"\bunlock (the|your)\b", "buzzword 'Unlock your/the'", False),
    (r"\bseamless(ly)?\b", "buzzword 'seamless'", False),
    (r"\brevolutioni[sz]e", "buzzword 'revolutionize'", False),
    (r"\belevate your\b", "buzzword 'Elevate your'", False),
    (r"\beffortless(ly)?\b", "buzzword 'effortless'", False),
    (r"\bgame[- ]chang", "buzzword 'game-changer'", False),
    (r"\bunleash\b", "buzzword 'unleash'", False),
    (r"\bempower", "buzzword 'empower'", False),
    (r"\bnext[- ]level\b", "buzzword 'next-level'", False),
    (r"\bcutting[- ]edge\b", "buzzword 'cutting-edge'", False),
    (r"\beverything you need\b", "'Everything you need…' heading", False),
    (r"ready to .{1,40}\?", "'Ready to…?' closing heading", True),
    (r"no credit card required", "'No credit card required.' filler", False),
    (r"see features", "generic secondary CTA 'See features'", True),
    (r"see how it works", "generic secondary CTA 'See how it works'", True),
    (r"get started( free| today| now)?\W*", "generic CTA 'Get started'", True),
    (r"(start|try it) (for )?free\W*", "generic CTA 'Start/Try free'", True),
    (r"all rights reserved", "'All rights reserved' footer filler", False),
    (r"\b(maya|sarah|alex|john|jane) [a-z]\.", "placeholder-looking testimonial name", False),
    (r"northwind|acme corp|lorem ipsum", "placeholder company/text", False),
]
COPY_WARN = [
    (r"\b(instant(ly)?|one[- ](click|tap))\b", "vague speed claim (instant/one click) - give a measured fact", "copy:instant"),
    (r"\bsmart [a-z]+", "'Smart X' filler", "copy:smart-x"),
    (r"\bsimple pricing\b", "'Simple pricing' heading", "copy:simple-pricing"),
    (r"\b\d+(\.\d+)?[km]\+\s", "round '+' stat (2M+, 10K+) - is it real?", "copy:round-stat"),
    (r"\b(join|trusted by) (thousands|millions|\d)", "social-proof claim - is it real?", "copy:social-proof"),
]
DISCLAIMERS = r"(?i:\bnot (?:yet )?connected\b|\bnothing is sent\b|\bpre-launch\b|\bprototype\b|\bnot released\b)|\[[^\]]{1,60}\bNEEDED\]"

EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF⭐⬆↔-⇿]")

# Category inference: keyword hits weighted by where they occur (title/h1 >
# meta description/lede > body). A category needs a title/h1 hit or >= 2 hits
# in title/meta/h1/lede; the highest score wins. Order breaks ties.
CATEGORY_RULES = [
    ("shop", r"(?<!app )(?<!play )\bstore\b|\b(shop|coffee|beans|roaster|roastery|bakery|merch)\b"),
    ("delivery", r"\bplants?\b|\bdelivery\b|\bdelivers?\b|\bsubscription box\b"),
    ("devtool", r"\b(deploy\w*|cli|api|sdk|developers?|devops|git|ci/cd|health check|rollbacks?)\b"),
    ("security", r"\b(passwords?|vault|encrypt\w*|cybersecurity|security|zero-knowledge|2fa|vpn)\b"),
    ("finance", r"\b(invoic\w*|accounting|bookkeeping|ledger|tax(es)?|payroll|banking)\b"),
    ("fitness", r"\b(fitness|workouts?|gym|training|running|lifting|reps)\b"),
    ("learning", r"\b(learn\w*|language|lessons?|course|flashcards?|vocabulary)\b"),
    ("ai", r"\b(ai|gpt|llm|assistant|copilot)\b"),
    ("app", r"\b(mobile|ios|android|iphone|ipad|app store|google play|play store|phone app)\b|(?<!web )\bapp\b"),
    ("studio", r"\b(studio|architect\w*|agency)\b"),
    ("saas", r"\b(task\w*|projects?|small teams|crm|saas|kanban|workflows?)\b"),
]
MOBILE_CATS = ("app", "fitness", "learning")

LAUNCH_CONST = re.compile(r"^[A-Z][A-Z0-9_]*_(URL|HREF|LINK)$")


# =============================================================================
# 2. Colour: parsing, sRGB -> OKLab/OKLCH, contrast, regions
# =============================================================================

NAMED_RGB = {
    "white": (1, 1, 1), "black": (0, 0, 0), "red": (1, 0, 0), "green": (0, .5, 0), "blue": (0, 0, 1),
    "yellow": (1, 1, 0), "orange": (1, .647, 0), "gray": (.5, .5, .5), "grey": (.5, .5, .5),
    "silver": (.75, .75, .75), "navy": (0, 0, .5), "purple": (.5, 0, .5), "teal": (0, .5, .5),
    "maroon": (.5, 0, 0), "olive": (.5, .5, 0), "lime": (0, 1, 0), "aqua": (0, 1, 1), "cyan": (0, 1, 1),
    "fuchsia": (1, 0, 1), "magenta": (1, 0, 1), "whitesmoke": (.96, .96, .96), "ivory": (1, 1, .94),
    "canvas": (1, 1, 1), "canvastext": (0, 0, 0),
}
COLOR_TOKEN = re.compile(
    r"#[0-9a-f]{3,8}\b|(?:rgba?|hsla?|oklch|oklab)\([^()]*\)|(?<![-\w])(?:%s|transparent)(?![-\w])" % "|".join(NAMED_RGB))


def _num(s, scale=1.0):
    s = s.strip()
    if s.endswith("%"):
        return float(s[:-1]) / 100 * scale
    if s in ("none", ""):
        return 0.0
    return float(s.rstrip("deg"))


def parse_color(s):
    """CSS colour string -> (r, g, b, a) in 0..1, or None if unknown."""
    if s is None:
        return None
    s = s.strip().lower()
    if s == "transparent":
        return (0.0, 0.0, 0.0, 0.0)
    if s in NAMED_RGB:
        return tuple(NAMED_RGB[s]) + (1.0,)
    m = re.fullmatch(r"#([0-9a-f]{3,8})", s)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h)
        if len(h) not in (6, 8):
            return None
        a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
        return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)) + (a,)
    m = re.fullmatch(r"(rgba?|hsla?|oklch|oklab)\((.*)\)", s)
    if not m:
        return None
    fn, args = m.group(1), m.group(2)
    if "var(" in args or "calc(" in args or "from " in args:
        return None
    parts = [p for p in re.split(r"[\s,/]+", args.strip()) if p]
    try:
        alpha = _num(parts[3]) if len(parts) > 3 else 1.0
        if fn.startswith("rgb"):
            rgb = tuple(_num(p, 255) / 255 for p in parts[:3])
        elif fn.startswith("hsl"):
            import colorsys
            h = _num(parts[0]) / 360
            sat, light = _num(parts[1], 1), _num(parts[2], 1)
            sat = sat / 100 if sat > 1 else sat
            light = light / 100 if light > 1 else light
            rgb = colorsys.hls_to_rgb(h % 1, light, sat)
        elif fn == "oklch":
            L = _num(parts[0], 1)
            L = L / 100 if L > 1 else L
            C, H = _num(parts[1], 0.4), _num(parts[2])
            rgb = oklab_to_srgb((L, C * math.cos(math.radians(H)), C * math.sin(math.radians(H))))
        else:
            L = _num(parts[0], 1)
            rgb = oklab_to_srgb((L, _num(parts[1], 0.4), _num(parts[2], 0.4)))
    except (ValueError, IndexError):
        return None
    return tuple(min(1.0, max(0.0, c)) for c in rgb) + (min(1.0, max(0.0, alpha)),)


def to_hex(c):
    return "#%02x%02x%02x" % tuple(int(round(v * 255)) for v in c[:3])


def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _gam(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def oklab(c):
    r, g, b = (_lin(v) for v in c[:3])
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (math.copysign(abs(x) ** (1 / 3), x) for x in (l, m, s))
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def oklab_to_srgb(lab):
    L, a, b = lab
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    rgb = (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
           -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
           -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)
    return tuple(_gam(min(1, max(0, v))) for v in rgb)


def oklch(c):
    L, a, b = oklab(c)
    return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


def delta_e(c1, c2):
    return math.dist(oklab(c1), oklab(c2)) if hasattr(math, "dist") else \
        math.sqrt(sum((x - y) ** 2 for x, y in zip(oklab(c1), oklab(c2))))


def luminance(c):
    r, g, b = (_lin(v) for v in c[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def over(fg, bg):
    """Composite fg (with alpha) over an opaque bg."""
    a = fg[3] if len(fg) > 3 else 1.0
    return tuple(fg[i] * a + bg[i] * (1 - a) for i in range(3)) + (1.0,)


def hue_in(h, lo, hi):
    return lo <= h <= hi if lo <= hi else (h >= lo or h <= hi)


# One hue table shared with brief_seed.py (seed sectors are assigned inside
# these buckets and outside the banned regions). Local copy if it is missing.
ACCENT_BUCKETS = [("red", 345, 32), ("orange-amber-yellow", 32, 95), ("lime-green", 95, 160),
                  ("teal-cyan", 160, 225), ("blue", 225, 262), ("indigo-violet", 262, 300),
                  ("magenta-pink", 300, 345)]
BANNED_HUES = {"orange": (32, 95), "indigo": (262, 300)}
if _seed is not None:
    try:
        ACCENT_BUCKETS = [tuple(b) for b in _seed.ACCENT_BUCKETS]
        for lo, hi, label in _seed.BANNED_HUES:
            BANNED_HUES["indigo" if "indigo" in label else "orange"] = (lo, hi)
    except Exception:
        pass


# Banned regions, in OKLCH (L 0-1, C ~0-0.37, H degrees).
def is_indigo_violet(c):
    L, C, H = oklch(c)
    return C >= 0.12 and hue_in(H, *BANNED_HUES["indigo"]) and 0.3 <= L <= 0.85


def is_orange_amber(c):
    L, C, H = oklch(c)
    return C >= 0.10 and hue_in(H, *BANNED_HUES["orange"]) and L >= 0.6


def is_sage_ground(c):
    L, C, H = oklch(c)
    if C > 0.03 and H < 115:        # light yellow-cream / pale chartreuse, not grey-green
        return False
    return L >= 0.82 and 0.006 <= C <= 0.06 and hue_in(H, 95, 185)


def is_cool_grey_ground(c):
    L, C, H = oklch(c)
    return 0.78 <= L <= 0.955 and 0.003 <= C <= 0.03 and hue_in(H, 190, 265)


def is_green_black(c):
    L, C, H = oklch(c)
    return L <= 0.28 and C >= 0.006 and hue_in(H, 120, 200)


def is_navy_ground(c):
    L, C, H = oklch(c)
    return L <= 0.26 and C >= 0.025 and hue_in(H, 250, 285)


def is_blue_gray_text(c):
    L, C, H = oklch(c)
    return 0.45 <= L <= 0.80 and 0.02 <= C <= 0.08 and hue_in(H, 230, 275)


def hue_bucket(c, neutral_c=0.03):
    L, C, H = oklch(c)
    if C < neutral_c:
        return "neutral"
    for name, lo, hi in ACCENT_BUCKETS:
        if hue_in(H, lo, hi):
            return name
    return "neutral"


def ground_bucket(c):
    L, C, H = oklch(c)
    tone = "light" if L >= 0.6 else ("mid" if L >= 0.4 else "dark")
    if C < 0.004:
        return tone + " neutral"
    if C < 0.035:
        fam = "warm" if hue_in(H, 20, 110) else "green" if hue_in(H, 110, 190) else \
            "cool" if hue_in(H, 190, 290) else "rose"
        return "%s %s-grey" % (tone, fam)
    return "%s %s" % (tone, hue_bucket(c))


# =============================================================================
# 3. Source preprocessing: comments, CSS parsing, var() resolution
# =============================================================================

def comments(raw):
    """All comment texts (HTML, CSS, JS) - used for LAUNCH TODO / seed override."""
    out = re.findall(r"<!--(.*?)-->", raw, flags=re.S)
    out += re.findall(r"/\*(.*?)\*/", raw, flags=re.S)
    out += re.findall(r"(?<![:\"'\w\\])//([^\n]*)", "\n".join(
        re.findall(r"<script[^>]*>(.*?)</script>", raw, flags=re.S | re.I)))
    return out


def strip_comments(raw, is_css=False):
    """Remove HTML comments, CSS /* */ comments, and JS // comments in scripts."""
    if is_css:
        return re.sub(r"/\*.*?\*/", " ", raw, flags=re.S)
    text = re.sub(r"<!--.*?-->", " ", raw, flags=re.S)
    text = re.sub(r"(<style[^>]*>)(.*?)(</style>)",
                  lambda m: m.group(1) + re.sub(r"/\*.*?\*/", " ", m.group(2), flags=re.S) + m.group(3),
                  text, flags=re.S | re.I)

    def js(m):
        body = re.sub(r"/\*.*?\*/", " ", m.group(2), flags=re.S)
        body = re.sub(r"(?<![:\"'\w\\])//[^\n]*", " ", body)
        return m.group(1) + body + m.group(3)
    return re.sub(r"(<script[^>]*>)(.*?)(</script>)", js, text, flags=re.S | re.I)


def extract_css(text, path):
    if path.endswith(".css"):
        return text
    blocks = re.findall(r"<style[^>]*>(.*?)</style>", text, flags=re.S | re.I)
    inline = re.findall(r'style="([^"]*)"', text)
    return "\n".join(blocks) + "\n" + "\n".join("x{%s}" % s for s in inline)


def split_top(s, sep):
    """Split on sep outside parentheses, brackets and quotes."""
    out, cur, depth, quote = [], [], 0, None
    for ch in s:
        if quote:
            cur.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
        elif ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        elif ch == sep and depth == 0:
            out.append("".join(cur))
            cur = []
            continue
        cur.append(ch)
    out.append("".join(cur))
    return out


def parse_decls(body):
    decls = []
    for part in split_top(body, ";"):
        if ":" not in part:
            continue
        prop, _, val = part.partition(":")
        prop = prop.strip().lower()
        val = val.strip()
        imp = False
        if val.lower().endswith("!important"):
            val, imp = val[:-10].strip(), True
        if prop and val:
            decls.append((prop, val, imp))
    return decls


class Rule:
    __slots__ = ("sel", "decls", "media", "order", "parsed")

    def __init__(self, sel, decls, media, order):
        self.sel, self.decls, self.media, self.order, self.parsed = sel, decls, media, order, None


def _match_brace(css, i):
    depth, j = 1, i
    while j < len(css) and depth:
        c = css[j]
        if c in "\"'":
            k = css.find(c, j + 1)
            j = k if k > 0 else j
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        j += 1
    return j


def parse_css(css, media=(), out=None):
    """Flatten a stylesheet into Rules. @media/@supports/@layer bodies recurse
    (their conditions recorded); @keyframes/@font-face/@property are skipped."""
    out = [] if out is None else out
    i, n = 0, len(css)
    while i < n:
        j = css.find("{", i)
        semi = css.find(";", i)
        if j < 0:
            break
        prelude = css[i:j].strip()
        if prelude.startswith("@") and 0 <= semi < j:   # @import ...;
            i = semi + 1
            continue
        end = _match_brace(css, j + 1)
        body = css[j + 1:end - 1]
        if prelude.startswith("@"):
            name = re.match(r"@([\w-]+)", prelude)
            name = name.group(1).lower() if name else ""
            if name in ("media", "supports", "layer", "container", "document"):
                cond = prelude if name == "media" else ""
                parse_css(body, media + ((cond,) if cond else ()), out)
        elif "{" not in body:
            out.append(Rule(prelude, parse_decls(body), media, len(out)))
        i = end
    return out


def media_applies(conds, theme, width):
    for cond in conds:
        c = cond.lower()[6:].strip()
        ok_any = False
        for alt in split_top(c, ","):
            alt = alt.strip()
            neg = alt.startswith("not ")
            alt = re.sub(r"^(not|only)\s+", "", alt)
            ok = True
            for term in re.split(r"\band\b", alt):
                term = term.strip().strip("()").strip()
                if not term or term in ("screen", "all"):
                    continue
                if term == "print":
                    ok = False
                    continue
                m = re.match(r"prefers-color-scheme\s*:\s*(\w+)", term)
                if m:
                    ok &= (m.group(1) == theme)
                    continue
                m = re.match(r"(max|min)-width\s*:\s*([\d.]+)(px|em|rem)?", term)
                if m:
                    px = float(m.group(2)) * (16 if m.group(3) in ("em", "rem") else 1)
                    ok &= (width <= px) if m.group(1) == "max" else (width >= px)
                    continue
                m = re.match(r"width\s*([<>]=?)\s*([\d.]+)(px|em|rem)?", term)
                if m:
                    px = float(m.group(2)) * (16 if m.group(3) in ("em", "rem") else 1)
                    ok &= eval("%s %s %s" % (width, m.group(1), px))  # noqa: S307 (numbers only)
                    continue
                ok = False      # reduced-motion, hover, orientation...: not the default state
            ok_any |= (ok != neg)
        if not ok_any:
            return False
    return True


def resolve_vars(value, vars_, depth=0):
    """Replace var(--x, fallback) recursively. None if a var cannot resolve."""
    if value is None or "var(" not in value:
        return value
    out, i = [], 0
    while True:
        j = value.find("var(", i)
        if j < 0:
            out.append(value[i:])
            break
        out.append(value[i:j])
        k, d = j + 4, 1
        while k < len(value) and d:
            d += {"(": 1, ")": -1}.get(value[k], 0)
            k += 1
        name, _, fb = value[j + 4:k - 1].partition(",")
        v = vars_.get(name.strip().lower())
        if v is None:
            v = fb.strip() if fb else None
        if v is None or depth > 8:
            return None
        v = resolve_vars(v, vars_, depth + 1)
        if v is None:
            return None
        out.append(v)
        i = k
    return "".join(out)


def length_px(val, parent_px, root_px=16.0, vw=1280.0, vh=900.0):
    """Evaluate a CSS length (incl. clamp/min/max/calc) to px; None if unknown."""
    if val is None:
        return None
    v = val.strip().lower()
    kw = {"xx-small": 9, "x-small": 10, "small": 13, "medium": 16, "large": 18, "x-large": 24,
          "xx-large": 32, "xxx-large": 48}
    if v in kw:
        return float(kw[v])
    if v == "smaller":
        return parent_px * 0.83
    if v == "larger":
        return parent_px * 1.2
    if v in ("inherit", "unset", "initial"):
        return parent_px
    units = {"px": 1, "rem": root_px, "em": parent_px, "%": parent_px / 100, "vw": vw / 100,
             "vh": vh / 100, "vmin": min(vw, vh) / 100, "vmax": max(vw, vh) / 100, "svh": vh / 100,
             "dvh": vh / 100, "lvh": vh / 100, "ch": parent_px * 0.5, "ex": parent_px * 0.5,
             "pt": 4 / 3, "cqi": vw / 100}

    def rep(m):
        return repr(float(m.group(1)) * units.get(m.group(2) or "px", 1))
    expr = re.sub(r"(-?\d*\.?\d+)(px|rem|em|%|vw|vh|vmin|vmax|svh|dvh|lvh|ch|ex|pt|cqi)?\b", rep, v)
    expr = expr.replace("%", "")
    expr = expr.replace("calc(", "(").replace("clamp(", "_c(")
    if not re.fullmatch(r"[\d.+\-*/(),\s e_cminax]*", expr) or re.search(r"[a-z]{2,}", expr.replace("_c", "").replace("min", "").replace("max", "")):
        return None
    try:
        r = eval(expr, {"__builtins__": {}}, {"_c": lambda a, b, c: max(a, min(b, c)), "min": min, "max": max})  # noqa: S307
        return float(r)
    except Exception:
        return None


# =============================================================================
# 4. DOM: a tolerant tree from html.parser
# =============================================================================

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param",
        "source", "track", "wbr"}
BLOCKS = {"address", "article", "aside", "blockquote", "div", "dl", "fieldset", "figure", "footer",
          "form", "h1", "h2", "h3", "h4", "h5", "h6", "header", "hr", "main", "nav", "ol", "p", "pre",
          "section", "table", "ul", "figcaption", "details", "menu"}
AUTO_CLOSE = {"p": BLOCKS, "li": {"li"}, "dt": {"dt", "dd"}, "dd": {"dt", "dd"}, "option": {"option"},
              "tr": {"tr"}, "td": {"td", "th", "tr"}, "th": {"td", "th", "tr"}}
NO_TEXT = {"script", "style", "template", "noscript", "head", "title", "option", "textarea"}


class Node:
    __slots__ = ("tag", "attrs", "children", "parent", "classes", "style")

    def __init__(self, tag, attrs, parent):
        self.tag, self.parent, self.children = tag, parent, []
        self.attrs = {k.lower(): (v if v is not None else "") for k, v in attrs}
        self.classes = set(self.attrs.get("class", "").lower().split())
        self.style = {}

    @property
    def elems(self):
        return [c for c in self.children if isinstance(c, Node)]

    def iter(self):
        yield self
        for c in self.children:
            if isinstance(c, Node):
                yield from c.iter()

    def find_all(self, *tags):
        return [n for n in self.iter() if n.tag in tags]

    def find(self, *tags):
        for n in self.iter():
            if n.tag in tags:
                return n
        return None

    def text(self):
        parts = []
        for c in self.children:
            if isinstance(c, Node):
                if c.tag not in NO_TEXT:
                    parts.append(c.text())
            else:
                parts.append(c)
        return re.sub(r"\s+", " ", " ".join(parts)).strip()

    def direct_text(self):
        return re.sub(r"\s+", " ", " ".join(c for c in self.children if isinstance(c, str))).strip()

    def ancestors(self):
        p = self.parent
        while p is not None:
            yield p
            p = p.parent

    def in_tag(self, *tags):
        return any(a.tag in tags for a in self.ancestors())

    def describe(self):
        d = self.tag
        if self.attrs.get("id"):
            d += "#" + self.attrs["id"]
        elif self.classes:
            d += "." + ".".join(sorted(self.classes)[:2])
        return d


class DomBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#document", [], None)
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        while len(self.stack) > 1 and self.stack[-1].tag in AUTO_CLOSE and tag in AUTO_CLOSE[self.stack[-1].tag]:
            self.stack.pop()
        node = Node(tag, attrs, self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        node = Node(tag, attrs, self.stack[-1])
        self.stack[-1].children.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def build_dom(html):
    b = DomBuilder()
    try:
        b.feed(html)
        b.close()
    except Exception:
        pass
    return b.root


def visible_nodes(root):
    """Text nodes a visitor can read (no head/script/style/hidden/svg title)."""
    out = []

    def walk(n):
        if n.tag in NO_TEXT or "hidden" in n.attrs or (n.tag in ("title", "desc") and n.in_tag("svg")):
            return
        for c in n.children:
            if isinstance(c, Node):
                walk(c)
            else:
                t = re.sub(r"\s+", " ", c).strip()
                if t:
                    out.append(t)
    walk(root)
    return out


# =============================================================================
# 5. Selector matching (simple and compound selectors, all four combinators)
# =============================================================================

class Unsupported(Exception):
    pass


STATE_PSEUDO = {"hover", "focus", "focus-visible", "focus-within", "active", "visited", "target",
                "placeholder-shown", "invalid", "valid", "user-invalid", "indeterminate", "autofill",
                "fullscreen", "modal", "open", "popover-open", "default", "required", "optional",
                "read-only", "read-write", "in-range", "out-of-range"}
PSEUDO_ELEM = {"before", "after", "marker", "placeholder", "selection", "first-line", "first-letter",
               "backdrop", "file-selector-button", "cue", "-webkit-scrollbar", "-webkit-details-marker",
               "-webkit-search-cancel-button", "-webkit-inner-spin-button", "-webkit-outer-spin-button",
               "-moz-focus-inner", "-webkit-slider-thumb", "-moz-range-thumb", "-webkit-slider-runnable-track",
               "-moz-range-track", "-webkit-input-placeholder", "-moz-placeholder", "-webkit-scrollbar-thumb"}
TOKEN = re.compile(
    r"""(?P<tag>\*|[a-z][\w-]*)|\#(?P<id>[\w-]+)|\.(?P<cls>[\w-]+)"""
    r"""|\[\s*(?P<attr>[\w:-]+)\s*(?:(?P<op>[~|^$*]?=)\s*(?P<val>"[^"]*"|'[^']*'|[^\]\s]+)\s*(?:[is])?\s*)?\]"""
    r"""|(?P<colons>::?)(?P<pseudo>[\w-]+)(?P<arg>\((?:[^()]|\([^()]*\))*\))?""", re.I)


def parse_compound(s):
    comp = {"tag": None, "ids": [], "cls": [], "attrs": [], "pseudo": [], "pelem": None}
    i = 0
    while i < len(s):
        m = TOKEN.match(s, i)
        if not m:
            raise Unsupported(s)
        if m.group("tag"):
            comp["tag"] = m.group("tag").lower()
        elif m.group("id"):
            comp["ids"].append(m.group("id").lower())
        elif m.group("cls"):
            comp["cls"].append(m.group("cls").lower())
        elif m.group("attr"):
            val = m.group("val")
            if val and val[0] in "\"'":
                val = val[1:-1]
            comp["attrs"].append((m.group("attr").lower(), m.group("op"), val.lower() if val is not None else None))
        else:
            name = m.group("pseudo").lower()
            arg = m.group("arg")[1:-1] if m.group("arg") else None
            if m.group("colons") == "::" or name in ("before", "after", "first-line", "first-letter"):
                comp["pelem"] = name
            else:
                comp["pseudo"].append((name, arg))
        i = m.end()
    return comp


def parse_selector(sel):
    """'nav > a.btn' -> [(' ', comp), ('>', comp)]; raises Unsupported."""
    parts, cur, depth, comb, quote = [], "", 0, " ", None
    for ch in sel.strip():
        if quote:
            cur += ch
            quote = None if ch == quote else quote
            continue
        if ch in "\"'":
            quote = ch
        elif ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if depth == 0 and ch in " >+~\n\t":
            if cur:
                parts.append((comb, parse_compound(cur)))
                cur, comb = "", " "
            if ch in ">+~":
                comb = ch
            continue
        cur += ch
    if cur:
        parts.append((comb, parse_compound(cur)))
    if not parts:
        raise Unsupported(sel)
    return parts


def specificity(parts):
    a = b = c = 0
    for _, comp in parts:
        a += len(comp["ids"])
        b += len(comp["cls"]) + len(comp["attrs"])
        c += (1 if comp["tag"] and comp["tag"] != "*" else 0) + (1 if comp["pelem"] else 0)
        for name, arg in comp["pseudo"]:
            if name in ("not", "is", "matches", "has"):
                try:
                    sub = [specificity(parse_selector(x)) for x in split_top(arg or "", ",")]
                    s = max(sub) if sub else (0, 0, 0)
                    a, b, c = a + s[0], b + s[1], c + s[2]
                except Unsupported:
                    b += 1
            elif name != "where":
                b += 1
    return (a, b, c)


def _nth(expr, pos):
    expr = (expr or "").replace(" ", "").lower()
    if expr == "odd":
        return pos % 2 == 1
    if expr == "even":
        return pos % 2 == 0
    m = re.fullmatch(r"([+-]?\d*)n([+-]\d+)?", expr)
    if m:
        a = int(m.group(1) + "1") if m.group(1) in ("", "+", "-") else int(m.group(1))
        b = int(m.group(2) or 0)
        return (pos - b) % a == 0 and (pos - b) // a >= 0 if a else pos == b
    if re.fullmatch(r"[+-]?\d+", expr):
        return pos == int(expr)
    raise Unsupported(expr)


def match_compound(node, comp, pelem=None):
    if node.tag.startswith("#"):
        return False
    if comp["pelem"] != pelem:
        return False
    if comp["tag"] and comp["tag"] != "*" and comp["tag"] != node.tag:
        return False
    if comp["ids"] and node.attrs.get("id", "").lower() not in comp["ids"]:
        return False
    if any(c not in node.classes for c in comp["cls"]):
        return False
    for name, op, val in comp["attrs"]:
        if name not in node.attrs:
            return False
        have = node.attrs[name].lower()
        if op == "=" and have != val or op == "~=" and val not in have.split() \
                or op == "^=" and not have.startswith(val) or op == "$=" and not have.endswith(val) \
                or op == "*=" and val not in have or op == "|=" and not (have == val or have.startswith(val + "-")):
            return False
    for name, arg in comp["pseudo"]:
        if not match_pseudo(node, name, arg):
            return False
    return True


def match_pseudo(node, name, arg):
    sibs = node.parent.elems if node.parent else [node]
    pos = sibs.index(node) + 1
    if name == "root":
        return node.tag == "html"
    if name == "first-child":
        return pos == 1
    if name == "last-child":
        return pos == len(sibs)
    if name == "only-child":
        return len(sibs) == 1
    if name in ("first-of-type", "last-of-type", "only-of-type", "nth-of-type", "nth-last-of-type"):
        same = [s for s in sibs if s.tag == node.tag]
        p = same.index(node) + 1
        if name == "first-of-type":
            return p == 1
        if name == "last-of-type":
            return p == len(same)
        if name == "only-of-type":
            return len(same) == 1
        return _nth(arg, p if name == "nth-of-type" else len(same) - p + 1)
    if name == "nth-child":
        return _nth((arg or "").split(" of ")[0], pos)
    if name == "nth-last-child":
        return _nth(arg, len(sibs) - pos + 1)
    if name in ("not", "is", "where", "matches"):
        hit = any(match_complex(node, parse_selector(x)) for x in split_top(arg or "", ",") if x.strip())
        return not hit if name == "not" else hit
    if name == "has":
        subs = [parse_selector(x.strip().lstrip(">").strip()) for x in split_top(arg or "", ",") if x.strip()]
        return any(match_complex(d, s) for d in node.iter() if d is not node for s in subs)
    if name in ("link", "any-link"):
        return node.tag == "a" and "href" in node.attrs
    if name == "empty":
        return not any(isinstance(c, Node) or c.strip() for c in node.children)
    if name == "checked":
        return "checked" in node.attrs or "selected" in node.attrs
    if name == "disabled":
        return "disabled" in node.attrs
    if name == "enabled":
        return "disabled" not in node.attrs
    if name in STATE_PSEUDO:
        return False
    if name in ("lang", "dir", "defined", "scope"):
        return True
    raise Unsupported(name)


def match_complex(node, parts, i=None, pelem=None):
    i = len(parts) - 1 if i is None else i
    comb, comp = parts[i]
    if not match_compound(node, comp, pelem if i == len(parts) - 1 else None):
        return False
    if i == 0:
        return True
    prev = parts[i][0]
    if prev == " ":
        return any(match_complex(a, parts, i - 1) for a in node.ancestors())
    if prev == ">":
        return node.parent is not None and match_complex(node.parent, parts, i - 1)
    sibs = node.parent.elems if node.parent else []
    before = sibs[:sibs.index(node)] if node in sibs else []
    if prev == "+":
        return bool(before) and match_complex(before[-1], parts, i - 1)
    return any(match_complex(s, parts, i - 1) for s in before)


# =============================================================================
# 6. Cascade-lite: computed colour, background, size and weight per element
# =============================================================================

UA_SIZE = {"h1": "2em", "h2": "1.5em", "h3": "1.17em", "h4": "1em", "h5": ".83em", "h6": ".67em",
           "small": ".83em", "sub": ".83em", "sup": ".83em", "code": ".8125em", "kbd": ".8125em",
           "samp": ".8125em", "pre": ".8125em"}
UA_BOLD = {"h1", "h2", "h3", "h4", "h5", "h6", "b", "strong", "th", "dt", "legend"}
UA_DISPLAY_NONE = {"head", "script", "style", "template", "noscript", "title", "meta", "link"}
WEIGHTS = {"normal": 400, "bold": 700, "lighter": 300, "bolder": 700}


def _strip_funcs(v, names):
    """Remove name(...) calls (paren-matched) from v; return (rest, [calls])."""
    calls, out, i = [], [], 0
    pat = re.compile(r"(?:%s)\(" % "|".join(names))
    while True:
        m = pat.search(v, i)
        if not m:
            out.append(v[i:])
            break
        out.append(v[i:m.start()])
        k, d = m.end(), 1
        while k < len(v) and d:
            d += {"(": 1, ")": -1}.get(v[k], 0)
            k += 1
        calls.append(v[m.start():k])
        i = k
    return "".join(out), calls


def parse_bg_layer(val):
    """background value(s) -> ('none',) | ('colors', [rgba..]) | ('image',) | ('unknown',) | ('inherit',).
    A gradient with transparent/translucent stops is treated as a decorative
    overlay (ruled lines, fades) and ignored; an opaque gradient gives its stops."""
    v = val.strip().lower()
    if v in ("none", "transparent", "initial", "unset", "0", "revert"):
        return ("none",)
    if v == "inherit":
        return ("inherit",)
    rest, grads = _strip_funcs(v, ["repeating-linear-gradient", "repeating-radial-gradient", "linear-gradient",
                                   "radial-gradient", "conic-gradient", "repeating-conic-gradient"])
    if "url(" in rest or "image-set(" in rest or "element(" in rest:
        return ("image",)
    if "color-mix(" in rest or "light-dark(" in rest or "from " in rest:
        return ("unknown",)
    base = None
    for t in split_top(rest.replace(",", " , "), " "):
        c = parse_color(t)
        if c is not None:
            base = c
    stops = []
    if re.search(r"no-repeat|/\s*(?!100%\s*100%|cover)[\d.]+", rest):
        grads = []            # a sized, non-repeating gradient is an underline/marker, not a ground
    for g in grads:
        cols = [parse_color(t.group(0)) for t in COLOR_TOKEN.finditer(g)]
        if not cols or any(c is None for c in cols):
            return ("unknown",) if base is None else ("colors", [base])
        if all(c[3] >= 1 for c in cols):
            stops = cols
    if stops:
        return ("colors", stops)
    if base is not None:
        return ("colors", [base]) if base[3] > 0 else ("none",)
    if grads:
        return ("none",)      # translucent overlay only: the parent shows through
    return ("none",) if not re.search(r"[a-z]{3,}\(|#", rest) else ("unknown",)


def border_edge(decls_get, side_only_ok=False):
    """Colour string of a full border / outline / ring shadow, or None.
    Only a border on all four sides counts unless side_only_ok."""
    cands = []
    for prop in ("border", "outline"):
        v = decls_get(prop)
        if v and not re.match(r"\s*(none|0|hidden)\b", v):
            cands.append(v)
    if decls_get("border-color") and decls_get("border-style") not in (None, "none", "hidden"):
        if not re.match(r"\s*0\b", decls_get("border-width") or "1px"):
            cands.append(decls_get("border-color").split()[0])
    sh = decls_get("box-shadow")
    if sh and re.match(r"\s*(inset\s+)?0(px)?\s+0(px)?\s+0(px)?\s+[1-9]", sh):
        cands.append(sh)
    if side_only_ok:
        for side in ("border-bottom", "border-top"):
            v = decls_get(side)
            if v and not re.match(r"\s*(none|0)\b", v):
                cands.append(v)
    for v in cands:
        for t in COLOR_TOKEN.finditer(v.lower()):
            return t.group(0)
        if "currentcolor" in v.lower():
            return "currentcolor"
    return None


class Styler:
    """Computes styles for one theme at one viewport width."""

    def __init__(self, page, theme, width=1280):
        self.page, self.theme, self.width = page, theme, width
        self.rules = [r for r in page.rules if media_applies(r.media, theme, width)]
        self.pseudo_rules = [r for r in self.rules if any(parts[-1][1]["pelem"] in ("before", "after")
                                                          for parts, _ in r.parsed)]
        self.styles, self.svg_shapes = {}, {}

    def declared_pseudo(self, node, pelem):
        out = {}
        for r in self.pseudo_rules:
            for parts, spec in r.parsed:
                try:
                    if match_complex(node, parts, pelem=pelem):
                        out.update({p: v for p, v, _ in r.decls})
                        break
                except Unsupported:
                    continue
        return out

    def matched(self, node, pelem=None):
        out = []
        for r in self.rules:
            for parts, spec in r.parsed:
                try:
                    if match_complex(node, parts, pelem=pelem):
                        out.append((spec, r.order, r.decls))
                        break
                except Unsupported:
                    continue
        out.sort(key=lambda x: (x[0], x[1]))
        return out

    def declared(self, node, pelem=None):
        normal, important = {}, {}
        for spec, order, decls in self.matched(node, pelem):
            for prop, val, imp in decls:
                (important if imp else normal)[prop] = val
        if pelem is None and node.attrs.get("style"):
            for prop, val, imp in parse_decls(node.attrs["style"].lower()):
                (important if imp else normal)[prop] = val
        normal.update(important)
        return normal

    def compute(self):
        root = self.page.dom
        html = root.find("html") or root
        for n in (html, root.find("body")):
            if n is not None:
                n.attrs["data-theme"] = self.theme
                if self.page.dark_class:
                    n.classes.discard("dark")
                    n.classes.discard("light")
                    n.classes.add(self.theme)
        canvas = {"vars": {}, "color": (0, 0, 0, 1), "eff_bg": [(1, 1, 1, 1)], "bg_note": None,
                  "px": 16.0, "weight": 400, "fill": "black", "hidden": False, "off": False,
                  "display": "block", "svg": None, "decl": {}}
        self._walk(root, canvas)
        return self.styles

    def _walk(self, node, ps):
        for c in node.children:
            if isinstance(c, Node):
                self._walk_el(c, ps)

    def _walk_el(self, node, ps):
        d = self.declared(node)
        st = {"decl": d}
        vars_ = dict(ps["vars"])
        for k, v in d.items():
            if k.startswith("--"):
                vars_[k] = v
        st["vars"] = vars_

        def get(prop):
            v = d.get(prop)
            return resolve_vars(v, vars_) if v is not None else None
        st["get"] = get

        disp = (get("display") or ("none" if node.tag in UA_DISPLAY_NONE else "")).split()
        st["display"] = disp[0] if disp else ("inline" if node.tag not in BLOCKS else "block")
        st["hidden"] = ps["hidden"] or st["display"] == "none" or "hidden" in node.attrs or \
            (node.tag == "dialog" and "open" not in node.attrs) or get("visibility") in ("hidden", "collapse")
        pos = get("position") or ""
        off = False
        if pos in ("absolute", "fixed"):
            for side in ("left", "top", "right"):
                v = length_px(get(side), ps["px"], vw=self.width)
                if v is not None and v <= -100:
                    off = True
            if re.search(r"rect\(\s*0|inset\(\s*50%", (get("clip") or "") + (get("clip-path") or "")):
                off = True
            w, h = length_px(get("width"), ps["px"]), length_px(get("height"), ps["px"])
            if w is not None and h is not None and w <= 1 and h <= 1:
                off = True
        if re.search(r"translate[xy]?\(\s*-1\d\d%", get("transform") or ""):
            off = True
        st["off"] = ps["off"] or off or bool(node.classes & {"sr-only", "visually-hidden", "visuallyhidden", "screen-reader-text"})

        # font size / weight
        size = get("font-size")
        if size is None and get("font"):
            m = re.search(r"([\d.]+(?:px|rem|em|%)|clamp\([^)]*\))\s*(/|\s)", get("font"))
            size = m.group(1) if m else None
        px_ = length_px(size, ps["px"], vw=self.width) if size else None
        if px_ is None:
            px_ = length_px(UA_SIZE[node.tag], ps["px"]) if node.tag in UA_SIZE and not size else ps["px"]
        st["px"] = px_
        w = get("font-weight")
        if w is None and get("font"):
            m = re.search(r"\b([1-9]00|bold|normal)\b", get("font"))
            w = m.group(1) if m else None
        if w is None:
            st["weight"] = 700 if node.tag in UA_BOLD else ps["weight"]
        else:
            st["weight"] = WEIGHTS.get(w.strip(), None) or (int(w) if w.strip().isdigit() else ps["weight"])

        # colour
        cv = get("color")
        if cv is None:
            st["color"] = ps["color"]
        else:
            cvl = cv.strip().lower()
            if cvl in ("inherit", "currentcolor", "unset", "initial"):
                st["color"] = ps["color"]
            else:
                st["color"] = parse_color(cvl)   # None = unresolved
        # svg fill (presentation attribute < CSS)
        fill = get("fill") or node.attrs.get("fill")
        st["fill"] = fill.lower().strip() if fill else ps["fill"]

        # background
        bgv = get("background-color") or get("background")
        if get("background-image") and get("background-image") != "none":
            bgv = (bgv or "") + " " + get("background-image")
        bsz = get("background-size")
        if bgv and bsz and not re.match(r"\s*(cover|100%(\s+100%)?|auto)\s*$", bsz):
            bgv += " no-repeat"
        note = ps["bg_note"]
        if d.get("background") is not None and bgv is None or d.get("background-color") is not None and bgv is None:
            layer = ("unknown",)
        else:
            layer = parse_bg_layer(bgv) if bgv else ("none",)
        if layer[0] == "image":
            eff, note = None, "background image"
        elif layer[0] == "unknown":
            eff, note = None, "unresolved background"
        elif layer[0] == "colors":
            parent = ps["eff_bg"]
            if all(c[3] >= 1 for c in layer[1]):
                eff, note = [c[:3] + (1.0,) for c in layer[1]], None
            elif parent is None:
                eff = None
            else:
                eff = [over(c, p) for c in layer[1] for p in parent]
        else:
            eff = ps["eff_bg"]
        # a ::before/::after layer with its own background sits behind the text
        if eff is not None and self.pseudo_rules:
            for pe in ("before", "after"):
                pd = self.declared_pseudo(node, pe)
                pbg = resolve_vars(pd.get("background") or pd.get("background-color"), vars_) if pd else None
                w = resolve_vars(pd.get("width", ""), vars_) or ""
                covers = "inset" in pd or ("left" in pd and "right" in pd) or ("top" in pd and "bottom" in pd) \
                    or w.strip().endswith("%")
                small = (length_px(w, st["px"]) or 999) < 40 and (length_px(pd.get("height"), st["px"]) or 999) < 40
                if pbg and parse_bg_layer(pbg)[0] != "none" and pd.get("position") in ("absolute", "fixed") \
                        and covers and not small:
                    eff, note = None, "pseudo-element background layer"
        st["own_bg"] = layer
        st["eff_bg"], st["bg_note"] = eff, note
        st["parent_bg"] = ps["eff_bg"]
        st["svg"] = node if node.tag == "svg" else ps.get("svg")
        st["svg_bg"] = None
        if st["svg"] is not None and node.tag != "svg":
            shapes = self.svg_shapes.setdefault(id(st["svg"]), [])
            fc = parse_color(st["color"] and st["fill"] == "currentcolor" and to_hex(st["color"]) or st["fill"]) \
                if st["fill"] != "none" else None
            if node.tag == "rect" and fc and fc[3] > 0:
                g = [_float(node.attrs.get(k, "0")) for k in ("x", "y", "width", "height")]
                if node.attrs.get("width", "").endswith("%"):
                    g[2] = 1e9
                if node.attrs.get("height", "").endswith("%"):
                    g[3] = 1e9
                shapes.append(("rect", g, fc))
            elif node.tag in ("circle", "ellipse", "path", "polygon", "polyline") and fc and fc[3] > 0:
                shapes.append((node.tag, None, fc))
            elif node.tag in ("text", "tspan"):
                src = node if "x" in node.attrs or node.tag == "text" else node.parent
                x, y = _float(src.attrs.get("x", "0")), _float(src.attrs.get("y", "0"))
                st["svg_bg"] = "html"
                for kind, g, fc in reversed(shapes):
                    if kind == "rect":
                        if g[0] <= x <= g[0] + g[2] and g[1] <= y - 2 <= g[1] + g[3]:
                            st["svg_bg"] = fc if fc[3] >= 1 else None
                            break
                    else:
                        st["svg_bg"] = None     # a shape we cannot place may sit behind the text
                        break
        self.styles[id(node)] = st
        self._walk(node, st)


def _float(s):
    try:
        return float(re.match(r"-?[\d.]+", s).group(0))
    except Exception:
        return 0.0


# =============================================================================
# 7. Page model
# =============================================================================

class Page:
    def __init__(self, path):
        self.path = path
        self.raw = open(path, encoding="utf-8", errors="replace").read()
        self.is_html = path.endswith((".html", ".htm"))
        self.is_css = path.endswith(".css")
        self.comments = comments(self.raw)
        self.code = strip_comments(self.raw, self.is_css)
        self.low = self.code.lower()
        self.css = extract_css(self.code, path).lower()
        self.rules = parse_css(self.css)
        self.unsupported = 0
        for r in self.rules:
            r.parsed = []
            for s in split_top(r.sel, ","):
                if not s.strip():
                    continue
                try:
                    parts = parse_selector(s.lower())
                    r.parsed.append((parts, specificity(parts)))
                except Unsupported:
                    self.unsupported += 1
        self.dom = build_dom(self.code) if self.is_html else Node("#document", [], None)
        self.dark_class = any(re.fullmatch(r"(html|:root|body)?\.dark", r.sel.strip()) for r in self.rules)
        self.has_dark = any("prefers-color-scheme: dark" in " ".join(r.media).replace(":dark", ": dark")
                            or re.search(r"data-theme\s*=\s*['\"]?dark", r.sel) for r in self.rules
                            if any(p == "color" or "background" in p or p.startswith("--") for p, _, _ in r.decls)) \
            or self.dark_class
        self.themes = ["light", "dark"] if self.has_dark else ["light"]
        if self.is_html:
            self.nodes = visible_nodes(self.dom)
        else:
            self.nodes = [t.strip() for t in re.sub(r"<[^>]+>", "\n", re.sub(
                r"<(script|style)[^>]*>.*?</\1>", " ", self.code, flags=re.S | re.I)).split("\n") if t.strip()]
        self.visible = " ".join(self.nodes)
        self._styles = {}
        self.name = os.path.basename(os.path.dirname(path)) if os.path.basename(path) == "index.html" \
            else os.path.splitext(os.path.basename(path))[0]
        self.seed, self.stamp, self.seed_error = read_seed(self.comments)
        self.suppressed = []        # (key, message) WARNs dropped because the seed assigned them

    def styles(self, theme, width=1280):
        key = (theme, width)
        if key not in self._styles:
            self._styles[key] = Styler(self, theme, width).compute()
        return self._styles[key]

    def st(self, node, theme="light", width=1280):
        return self.styles(theme, width).get(id(node))

    def blocks(self):
        """Whole text of short text-bearing elements (for whole-text copy rules)."""
        return [n.text() for n in self.dom.iter()
                if n.tag in ("a", "button", "h1", "h2", "h3", "h4", "p", "li", "label", "summary", "figcaption", "dt", "dd")]

    def families(self):
        fams = []
        for href in re.findall(r"(?:fonts\.googleapis\.com|fonts\.bunny\.net)/css2?\?([^\"')\s>]+)", self.low):
            for f in re.findall(r"family=([^&:]+)", href.replace("&amp;", "&")):
                fams.append(re.sub(r"\+|%20", " ", f).strip())
        fams += [f.strip().strip("'\"") for f in re.findall(r"@font-face\s*\{[^}]*font-family\s*:\s*([^;}]+)", self.css)]
        fams += [re.sub(r"[-+]", " ", f) for f in re.findall(r"api\.fontshare\.com[^\"']*f\[\]=([\w-]+)", self.low)]
        out = []
        for f in fams:
            if f and f not in out:
                out.append(f)
        return out

    def ctas(self):
        """Elements that look like a button / call to action (by name, role or
        styling: a link with its own fill and padding outside the nav)."""
        if hasattr(self, "_ctas"):
            return self._ctas
        out = []
        styles = self.styles("light")
        for n in self.dom.iter():
            cls = " ".join(n.classes) + " " + n.attrs.get("id", "")
            if n.tag == "button" or n.tag == "input" and n.attrs.get("type") in ("submit", "button") \
                    or n.tag == "a" and (re.search(r"\b(btn|button|cta)\b|btn-|-btn|cta-|-cta", cls)
                                         or n.attrs.get("role") == "button"):
                out.append(n)
            elif n.tag == "a" and not n.in_tag("nav") and "skip" not in n.classes:
                st = styles.get(id(n))
                if st and st["own_bg"][0] == "colors" and st["get"]("padding") and not st["off"]:
                    out.append(n)
        self._ctas = out
        return out



# =============================================================================
# 7b. Seed stamp (brief_seed.py) and slop-ok comments
# =============================================================================

STAMP_RE = re.compile(r'\bseed:\s*"((?:[^"\\]|\\.)*)"\s*salt\s*=\s*(\d+)', re.I)
SLOP_OK_RE = re.compile(r"slop-ok:\s*([\w.-]+:[\w.-]+)[ \t]*([^\n]*)", re.I)
GREEN_BLACK_HUES = (120, 200)    # is_green_black
SAGE_HUES = (95, 130)            # where a seed-assigned olive/chartreuse tint reads as sage


def read_seed(comment_texts):
    """(seed dict | None, (brief, salt) | None, error | None) from a
    <!-- seed: "<brief>" salt=N --> comment."""
    for c in comment_texts:
        m = STAMP_RE.search(c)
        if not m:
            continue
        brief = re.sub(r"\\(.)", r"\1", m.group(1))
        salt = int(m.group(2))
        if _seed is None or not hasattr(_seed, "seed"):
            return None, (brief, salt), "brief_seed.py not importable next to slop_check.py"
        try:
            s = _seed.seed(brief, salt)
        except Exception as e:  # pragma: no cover
            return None, (brief, salt), "brief_seed.seed() failed: %s" % e
        if "hue_range" not in s.get("color", {}):
            return None, (brief, salt), "brief_seed.py is too old (no OKLCH hue_range)"
        return s, (brief, salt), None
    return None, None, None


def _ranges_overlap(lo, hi, a, b):
    pts = [(lo + i) % 360 for i in range(((hi - lo) % 360) + 1)]
    return any(hue_in(x, a, b) for x in pts)


def seed_hue(p, c, tol=6, with_b=True):
    """Is colour c chromatic and inside the seed's assigned hue sector (or the
    duotone's derived hue B)?"""
    s = p.seed
    if not s or c is None or not s["color"].get("hue_range"):
        return False
    L, C, H = oklch(c)
    if C < 0.02:
        return False
    rngs = [s["color"]["hue_range"]]
    if with_b and s["color"].get("hue_b_range"):
        rngs.append(s["color"]["hue_b_range"])
    return any(hue_in(H, (lo - tol) % 360, (hi + tol) % 360) for lo, hi in rngs)


def seed_sector_overlaps(p, a, b):
    if not p.seed or not p.seed["color"].get("hue_range"):
        return False
    lo, hi = p.seed["color"]["hue_range"]
    return _ranges_overlap(lo, hi, a, b)


def seed_fonts(p):
    """(shortlist, allowed) lower-case font names from the seed."""
    t = p.seed["type"]
    short = [f.lower() for f in t["shortlist"]]
    allowed = list(short)
    if t.get("text_face"):
        allowed.append(t["text_face"].lower())
    if "display only" in t["class"] or "brand voice" in t["class"]:
        allowed += [f.lower() for f in getattr(_seed, "TEXT_FACES", [])]
    return short, allowed


def has_override(p, *words):
    for c in p.comments:
        m = re.search(r"seed override:(.*)", c, flags=re.I | re.S)
        if m and any(w.lower() in m.group(1).lower() for w in words):
            return True
    return False


def slop_oks(p):
    """{rule-key: reason} from <!-- slop-ok: <key> <reason> --> comments."""
    out = {}
    for c in p.comments:
        for m in SLOP_OK_RE.finditer(c):
            out[m.group(1).lower()] = m.group(2).strip().rstrip("-").strip()
    return out

# =============================================================================
# 8. Checks
# =============================================================================

def check_layout(p, add):
    css = p.css
    if re.search(r"\.(wrap|container|wrapper)\b", css) and any(
            1000 <= int(m) <= 1100 for m in re.findall(r"max-width\s*:\s*(\d+)px", css)):
        add("WARN", "layout", "one global wrapper width shared by every section - choose widths per section", "layout:global-wrapper")
    if re.search(r"repeat\(\s*auto-(fit|fill)\s*,\s*minmax\(\s*2[0-9]{2}px\s*,\s*1fr", css):
        add("FAIL", "layout", "auto-fit card grid (icon + h3 + line in equal cards) - pick a form for the content")
    if re.search(r"grid-template-columns\s*:\s*1\.1fr\s+\.9fr", css):
        add("WARN", "layout", "near-even copy/artifact split hero (the v1 split)", "layout:v1-split")


def declared_colors(p):
    out = {}
    for t in COLOR_TOKEN.finditer(p.css):
        c = parse_color(t.group(0))
        if c and c[3] > 0.5 and t.group(0) not in ("transparent", "white", "black"):
            out.setdefault(to_hex(c), c)
    return out


def page_ground(p, theme):
    for tag in ("body", "html", "main"):
        n = p.dom.find(tag)
        if n is None:
            continue
        st = p.st(n, theme)
        if st and st["own_bg"][0] == "colors":
            return st["eff_bg"][0] if st["eff_bg"] else None
    body = p.dom.find("body")
    st = p.st(body, theme) if body else None
    return st["eff_bg"][0] if st and st["eff_bg"] else (1, 1, 1, 1)


def same_cell(c1, c2):
    """Same (lightness, chroma, hue) cell: the shape of the colour, not its hex."""
    L1, C1, H1 = oklch(c1)
    L2, C2, H2 = oklch(c2)
    if abs(L1 - L2) > 0.05 or abs(C1 - C2) > max(0.012, 0.35 * max(C1, C2)):
        return False
    if min(C1, C2) < 0.008:
        return max(C1, C2) < 0.012
    return min(abs(H1 - H2), 360 - abs(H1 - H2)) < 25


def ground_colors(p):
    """Page grounds (every theme) and section-level backgrounds."""
    out = {}
    for theme in p.themes:
        g = page_ground(p, theme)
        if g:
            out[to_hex(g)] = g
        for n in p.dom.iter():
            if n.tag in ("section", "header", "footer", "main", "article", "aside", "body", "html"):
                st = p.st(n, theme)
                if st and st["own_bg"][0] == "colors" and st["eff_bg"] and len(st["eff_bg"]) == 1:
                    out[to_hex(st["eff_bg"][0])] = st["eff_bg"][0]
    return out


def cta_fills(p, theme="light"):
    out = []
    for n in p.ctas():
        st = p.st(n, theme)
        if st and not st["hidden"] and st["own_bg"][0] == "colors" and st["eff_bg"]:
            out.append((n, st["eff_bg"][0]))
    return out


def check_colour(p, add):
    css = p.css
    if all(re.search(rf"--{t}\s*:", css) for t in ("bg", "muted", "card")):
        add("FAIL", "color", "generic token set --bg/--muted/--card - name tokens for this product's roles")
    cols = declared_colors(p)
    exact = sorted(h for h in cols if h in TAILWIND_HEXES)
    if exact:
        add("FAIL", "color", "stock Tailwind hexes: " + ", ".join("%s (%s)" % (h, TAILWIND_HEXES[h]) for h in exact[:6]))
    near = []
    for h, c in cols.items():
        if h in TAILWIND_HEXES or oklch(c)[1] < 0.02:    # neutral greys are nobody's swatch
            continue
        for th, name in TAILWIND_HEXES.items():
            tc = parse_color(th)
            if oklch(tc)[1] >= 0.04 and delta_e(c, tc) < DELTA_E:
                if seed_hue(p, c):
                    p.suppressed.append(("color:tailwind-near", "%s ~ %s (inside the seed's hue)" % (h, name)))
                else:
                    near.append("%s ~ %s" % (h, name))
                break
    if near:
        add("WARN", "color", "nudged stock Tailwind swatches (same colour within ΔE .05): " + ", ".join(near[:5]), "color:tailwind-near")
    for h, c in ground_colors(p).items():
        for bh, label in BANNED_SWATCHES.items():
            bc = parse_color(bh)
            de = delta_e(c, bc)
            # neutral swatches: same lightness/hue cell as well as close
            limit = DELTA_E if oklch(bc)[1] >= 0.04 else 0.02
            if de < limit and same_cell(c, bc):
                lvl = "FAIL" if de < 0.01 or h in STOCK_NAVY else "WARN"
                if lvl == "WARN" and seed_ground_ok(p, c, label):
                    p.suppressed.append(("color:converged-ground", "%s ~ %s" % (h, label)))
                    break
                add(lvl, "color", "ground %s is the converged %s (ΔE %.3f) - a nudged hex is the same choice"
                    % (h, label, de), "color:converged-ground")
                break
    # regions
    indigo = sorted(h for h, c in cols.items() if is_indigo_violet(c) and h not in TAILWIND_HEXES
                    and not seed_hue(p, c, with_b=False))
    if indigo:
        add("WARN", "color", "indigo/violet accent family (%s) - the v1 default hue" % ", ".join(indigo[:3]), "color:indigo-violet")
    fills = cta_fills(p)
    orange = sorted({to_hex(c) for n, c in fills if is_orange_amber(c)})
    if not fills:
        orange = sorted(h for h, c in cols.items() if is_orange_amber(c) and re.search(
            r"--[\w-]*(accent|cta|primary|action|brand|button|btn)[\w-]*\s*:\s*%s" % h, css))
    if orange:
        add("WARN", "color", "orange/amber/safety-yellow CTA fill (%s) - the v3 converged action colour" % ", ".join(orange[:3]), "color:orange-cta")
    for theme in p.themes:
        g = page_ground(p, theme)
        if not g:
            continue
        hx = to_hex(g)
        if theme == "light" and is_sage_ground(g) and not seed_ground_ok(p, g, "sage"):
            add("WARN", "color", "page ground is sage/grey-green paper (%s) - the v2 template ground" % hx, "color:sage-ground")
        if is_cool_grey_ground(g):
            add("WARN", "color", "page ground is a cool 'galvanized' grey (%s) - a v3 converged ground" % hx, "color:cool-grey-ground")
        if is_green_black(g) and not seed_ground_ok(p, g, "green-black"):
            add("WARN", "color", "[%s] page ground is green-black (%s) - the v2 dark template" % (theme, hx), "color:green-black-ground")
        if is_navy_ground(g) and hx not in STOCK_NAVY:
            add("WARN", "color", "[%s] page ground is stock navy-black (%s)" % (theme, hx), "color:navy-ground")
    texty = set(re.findall(r"(?<![-\w])color\s*:\s*(#[0-9a-f]{3,8}|rgba?\([^)]*\)|oklch\([^)]*\))", css))
    texty |= {v.strip() for v in re.findall(r"--[\w-]*(?:muted|dim|soft|subtle|secondary|quiet|faint)[\w-]*\s*:\s*([^;]+)", css)}
    bg_ = sorted({to_hex(c) for c in (parse_color(v) for v in texty) if c and is_blue_gray_text(c)})
    if bg_:
        add("FAIL", "color", "blue-gray muted text (%s) - tint neutrals toward the brand hue" % ", ".join(bg_[:4]))
    if re.search(r"--accent-?2\s*:", css):
        add("WARN", "color", "a second accent token that exists only to feed a gradient", "color:accent2-token")
    if re.search(r"linear-gradient\(\s*1[23]5deg\s*,\s*var\(--accent", css):
        add("FAIL", "color", "diagonal accent→accent2 gradient")
    if re.search(r"background-clip\s*:\s*text", css):
        add("FAIL", "effects", "gradient-clipped text")


def seed_ground_ok(p, c, label):
    """A green-black or sage ground the seed itself produced: near-black (or a
    dark theme) + an assigned green/teal hue, or an assigned olive/chartreuse
    hue on a light tint."""
    if not p.seed:
        return False
    if "green-black" in label:
        dark = p.seed["color"]["strategy"].startswith("near-black") or "dark" in p.seed["color"]["theme"] \
            or p.seed["color"]["strategy"].startswith(("alternating", "monochrome", "pastel field"))
        return dark and seed_sector_overlaps(p, *GREEN_BLACK_HUES)
    if "sage" in label:
        return seed_sector_overlaps(p, *SAGE_HUES)
    return False


def font_overridden(p, fam):
    for c in p.comments:
        m = re.search(r"seed override:(.*)", c, flags=re.I | re.S)
        if m and fam.lower() in m.group(1).lower():
            return True
    return False


def is_converged_font(f):
    f = f.lower()
    return f in CONVERGED_FONTS or f.startswith(CONVERGED_PREFIXES)


def check_type(p, add):
    css, low = p.css, p.low
    if p.is_html:
        fams = p.families()
        has_font = fams or re.search(r"use\.typekit|@font-face", low)
        if not has_font:
            add("FAIL", "type", "no typeface loaded - system-ui only")
        short, allowed = seed_fonts(p) if p.seed else ([], [])
        conv = [f for f in fams if is_converged_font(f) and not font_overridden(p, f) and f.lower() not in allowed]
        for f in conv:
            only = len(fams) == 1
            add("FAIL" if only else "WARN", "type",
                "converged font '%s'%s - a family earlier runs landed on; take the seed's class "
                "(or note 'seed override: %s' with a visitor reason)" % (f, " is the only family" if only else "", f), "type:converged-font")
        if p.seed and fams:
            has_code = p.dom.find("pre", "code", "kbd", "samp")
            own = [f for f in fams if not (has_code and re.search(r"mono|code", f, re.I))]
            t = p.seed["type"]
            stray = [f for f in own if f.lower() not in allowed]
            if not any(f.lower() in short for f in own) or (stray and not ("display only" in t["class"])):
                if not has_override(p, "font", "type", "typeface", *fams):
                    add("WARN", "seed", "seed not followed: loaded %s; the seed assigned %s (alternate %s)%s - "
                        "use it, or write <!-- seed override: font <visitor reason> -->"
                        % (", ".join(fams), t["shortlist"][0], t["shortlist"][1] if len(t["shortlist"]) > 1 else "-",
                           ", text face %s" % t["text_face"] if t.get("text_face") else ""), "seed:font")
    if re.search(r"clamp\(\s*2\.[0-9]+rem\s*,\s*[56](\.\d+)?vw\s*,\s*3\.[5-9]+rem", css):
        add("WARN", "type", "h1 sized with the stock fluid-clamp formula (v1 hero size)", "type:stock-clamp")
    if re.search(r"font-weight\s*:\s*800", css):
        add("WARN", "type", "extra-bold weight used - by choice or by reflex?", "type:weight-800")


def check_components(p, add):
    css, low = p.css, p.low
    if re.search(r"padding\s*:\s*1[23]px\s+2[2-6]px", css):
        add("WARN", "components", "stock button proportions (the v1 pill/button padding)", "components:stock-button")
    if re.search(r"\.(btn-?)?ghost\b|\.btn-outline\b|\.btn\.secondary", css):
        add("WARN", "components", "solid + ghost button pair", "components:ghost-pair")
    if re.search(r'class="[^"]*logo[^"]*"[^>]*>[^<]*<span', low):
        add("FAIL", "components", "split two-tone wordmark (Brand<span>name</span>)")
    if static_year(p):
        add("WARN", "copy", "hardcoded copyright year", "copy:static-year")


def static_year(p):
    """A '© 2026' a script does not keep current. A year inside an element
    whose id/class/data-attribute a getFullYear() script targets is the
    allowed static fallback, not a hardcoded year."""
    scripts = " ".join(re.findall(r"<script[^>]*>(.*?)</script>", p.code, flags=re.S | re.I))
    dyn = "getfullyear" in scripts.lower()
    for m in re.finditer(r"(?:©|&copy;|&#169;|&#xa9;)\s*((?:<[^>]+>\s*)*)(20\d\d)", p.code, re.I):
        tags = m.group(1)
        if dyn and tags:
            names = []
            for tag in re.findall(r"<[^/][^>]*>", tags):
                names += re.findall(r'\bid="([^"]+)"', tag)
                for cls in re.findall(r'\bclass="([^"]+)"', tag):
                    names += cls.split()
                names += re.findall(r"\b(data-[\w-]+)", tag)
            if any(re.search(r"[\"'`\[(][#.]?%s[\"'`\]=)]" % re.escape(n), scripts) for n in names):
                continue
        return True
    return False


def check_a11y_meta(p, add):
    css, low = p.css, p.low
    if "transition" not in css:
        add("FAIL", "motion", "no transition on interactive states")
    if ":focus-visible" not in css:
        add("FAIL", "a11y", "no :focus-visible style")
    if "prefers-reduced-motion" not in css and re.search(r"animation|@keyframes|scroll-behavior", css):
        add("FAIL", "a11y", "motion without prefers-reduced-motion")
    if not p.dom.find("main"):
        add("FAIL", "a11y", "no <main> landmark")
    main = p.dom.find("main")
    targets = ["main", "content"] + ([main.attrs["id"].lower()] if main is not None and main.attrs.get("id") else [])
    if not any(re.search(r'href="#%s"' % re.escape(t), low) for t in targets):
        add("WARN", "a11y", "no skip link", "a11y:skip-link")
    if not re.search(r'<meta[^>]+name="description"', low):
        add("WARN", "code", "no meta description", "code:meta-description")
    if not re.search(r'property="og:', low):
        add("WARN", "code", "no Open Graph tags", "code:og-tags")
    if not re.search(r'<link[^>]+rel="[^"]*icon', low):
        add("WARN", "imagery", "no favicon", "imagery:favicon")
    if not p.dom.find("img", "svg", "picture", "video", "canvas"):
        if re.search(r'role="img"[^>]*aria-label|aria-label="[^"]+"[^>]*role="img"', low):
            add("WARN", "imagery", "no image/SVG - hero artifact is CSS-drawn (role=img); fine if it shows a real state", "imagery:css-only")
        else:
            add("FAIL", "imagery", "no image, SVG or video anywhere")
    n = len(re.findall(r'href="#"', low))
    if n:
        add("FAIL", "code", f'{n} dead link(s) href="#"')
    levels = [int(n.tag[1]) for n in p.dom.iter() if re.fullmatch(r"h[1-6]", n.tag)]
    for a, b in zip(levels, levels[1:]):
        if b > a + 1:
            add("WARN", "a11y", f"heading level skip h{a} → h{b}", "a11y:heading-skip")
            break
    if len(p.dom.find_all("h1")) != 1:
        add("WARN", "a11y", "page should have exactly one <h1>", "a11y:one-h1")
    n = len(re.findall(r'\sstyle="', low))
    if n >= 3:
        add("WARN", "code", f"{n} inline style patches", "code:inline-style")


def check_copy(p, add):
    vis, vl = p.visible, p.visible.lower()
    blocks = [b.lower() for b in p.blocks()]
    emojis = EMOJI.findall(vis)
    if emojis:
        add("FAIL", "imagery", f"{len(emojis)} emoji in visible text ({''.join(sorted(set(emojis))[:8])})")
    for pat, msg, whole in COPY_FAIL:
        if (any(re.fullmatch(r"\s*" + pat + r"\s*", b) for b in blocks) if whole else re.search(pat, vl)):
            add("FAIL", "copy", msg)
    for pat, msg, key in COPY_WARN:
        if re.search(pat, vl):
            add("WARN", "copy", msg, key)
    if not p.is_html:
        return
    h1 = p.dom.find("h1")
    lead = None
    if h1 is not None:
        seen = False
        for n in p.dom.iter():
            if n is h1:
                seen = True
            elif seen and n.tag == "p" and not n.in_tag("h1"):
                lead = n.text()
                break
    if lead:
        if re.search(r"\b\w+, \w+,? (and|or) \w+", lead) or len(re.findall(r"\b[Nn]o \w+[,.]", lead)) >= 3:
            add("WARN", "copy", f"hero lead built on a list of three: “{lead[:70]}”", "copy:lead-list-of-three")
        tm = re.search(r"<title>\s*([^<–|:-]+)", p.code, re.I)
        brand = tm.group(1).strip() if tm else None
        if brand and re.match(rf"\s*{re.escape(brand)}\s+(is|turns|helps|makes|lets)\b", lead, re.I):
            add("WARN", "copy", f"hero lead opens with '{brand} is/turns/helps…'", "copy:lead-brand-is")
    for h in p.dom.find_all("h1", "h2"):
        t = h.text()
        if re.fullmatch(r"(?:[\w'’]+\.\s+){2,}[\w'’]+\.?", t):
            add("FAIL", "copy", f"staccato 'X. Y. Z.' heading: “{t}”")
            break
        if re.search(r"\b\w+, \w+,? (and|or) \w+", t):
            add("WARN", "copy", f"heading built on a list of three: “{t[:60]}”", "copy:heading-list-of-three")
            break
    n_count = sum(1 for h in p.dom.find_all("h2") if re.match(r"(one|two|three|four|five|six|seven|eight)\b", h.text().lower()))
    if n_count:
        add("WARN", "copy", f"{n_count} count-led h2 ('Four passes…')", "copy:count-led-h2")
    if re.search(r"\bwhat happens (after|in|when|next)\b", vl):
        add("WARN", "copy", "'What happens after…' formula", "copy:what-happens")
    links = [n.text().lower() for n in p.dom.find_all("a", "button")]
    if any(re.match(r"see (the|what|where|one|how|our|a)\b", t) for t in links):
        add("WARN", "copy", "'See …' secondary link", "copy:see-link")
    if any(re.match(r"[a-z]+ your first [a-z]+", t) for t in links + blocks):
        add("WARN", "copy", "'[Verb] your first [noun]' CTA formula", "copy:your-first")
    if re.search(r"deploy your first app|pick a roast|book a site visit|\$17 a bag|ships within 48 hours of roasting", vl):
        add("FAIL", "copy", "copied an example from the skill verbatim")
    if re.search(r"\btry it\b", vl):
        add("WARN", "copy", "'Try it' widget prompt", "copy:try-it")
    n_disc = len(re.findall(r"\b(sample|illustrative|prototype|placeholder|made-up|fictional|invented)\b", vl))
    if n_disc >= 3:
        add("WARN", "copy", f"{n_disc} sample/invented disclaimers - one caption per artifact at most", "copy:disclaimers")
    if re.search(r"desk[- ]lamp", vl):
        add("WARN", "color", "'desk lamp' dark-theme narrative", "color:desk-lamp")
    # honesty notes on the page (rule 11)
    script_strings = " ".join(re.findall(r"""(?:textContent|innerText|innerHTML)\s*=\s*([^;]+)""", " ".join(
        re.findall(r"<script[^>]*>(.*?)</script>", p.code, flags=re.S | re.I))))
    hits = re.findall(DISCLAIMERS, vis) + re.findall(DISCLAIMERS, script_strings)
    if sum(1 for h in hits if h.endswith("NEEDED]")) > 2:     # the placeholder rule reports those
        hits = [h for h in hits if not h.endswith("NEEDED]")]
    if len(hits) > 1:
        add("FAIL", "copy", "%d visible 'not connected / pre-launch / NEEDED' notes (%s) - honesty goes in the hand-off and LAUNCH TODO"
            % (len(hits), "; ".join(sorted(set(h[:28] for h in hits))[:3])))
    elif hits:
        add("WARN", "copy", "visible '%s' note - tell the user in the hand-off, not the visitor" % hits[0][:30], "copy:visible-note")


VOICE_TOKENS = {"nav", "footer", "masthead", "colophon", "kicker", "eyebrow", "label", "tag"}


def mono_voice(p):
    """A rule that sets a mono font on nav/footer/label-like selectors. Tokens
    are whole selector identifiers or their hyphen parts ('nav-link', '.tag'),
    never substrings ('stage' is not 'tag')."""
    for r in p.rules:
        if not any(prop in ("font-family", "font") and re.search(r"mono", val) for prop, val, _ in r.decls):
            continue
        for ident in re.findall(r"[a-z][\w-]*", re.sub(r"\[[^\]]*\]|\([^)]*\)", " ", r.sel)):
            if set(ident.split("-")) & VOICE_TOKENS or set(ident.split("_")) & VOICE_TOKENS:
                return True
    return False


RULE_PROPS = ("border-top", "border-bottom", "border-block", "border-block-start", "border-block-end")


def ruled_row_sections(p):
    """Sections that use ruled rows: >= 3 repeated siblings (same tag, one
    parent) that each carry a 1px top/bottom rule on themselves or on a child
    up to two levels down. Tables, the footer and one timeline do not count."""
    styles = p.styles("light", 1280)
    groups = {}
    for n in p.dom.iter():
        if n.tag in ("table", "thead", "tbody", "tfoot", "tr", "td", "th", "caption", "footer", "hr") \
                or n.in_tag("table", "footer"):
            continue
        st = styles.get(id(n))
        if not st or st["hidden"]:
            continue
        if not any(re.match(r"\s*(1px|thin)\s+(solid|dashed|dotted)", st["get"](prop) or "") for prop in RULE_PROPS):
            continue
        row, depth = n, 0
        while row is not None and depth <= 2:
            par = row.parent
            if par is not None and sum(1 for k in par.elems if k.tag == row.tag) >= 3:
                groups.setdefault(id(par), (par, set()))[1].add(id(row))
                break
            row, depth = par, depth + 1
    secs, timelines = [], []
    for par, rows in groups.values():
        if len(rows) < 3:
            continue
        chain = [par] + list(par.ancestors())
        sec = next((a for a in chain if a.tag in ("section", "article", "aside", "header")
                    or (a.parent is not None and a.parent.tag in ("main", "body"))), par)
        names = " ".join(" ".join(a.classes) + " " + a.attrs.get("id", "") for a in chain)
        if re.search(r"timeline|history|chronolog", names):
            timelines.append(id(sec))
        elif id(sec) not in secs:
            secs.append(id(sec))
    for t in timelines[1:]:       # one timeline is a fine use of rules; a second one counts
        if t not in secs:
            secs.append(t)
    return len(secs)


def check_second_order(p, add):
    """Later-order defaults (v2/v3 runs). Messages name the shape, not a value."""
    css, low = p.css, p.low
    has_code = p.dom.find("pre", "code", "kbd", "samp")
    if re.search(MONO_FAMILIES, low):
        if not has_code:
            add("FAIL", "type", "monospace web font loaded but the page shows no code/terminal")
        else:
            add("WARN", "type", "monospace face loaded - keep it inside code/terminal elements only", "type:mono-loaded")
    if mono_voice(p):
        add("WARN", "type", "mono used as the voice of nav/footer/labels", "type:mono-voice")
    h1 = p.dom.find("h1")
    if h1 is not None and any(c.tag in ("em", "i", "mark") or c.tag == "span" and c.classes & {"accent", "em", "hl", "highlight"}
                              for c in h1.elems):
        add("WARN", "type", "emphasized fragment inside the h1 (the italic/coloured-word template)", "type:h1-fragment")
    if len(re.findall(r"text-transform\s*:\s*uppercase", css)) >= 4:
        add("WARN", "type", "tracked-uppercase labels used as the page's voice - one label style, used twice at most", "type:uppercase-voice")
    if re.search(r"minmax\(\s*0\s*,\s*5fr\s*\)\s+minmax\(\s*0\s*,\s*[6-8]fr\s*\)", css):
        add("WARN", "layout", "copy-left/artifact-right split hero (the v2 template split)", "layout:v2-split")
    if len(re.findall(r"max\(\s*(16px|1rem)\s*,\s*4vw\s*\)|clamp\(\s*(16px|1rem)\s*,\s*4vw\s*,\s*[^)]+\)", css)) >= 3:
        add("WARN", "layout", "one fluid gutter repeated on every section - the old global wrapper in another form", "layout:fluid-gutter")
    if re.search(r"repeat\(\s*auto-fit\s*,\s*minmax\(\s*1[0-2]rem\s*,\s*1fr\s*\)\s*\)", css):
        add("WARN", "layout", "auto-fit multi-column footer grid (the v2 footer)", "layout:v2-footer")
    if re.search(r"border-(top|bottom|block)[\w-]*\s*:\s*(1px|thin)\s", css) and ruled_row_sections(p) >= 3 \
            and not (p.seed and p.seed["edges"]["name"] == "hairline sharp" and
                     not p.suppressed.append(("layout:ruled-rows", "seed edges: hairline sharp"))):
        add("WARN", "layout", "ruled rows used as the default form across sections", "layout:ruled-rows")
    if len(set(re.findall(STATIONERY_TOK, css))) >= 3:
        add("WARN", "color", "stationery token vocabulary (ink/paper/rule/pencil) - renamed --fg/--bg/--line", "color:stationery-tokens")
    if any(c and oklch(c)[1] >= 0.08 and hue_in(oklch(c)[2], 345, 40) for c in (
            parse_color(v.strip()) for v in re.findall(r"--[\w-]*(?:pencil|margin|strike|oxblood)[\w-]*\s*:\s*([^;}]+)", css))):
        add("WARN", "color", "pencil/margin/oxblood red accent token (the v2 accent)", "color:oxblood-token")
    if re.search(r"\[data-theme", css) and not re.search(r"(setattribute\(\s*['\"]data-theme|dataset\.theme)", low):
        add("FAIL", "code", "[data-theme] selectors but no toggle sets data-theme")
    skeuo = [n for n, pat in (
        ("rotation", r"transform\s*:\s*rotate\(-?[0-9.]+deg\)"),
        ("ruled gradient", r"repeating-linear-gradient"),
        ("clip-path", r"clip-path\s*:\s*polygon"),
        ("offset shadow", r"box-shadow\s*:\s*-?\d+px\s+-?\d+px\s+0(px)?\s"),
        ("stamp", r"\.(stamp|seal)\b")) if re.search(pat, css)]
    if len(skeuo) >= 3:
        add("WARN", "effects", f"{len(skeuo)} skeuomorphic effects stacked ({', '.join(skeuo)}) - pick one", "effects:skeuo-stack")
    if re.search(r"border-radius\s*:\s*(\d+px)\s+(\d+px)\s+\1\s+\2|border-radius\s*:\s*0\s+\d{2}px\s+\d{2}px\s+0", css):
        add("WARN", "components", "asymmetric 'material' radius on controls (a v3 gimmick)", "components:material-radius")
    # placeholders and destinations
    ph = re.findall(r"\[[A-Z][A-Z0-9 ,/&'.-]* NEEDED\]", p.visible)
    if len(ph) > 2:
        add("FAIL", "copy", f"{len(ph)} visible [… NEEDED] placeholders - cut those sections, max 2")
    if re.search(r'(href|content|action|src)="[^"]*\.(example|invalid|test)\b', low):
        add("FAIL", "code", ".example/.invalid domain in a link, form or meta - use a launch constant")
    if re.search(r'href="tel:\+?1?0{7,}', low):
        add("FAIL", "code", "fake tel: link")
    if re.search(r'href="mailto:[^"]*\?subject=(privacy|terms|legal)', low):
        add("WARN", "code", "mailto posing as a legal page", "code:mailto-legal")
    if re.search(r'property="og:image"\s+content="(data:|[^"]*\.example)|content="(data:[^"]*)"\s+property="og:image"', low):
        add("FAIL", "code", "og:image is a data: URI or .example URL - omit it until there is a host")
    if re.search(r'id="(yr|year|y)"\s*>\s*</span>', low):
        add("WARN", "code", "empty year span - blank without JS; put the year in as fallback", "code:empty-year")


# ---- category conventions and conversion (rules 3-4, 10) -------------------

def infer_categories(p):
    """Ranked categories. With a seed stamp, the brief's categories."""
    if p.seed:
        return list(p.seed["categories"])
    title = re.search(r"<title>(.*?)</title>", p.code, re.S | re.I)
    desc = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]*)"', p.code, re.I) or \
        re.search(r'<meta[^>]+content="([^"]*)"[^>]+name="description"', p.code, re.I)
    h1 = p.dom.find("h1")
    lede = ""
    if h1 is not None:
        seen = False
        for n in p.dom.iter():
            if n is h1:
                seen = True
            elif seen and n.tag == "p":
                lede = n.text()
                break
    top = " ".join([title.group(1) if title else "", h1.text() if h1 is not None else ""]).lower()
    mid = " ".join([desc.group(1) if desc else "", lede]).lower()
    body = p.visible.lower()
    scored, weak = [], []
    for i, (cat, pat) in enumerate(CATEGORY_RULES):
        t, m = len(re.findall(pat, top)), len(re.findall(pat, mid))
        if t or t + m >= 2:
            scored.append((3 * t + 2 * m + 0.1 * min(len(re.findall(pat, body)), 10), -i, cat))
        elif m:
            weak.append(cat)        # one mention in meta/lede: secondary only
    if scored:
        return [c for _, _, c in sorted(scored, reverse=True)] + weak
    # the page never names its category: fall back to the author's LAUNCH TODO note
    todo = " ".join(c for c in p.comments if "launch todo" in c.lower()).lower()
    for cat, pat in CATEGORY_RULES:
        if re.search(pat, todo):
            return [cat] + [w for w in weak if w != cat]
    return weak or ["saas"]


def infer_category(p):
    return infer_categories(p)[0]


def leaves_page(n):
    """Does this link/button/form take the visitor somewhere (a real conversion)?"""
    if n.tag == "form":
        a = n.attrs.get("action", "").strip()
        return bool(a) and not a.startswith("#")
    if n.attrs.get("data-href", "").strip():
        return True
    href = n.attrs.get("href", "").strip()
    if not href or href.startswith(("#", "javascript:")) or href in ("/", "./", "index.html", "/index.html"):
        return False
    if re.search(r"privacy|terms|legal|cookie|imprint|impressum", href, re.I):
        return False
    return True


def check_content(p, add):
    cats = infer_categories(p)
    cat = cats[0]
    vis = p.visible
    body = p.dom.find("body") or p.dom
    footers = set(id(x) for f in p.dom.find_all("footer") for x in f.iter())
    convs = [n for n in body.iter() if n.tag in ("a", "button", "form") and id(n) not in footers and leaves_page(n)]
    launch = [n for n in body.iter() for k in ("href", "data-href", "action") if LAUNCH_CONST.match(n.attrs.get(k, ""))]
    if not convs:
        add("FAIL", "conversion", "no primary conversion: every link and button stays on the page (in-page anchors, "
                                  "toy widgets, forms without action) - point the real CTA at a launch constant or URL")
    price = re.search(r"[$€£₺¥]\s?\d|\d[\d.,]*\s?(€|£|₺|usd|eur|gbp|tl)\b", vis, re.I) or \
        re.search(r'<data[^>]*class="[^"]*todo[^"]*"[^>]*>[^<]*\d', p.code, re.I)
    photo = p.dom.find("img", "picture", "video") or any(
        re.search(r"photo", " ".join(n.classes)) for n in p.dom.iter())
    phone = any(re.search(r"phone|device|handset|iphone", " ".join(n.classes) + " " + n.attrs.get("id", ""))
                for n in p.dom.iter())
    store = re.search(r"apps\.apple\.com|play\.google\.com|APP_STORE|PLAY_STORE|APPSTORE|app store|google play",
                      p.code, re.I)
    code = p.dom.find("pre", "code")
    tag = "[%s] " % cat
    if cat in ("shop", "delivery") and not set(cats) & set(MOBILE_CATS):
        if not price:
            add("WARN", "content", tag + "no price anywhere - a buyer of this category needs prices (draft them in <data class=\"todo\">)", "content:no-price")
        if not photo:
            add("WARN", "content", tag + "no product photo or photo slot - visitors came to see what they buy", "content:no-photo")
    if cat == "app" or ("app" in cats and cat in MOBILE_CATS):
        if not phone:
            add("WARN", "content", tag + "no phone frame showing the app's real screen", "content:no-phone")
        if not store:
            add("WARN", "content", tag + "no App Store / Google Play link (use launch constants)", "content:no-store-link")
    if cat == "devtool" and not code:
        add("WARN", "content", tag + "no <pre>/<code>: a developer expects the terminal, install step or config", "content:no-code")
    if cat == "studio" and not photo:
        add("WARN", "content", tag + "no photographs of built work - for a studio the portfolio is the product", "content:no-portfolio")
    # LAUNCH TODO bookkeeping (read from raw comments)
    todo = " ".join(c for c in p.comments if "launch todo" in c.lower())
    consts = sorted({v for n in launch for k in ("href", "data-href", "action")
                     for v in [n.attrs.get(k, "")] if LAUNCH_CONST.match(v)})
    if (consts or re.search(r'<data[^>]*class="[^"]*todo', p.code, re.I)) and not todo:
        add("WARN", "code", "launch constants or <data class=\"todo\"> values but no <!-- LAUNCH TODO --> comment listing them", "code:no-launch-todo")
    missing = [c for c in consts if todo and c not in todo]
    if missing:
        add("WARN", "code", "launch constants not listed in LAUNCH TODO: " + ", ".join(missing[:5]), "code:launch-todo-missing")
    return cat


# ---- structure: stray grid items, artifact-first hero -----------------------

ARTIFACT_TAGS = ("svg", "pre", "canvas", "video", "picture", "img", "table")


def is_big_artifact(n):
    if n.tag not in ARTIFACT_TAGS and n.attrs.get("role") != "img":
        return False
    if n.in_tag("a", "button", "label", "h1", "h2", "header", "nav", "svg", "picture"):
        return False
    if n.tag in ("svg", "img"):
        w = _float(n.attrs.get("width", "0"))
        if 0 < w <= 64 or re.search(r"icon|logo|mark", " ".join(n.classes)):
            return False
    return True


def hero_order(p):
    main = p.dom.find("main") or p.dom.find("body") or p.dom
    h1 = p.dom.find("h1")
    if h1 is None:
        return "no-h1"
    body = p.dom.find("body") or p.dom
    if main.tag == "main" and h1 not in list(main.iter()):
        # h1 outside <main>: a header/sidebar hero. Artifact-first only if a
        # big artifact comes before the h1 in DOM order.
        for n in body.iter():
            if n is h1:
                return "h1-first"
            if n is main:
                return "artifact-first"
            if is_big_artifact(n):
                return "artifact-first"
        return "h1-first"
    first = next((e for e in main.elems if e.tag not in ("script", "style", "a")), None)
    if first is not None and main.tag == "main" and h1 not in list(first.iter()) and len(first.text()) > 40 \
            and not in_side_column(p, h1):
        return "artifact-first"     # the h1 is not in the first block of <main>
    for n in main.iter():
        if n is h1:
            return "h1-first"
        if is_big_artifact(n):
            return "artifact-first"
    return "h1-first"


def in_side_column(p, n):
    """Is n in a sidebar / sticky column (aside, position: sticky|fixed, or a
    side/sidebar/sticky/index class)?"""
    for a in [n] + list(n.ancestors()):
        if a.tag == "aside" or re.search(r"(^|[-_])(side|sidebar|sticky|rail|index)([-_]|$)",
                                         " ".join(a.classes) + " " + a.attrs.get("id", "")):
            return True
        for w in (1280,):
            st = p.st(a, "light", w)
            if st and (st["get"]("position") or "").strip() in ("sticky", "fixed"):
                return True
    return False


PHRASING = {"span", "a", "em", "strong", "b", "i", "code", "small", "time", "data", "abbr", "mark", "kbd", "samp", "var", "sup", "sub"}


def grid_columns(v):
    """Number of column tracks in a grid-template-columns value (1 if unknown)."""
    v = v.split("/")[-1].strip() if "/" in v else v.strip()
    if not v or v in ("none", "auto"):
        return 1
    m = re.match(r"repeat\(\s*(\d+)\s*,", v)
    if m:
        return int(m.group(1))
    if "auto-fit" in v or "auto-fill" in v:
        return 2
    return max(1, len([t for t in split_top(re.sub(r"\[[^\]]*\]", "", v), " ") if t.strip()]))


def check_structure(p, add):
    styles = p.styles("light", 1280)
    mob = p.styles("light", 360)
    stray = []
    for n in p.dom.iter():
        for s in (styles.get(id(n)), mob.get(id(n))):
            if not s or s["display"] not in ("grid", "inline-grid") or s["hidden"]:
                continue
            bare = [c.strip() for c in n.children if isinstance(c, str) and c.strip()]
            if not bare or not n.elems:
                break
            cols = grid_columns(s["get"]("grid-template-columns") or s["get"]("grid-template") or "")
            items = len(n.elems) + sum(1 for c in n.children if isinstance(c, str) and c.strip())
            after_inline = False
            prev = None
            for c in n.children:
                if isinstance(c, Node):
                    prev = c
                elif c.strip() and prev is not None and prev.tag in PHRASING:
                    after_inline = True
            if (cols >= 2 and items > cols) or (cols == 1 and after_inline):
                stray.append((n, bare[0]))
            break
    if stray:
        n, t = stray[0]
        add("WARN", "layout", "display:grid element `%s` has bare text nodes beside its children (“%s”) - each becomes a "
                              "stray grid item; wrap the text (%d element(s))" % (n.describe(), t[:30], len(stray)), "layout:stray-grid-text")
    if hero_order(p) == "artifact-first":
        add("WARN", "layout", "artifact-first hero: make sure the h1 + primary CTA still sit in the first 360x740 viewport", "layout:artifact-first")


# ---- contrast ----------------------------------------------------------------

def text_pairs(p, theme):
    """For every element with direct text: (node, fg, [bg..], ratio, large, svg) or (node, None, reason)."""
    styles = p.styles(theme)
    out = []
    for n in p.dom.iter():
        st = styles.get(id(n))
        if st is None or n.tag in NO_TEXT or st["hidden"] or st["off"]:
            continue
        dt = n.direct_text()
        if not dt or not re.search(r"\w", EMOJI.sub("", dt)) or (n.tag in ("title", "desc") and n.in_tag("svg")):
            continue
        in_svg = n.tag in ("text", "tspan") or n.in_tag("svg")
        if in_svg:
            f = st["fill"]
            if f in ("none", "transparent"):
                continue
            fg = st["color"] if f == "currentcolor" else parse_color(f)
            sb = st.get("svg_bg")
            if sb is None and n.tag in ("text", "tspan"):
                out.append((n, None, "svg shapes behind text"))
                continue
            bgs = [sb] if isinstance(sb, tuple) else st["eff_bg"]
        else:
            fg, bgs = st["color"], st["eff_bg"]
        if fg is None:
            out.append((n, None, "colour not resolvable"))
            continue
        if fg[3] == 0:
            continue
        if bgs is None:
            out.append((n, None, st["bg_note"] or "background not resolvable"))
            continue
        ratios = [contrast(over(fg, b), b) for b in bgs]
        r = min(ratios)
        b = bgs[ratios.index(r)]
        large = st["px"] >= 24 or (st["px"] >= 18.66 and st["weight"] >= 700)
        out.append((n, over(fg, b), b, r, large, in_svg))
    return out


def boundary_pairs(p, theme):
    """Buttons and form controls: (node, kind, colour, against, ratio)."""
    styles = p.styles(theme)
    out = []
    for n in p.ctas():
        st = styles.get(id(n))
        if not st or st["hidden"] or st["off"] or st["own_bg"][0] != "colors" or not st["parent_bg"] or not st["eff_bg"]:
            continue
        fill, back = st["eff_bg"][0], st["parent_bg"][0]
        edge = border_edge(st["get"])
        if edge:
            ec = st["color"] if edge == "currentcolor" else parse_color(edge)
            if ec and contrast(over(ec, back), back) >= 3:
                continue
        out.append((n, "button", fill, back, contrast(fill, back)))
    for n in p.dom.iter():
        if n.tag not in ("input", "select", "textarea", "label"):
            continue
        if n.tag == "input" and n.attrs.get("type", "text") in ("hidden", "submit", "button", "reset", "image"):
            continue
        st = styles.get(id(n))
        if not st or st["hidden"] or st["off"] or not st["parent_bg"]:
            continue
        get = st["get"]
        if n.tag == "label":
            if not (get("border") or get("border-color")) or not label_is_choice(p, n):
                continue
        elif n.tag == "input" and n.attrs.get("type") in ("radio", "checkbox") and "none" not in (get("appearance") or ""):
            continue
        back = st["parent_bg"][0]
        edge = border_edge(get, side_only_ok=n.tag in ("input", "textarea"))
        has_fill = st["own_bg"][0] == "colors" and st["eff_bg"]
        if not edge and not has_fill:
            continue
        best, col = 0.0, None
        if edge:
            ec = st["color"] if edge == "currentcolor" else parse_color(edge)
            if ec:
                best, col = contrast(over(ec, back), back), over(ec, back)
        if has_fill:
            r = contrast(st["eff_bg"][0], back)
            if r > best:
                best, col = r, st["eff_bg"][0]
        if col is not None:
            out.append((n, "control", col, back, best))
    return out


def label_is_choice(p, n):
    """A label that renders a radio/checkbox choice (wraps one, is for= one, or follows one)."""
    choice = ("radio", "checkbox")
    if any(c.tag == "input" and c.attrs.get("type") in choice for c in n.iter()):
        return True
    f = n.attrs.get("for")
    if f and any(c.tag == "input" and c.attrs.get("id") == f and c.attrs.get("type") in choice for c in p.dom.iter()):
        return True
    sibs = n.parent.elems if n.parent else []
    i = sibs.index(n)
    return i > 0 and sibs[i - 1].tag == "input" and sibs[i - 1].attrs.get("type") in choice


def placeholder_pairs(p, theme):
    styler = Styler(p, theme)
    styles = p.styles(theme)
    out = []
    for n in p.dom.iter():
        if n.tag in ("input", "textarea") and n.attrs.get("placeholder"):
            st = styles.get(id(n))
            if not st or st["hidden"] or not st["eff_bg"]:
                continue
            d = styler.declared(n, pelem="placeholder")
            v = resolve_vars(d.get("color"), st["vars"]) if d.get("color") else None
            c = parse_color(v) if v else None
            if c:
                b = st["eff_bg"][0]
                out.append((n, over(c, b), b, contrast(over(c, b), b)))
    return out


def check_contrast(p, add):
    for theme in p.themes:
        pairs = text_pairs(p, theme)
        total = len(pairs)
        unres = [x for x in pairs if x[1] is None]
        fails = {}
        for x in pairs:
            if x[1] is None:
                continue
            n, fg, bg, r, large, svg = x
            need = 3.0 if large else 4.5
            if r < need:
                key = (to_hex(fg), to_hex(bg), svg)
                fails.setdefault(key, []).append((n, r, need))
        for (fg, bg, svg), items in sorted(fails.items(), key=lambda kv: kv[1][0][1])[:8]:
            n, r, need = items[0]
            more = " (+%d more)" % (len(items) - 1) if len(items) > 1 else ""
            add("WARN" if svg else "FAIL", "a11y", "[%s] %stext %.2f:1 < %.1f (%s on %s) at `%s` “%s”%s"
                % (theme, "svg " if svg else "", math.floor(r * 100) / 100, need, fg, bg, n.describe(), n.direct_text()[:24], more), "a11y:svg-contrast" if svg else "a11y:contrast")
        if len(fails) > 8:
            add("FAIL", "a11y", "[%s] … and %d more low-contrast pairs (run --contrast)" % (theme, len(fails) - 8))
        if total and len(unres) / total > 0.3:
            add("WARN", "a11y", "[%s] contrast unresolved for %d/%d text elements (%s) - check them by hand"
                % (theme, len(unres), total, ", ".join(sorted(set(x[2] for x in unres)))), "a11y:contrast-unresolved")
        seen = set()
        for n, kind, col, back, r in boundary_pairs(p, theme):
            key = (kind, to_hex(col), to_hex(back))
            if r >= 3 or key in seen:
                continue
            seen.add(key)
            lvl = "FAIL" if r < 1.5 and kind == "button" else "WARN"
            what = "button fill with no full border" if kind == "button" else "form-control edge"
            add(lvl, "a11y", "[%s] %s %.2f:1 < 3 (%s on %s) at `%s`" % (theme, what, r, to_hex(col), to_hex(back), n.describe()), "a11y:control-boundary")
        for n, c, b, r in placeholder_pairs(p, theme):
            if r < 4.5 and ("ph", to_hex(c)) not in seen:
                seen.add(("ph", to_hex(c)))
                add("WARN", "a11y", "[%s] placeholder text %.2f:1 (%s on %s) at `%s`" % (theme, r, to_hex(c), to_hex(b), n.describe()), "a11y:placeholder")


# ---- template fingerprints ---------------------------------------------------

FEATURES = ["families", "width", "h1_weight", "ground", "accent", "themes", "hero", "last_section", "footer"]

# Modal values of the three measured runs (computed with --corpus on research/
# and pages-v3). A page that matches >= 5 of 9 is on that template.
TEMPLATES = {
    "v1 'indigo SaaS'": {
        "families": {"system"}, "width": {"normal"}, "h1_weight": {"bold", "heavy"},
        "ground": {"light neutral", "light cool-grey", "dark cool-grey"}, "accent": {"indigo-violet", "blue"},
        "themes": {"2"}, "hero": {"h1-first"}, "last_section": {"content"}, "footer": {"one-line"}},
    "v2 'stationery editorial'": {
        "families": {"newsreader", "ibm plex mono", "ibm plex sans", "jetbrains mono", "ibm plex sans condensed"},
        "width": {"normal"}, "h1_weight": {"regular"}, "ground": {"light green-grey"},
        "accent": {"red", "orange-amber-yellow"}, "themes": {"2"}, "hero": {"h1-first"},
        "last_section": {"content"}, "footer": {"multi-column"}},
    "v3 'industrial caption'": {
        "families": {"barlow semi condensed", "archivo", "bitter", "zilla slab"},
        "width": {"condensed"}, "h1_weight": {"bold"},
        "ground": {"light cool-grey", "light warm-grey", "dark warm-grey", "dark cool-grey"},
        "accent": {"orange-amber-yellow"}, "themes": {"1"}, "hero": {"artifact-first"},
        "last_section": {"widget"}, "footer": {"one-line"}},
}


def accent_by_use(p):
    """The chromatic colour the stylesheet uses most (tokens count per use)."""
    toks = {}
    for name, val in re.findall(r"(--[\w-]+)\s*:\s*([^;}]+)", p.css):
        c = parse_color(val.strip())
        if c and oklch(c)[1] >= 0.06:
            toks[name] = c
    score = {}
    for name, c in toks.items():
        score[to_hex(c)] = score.get(to_hex(c), 0) + len(re.findall(r"var\(\s*%s\s*[,)]" % re.escape(name), p.css))
    body = re.sub(r"--[\w-]+\s*:\s*[^;}]+", "", p.css)
    for t in COLOR_TOKEN.finditer(body):
        c = parse_color(t.group(0))
        if c and oklch(c)[1] >= 0.06:
            score[to_hex(c)] = score.get(to_hex(c), 0) + 1
    if not score:
        return None
    return parse_color(max(score.items(), key=lambda kv: (kv[1], oklch(parse_color(kv[0]))[1]))[0])


def fingerprint(p):
    fams = [f.lower() for f in p.families()] or ["system"]
    width = "normal"
    if any(re.search(r"condensed|narrow|compressed|gothic", f) for f in fams):
        width = "condensed"
    elif any(re.search(r"expanded|extended|wide", f) for f in fams):
        width = "wide"
    for v in re.findall(r"font-stretch\s*:\s*([^;}]+)", p.css):
        v = v.strip()
        m = re.match(r"([\d.]+)%", v)
        if (m and float(m.group(1)) < 90) or re.match(r"(extra-|ultra-|semi-)?condensed", v):
            width = "condensed"
    for v in re.findall(r"['\"]wdth['\"]\s*([\d.]+)", p.css):
        if float(v) < 90:
            width = "condensed"
    h1 = p.dom.find("h1")
    w = p.st(h1)["weight"] if h1 is not None and p.st(h1) else 700
    wb = "light" if w <= 300 else "regular" if w <= 500 else "bold" if w <= 700 else "heavy"
    g = page_ground(p, "light") or (1, 1, 1, 1)
    fills = [c for n, c in cta_fills(p) if oklch(c)[1] >= 0.06]
    if fills:
        acc = hue_bucket(fills[0], 0.06)
    else:
        acc = hue_bucket(accent_by_use(p), 0.06) if accent_by_use(p) else "neutral"
    main = p.dom.find("main") or p.dom.find("body")
    blocks = [e for e in (main.elems if main is not None else [])
              if e.tag not in ("footer", "script", "style", "header", "nav", "noscript", "template")]
    last = "none"
    if blocks:
        sec = blocks[-1]
        forms = sec.find_all("form")
        if forms and any(leaves_page(f) for f in forms):
            last = "form"
        elif forms or sec.find("input", "select", "textarea", "output") or \
                (sec.find("button") and not sec.find("a")):
            last = "widget"
        elif re.search(r'href="(mailto|tel):', " ".join(str(n.attrs) for n in sec.iter())) or sec.find("address"):
            last = "contact"
        else:
            last = "content"
    foot = p.dom.find_all("footer")
    if not foot:
        fs = "none"
    else:
        f = foot[-1]
        lists = len(f.find_all("ul", "ol", "nav", "dl"))
        heads = len(f.find_all("h2", "h3", "h4", "h5"))
        links = len(f.find_all("a"))
        st = p.st(f) or {}
        if lists >= 2 or heads >= 2 or (st.get("display") == "grid" and len(f.elems) >= 3):
            fs = "multi-column"
        elif lists == 0 and links <= 3 and len(f.text()) <= 160:
            fs = "one-line"
        else:
            fs = "short"
    return {"families": fams, "width": width, "h1_weight": wb, "ground": ground_bucket(g), "accent": acc,
            "themes": str(len(p.themes)), "hero": hero_order(p), "last_section": last, "footer": fs}


SIGNATURE = {"families", "width", "ground", "accent"}


def template_matches(fp):
    """[(template, matched features)] for templates the page is on: >= 5 of 9
    features, at least 2 of them signature features (generic values such as
    'h1-first' or 'one theme' alone do not make a template)."""
    out = []
    for name, t in TEMPLATES.items():
        hit = [f for f in FEATURES if (set(fp[f]) & t[f] if f == "families" else fp[f] in t[f])]
        if len(hit) >= 5 and len(SIGNATURE & set(hit)) >= 2:
            out.append((name, hit))
    return out


H1_FIRST_COMPS = {"product-UI stage", "type poster", "single long-read column", "sticky index sidebar",
                  "fixed half + scrolling half", "centred stack with an oversized artifact", "demo-in-hero",
                  "one big number", "horizontal strata"}


def seed_assigned_features(p, fp):
    """Fingerprint features whose value the seed stamp assigned (so a match
    on them is the seed's doing, not the model's default)."""
    s = p.seed
    if not s:
        return set()
    out = set()
    short, allowed = seed_fonts(p)
    if any(f in allowed for f in fp["families"]):
        out.add("families")
    cls = s["type"]["class"]
    w = "condensed" if "condensed" in cls else "wide" if "wide" in cls else "normal"
    if fp["width"] == w:
        out.add("width")
    bucket = s["color"].get("hue_bucket")
    if fp["accent"] == bucket or (bucket == "neutral" and fp["accent"] == "neutral"):
        out.add("accent")
    strat = s["color"]["strategy"]
    if bucket and bucket in fp["ground"] or fp["ground"].endswith("neutral") and strat.startswith(
            ("Swiss", "near-black", "neon", "image-sampled", "high-chroma duotone")):
        out.add("ground")
    theme = s["color"]["theme"]
    if (fp["themes"] == "2") == theme.startswith("two themes"):
        out.add("themes")
    comp = s["composition"]["name"]
    if (fp["hero"] == "h1-first") == (comp in H1_FIRST_COMPS):
        out.add("hero")
    return out


def check_template(p, add):
    fp = fingerprint(p)
    assigned = seed_assigned_features(p, fp)
    for name, hit in template_matches(fp):
        own = [f for f in hit if f not in assigned]
        if assigned and (len(own) < 5 or len(SIGNATURE & set(own)) < 2):
            p.suppressed.append(("template:" + name.split()[0], "%s match on seed-assigned %s"
                                 % (name, ", ".join(f for f in hit if f in assigned))))
            continue
        add("WARN", "template", "matches the %s template on %d/9 features (%s) - change the axes that match, "
                                "not their values" % (name, len(hit), ", ".join(hit)), "template:" + name.split()[0])


# =============================================================================
# 9. Driver: one page
# =============================================================================

_LAST_PAGE = [None]


def check(path):
    p = Page(path)
    _LAST_PAGE[0] = p
    hits = []

    def add(level, cat, msg, key=None):
        hits.append([level, cat, msg, (key or cat).lower()])

    check_layout(p, add)
    if p.is_html:
        check_colour(p, add)
    else:
        check_colour_css_only(p, add)
    check_type(p, add)
    check_components(p, add)
    if p.is_html:
        check_a11y_meta(p, add)
    check_copy(p, add)
    if p.is_html:
        check_second_order(p, add)
        check_content(p, add)
        check_structure(p, add)
        check_contrast(p, add)
        check_template(p, add)
        check_seed_stamp(p, add)
    apply_slop_ok(p, hits)
    return hits


def check_seed_stamp(p, add):
    if p.stamp is None:
        add("WARN", "seed", "no seed stamp - paste the last line of brief_seed.py's output "
                            "(<!-- seed: \"<brief>\" salt=N -->) so seed-assigned values are not read as defaults",
            "seed:none")
    elif p.seed is None:
        add("WARN", "seed", "seed stamp found but not usable (%s) - seed-assigned values are checked as defaults"
            % p.seed_error, "seed:unreadable")
    else:
        col = p.seed["color"]
        fills = [c for n, c in cta_fills(p) if oklch(c)[1] >= 0.06]
        acc = fills[0] if fills else accent_by_use(p)
        if acc is None or has_override(p, "colour", "color", "hue", "accent", "palette"):
            return
        if col.get("hue_range") and not seed_hue(p, acc):
            add("WARN", "seed", "seed not followed: the accent %s (OKLCH hue %d) is outside the assigned %s - "
                                "move it into the range, or write <!-- seed override: colour <visitor reason> -->"
                % (to_hex(acc), round(oklch(acc)[2]), col["hue"]), "seed:hue")
        elif not col.get("hue_range") and fills:
            add("WARN", "seed", "seed not followed: the CTA fill %s is chromatic but the seed assigned "
                                "'achromatic + photo' (black/white CTA)" % to_hex(acc), "seed:hue")


def apply_slop_ok(p, hits):
    """<!-- slop-ok: <key> <reason> --> keeps a WARN as OK* when the reason has
    >= 4 words. A FAIL is never downgraded."""
    oks = slop_oks(p)
    used = set()
    for h in hits:
        level, cat, msg, key = h
        if key not in oks:
            continue
        used.add(key)
        reason = oks[key]
        if level == "FAIL":
            h[2] = msg + "  (slop-ok ignored: a FAIL cannot be kept)"
        elif len(re.findall(r"[\w'’-]+", reason)) < 4:
            h[2] = msg + "  (slop-ok ignored: give a reason of >= 4 words)"
        else:
            h[0] = "OK*"
            h[2] = msg + "  -- kept: " + reason
    for key in sorted(set(oks) - used):
        hits.append(["NOTE", "slop-ok", "slop-ok '%s' matches no rule on this page (typo, or already fixed?)" % key,
                     "slop-ok:unused"])


def check_colour_css_only(p, add):
    exact = sorted(h for h in declared_colors(p) if h in TAILWIND_HEXES)
    if exact:
        add("FAIL", "color", "stock Tailwind hexes: " + ", ".join(exact[:8]))
    if re.search(r"background-clip\s*:\s*text", p.css):
        add("FAIL", "effects", "gradient-clipped text")


# =============================================================================
# 10. Modes: --contrast, --corpus, --render
# =============================================================================

def walk(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = sorted(d for d in dirs if d not in ("node_modules", ".git", "dist", "build"))
                for f in sorted(files):
                    if f.endswith(EXTS):
                        yield os.path.join(root, f)
        elif p.endswith(EXTS):
            yield p


def run_contrast(paths):
    for f in walk(paths):
        if not f.endswith((".html", ".htm")):
            continue
        p = Page(f)
        print(f"\n{f}")
        for theme in p.themes:
            pairs = text_pairs(p, theme)
            unres = [x for x in pairs if x[1] is None]
            print(f"  [{theme}] checked {len(pairs) - len(unres)}/{len(pairs)} text elements, {len(unres)} unresolved"
                  f" ({p.unsupported} selectors skipped as unsupported)")
            seen = {}
            for x in pairs:
                if x[1] is None:
                    continue
                n, fg, bg, r, large, svg = x
                key = (to_hex(fg), to_hex(bg), large, svg)
                seen.setdefault(key, [r, []])[1].append(n)
            for (fg, bg, large, svg), (r, ns) in sorted(seen.items(), key=lambda kv: kv[1][0]):
                need = 3.0 if large else 4.5
                mark = "ok  " if r >= need else ("warn" if svg else "FAIL")
                print(f"    {mark} text{'(svg)' if svg else '':5} {r:5.2f}:1 need {need}  {fg} on {bg}  "
                      f"x{len(ns)} e.g. `{ns[0].describe()}`")
            for n, kind, col, back, r in boundary_pairs(p, theme):
                print(f"    {'ok  ' if r >= 3 else 'FAIL'} {kind:10} {r:5.2f}:1 need 3.0  {to_hex(col)} on {to_hex(back)}  `{n.describe()}`")
            for n, c, b, r in placeholder_pairs(p, theme):
                print(f"    {'ok  ' if r >= 4.5 else 'warn'} placeholder {r:5.2f}:1  {to_hex(c)} on {to_hex(b)}  `{n.describe()}`")
            reasons = {}
            for x in unres:
                reasons.setdefault(x[2], []).append(x[0].describe())
            for why, ds in reasons.items():
                print(f"    ??   unresolved ({why}): {', '.join(sorted(set(ds))[:6])}")
    return 0


NEUTRAL_SHARED = {("width", "normal"), ("hero", "h1-first"), ("themes", "1")}


def run_corpus(paths):
    pages = [Page(f) for f in walk(paths) if f.endswith((".html", ".htm"))]
    if not pages:
        print("no pages found")
        return 2
    fps = [(p.name, fingerprint(p)) for p in pages]
    print("Fingerprints (%d pages)" % len(fps))
    for name, fp in fps:
        print("  %-8s " % name + " | ".join(
            "+".join(fp[f]) if f == "families" else fp[f] for f in FEATURES))
    print("\nShared values (> 30%% of pages; features: %s)" % ", ".join(FEATURES))
    limit = 0.3 * len(fps)
    shared = []
    for f in FEATURES:
        counts = {}
        for name, fp in fps:
            for v in (fp[f] if f == "families" else [fp[f]]):
                counts.setdefault(v, []).append(name)
        for v, names in sorted(counts.items(), key=lambda kv: -len(kv[1])):
            if len(names) > limit:
                shared.append((f, v, names))
    # neutral conventions are only a smell when they ride along with >= 2
    # other shared values on the same pages
    for f, v, names in shared:
        lvl = "WARN"
        note = ""
        if (f, v) in NEUTRAL_SHARED:
            # the same pages must also share the same two other (non-neutral) values
            others = [(g, w, set(ns)) for g, w, ns in shared if (g, w) not in NEUTRAL_SHARED and g != f]
            best = (set(), None)
            for i in range(len(others)):
                for j in range(i + 1, len(others)):
                    if others[i][0] == others[j][0]:
                        continue
                    common = set(names) & others[i][2] & others[j][2]
                    if len(common) > len(best[0]):
                        best = (common, (others[i][:2], others[j][:2]))
            if len(best[0]) <= limit:
                lvl, note = "ok  ", "  neutral convention (no cluster with 2 other shared values)"
            else:
                (g1, w1), (g2, w2) = best[1]
                note = "  clusters with %s=%s + %s=%s on %s" % (g1, w1, g2, w2, ", ".join(sorted(best[0])))
        print("  %s %-13s %-28s %d/%d  (%s)%s" % (lvl, f, v, len(names), len(fps), ", ".join(names), note))
    if not shared:
        print("  none")
    print("\nKnown templates (WARN at >= 5/9 features)")
    for name, fp in fps:
        for tname, hit in template_matches(fp):
            if hit:
                print("  WARN %-8s matches %s on %d/9: %s" % (name, tname, len(hit), ", ".join(hit)))
    return 0


PW_NODE_DIR = "/tmp/claude-0/-home-user/d5522f34-2674-57a0-9aec-a00bea1b0150/scratchpad/tools/node_modules"
PW_CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

# Runs inside the page; returns the first-viewport measurements.
MEASURE_JS = r"""
([w, h]) => {
  const vis = el => { const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) return false;
    const d = el.closest('details:not([open])');
    if (d && !el.closest('summary')) return false;
    const r = el.getBoundingClientRect();
    if (r.width <= 1 || r.height <= 1) return false;
    for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) {
      const s = getComputedStyle(a);
      if (+s.opacity === 0) return false;
      if (s.overflowX !== 'visible' || s.overflowY !== 'visible') {
        const ar = a.getBoundingClientRect();
        if (Math.min(r.right, ar.right) - Math.max(r.left, ar.left) <= 1 ||
            Math.min(r.bottom, ar.bottom) - Math.max(r.top, ar.top) <= 1) return false;
      }
    }
    return true; };
  const box = el => { const r = el.getBoundingClientRect();
    return {top: Math.round(r.top), bottom: Math.round(r.bottom), left: Math.round(r.left), right: Math.round(r.right)}; };
  const label = el => (el.tagName.toLowerCase() + (el.id ? '#' + el.id : (el.classList.length ? '.' + el.classList[0] : '')))
    + ' "' + (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 28) + '"';
  const out = {overflow: document.documentElement.scrollWidth, overlaps: []};
  const h1 = document.querySelector('h1');
  out.h1 = h1 && vis(h1) ? box(h1) : null;
  const main = document.querySelector('main') || document.body;
  const cands = [...main.querySelectorAll('a[href], button, input[type=submit]')].filter(vis);
  const re = /(^|[\s_-])(cta|btn|button|primary|action|buy|order|signup|subscribe|start|download|install|book|join|shop)([\s_-]|$)/i;
  const cls = e => (typeof e.className === 'string' ? e.className : '') + ' ' + (e.id || '') + ' ' + (e.getAttribute('role') || '');
  const notNav = e => !e.closest('nav') && !/skip|mark|logo/.test(cls(e));
  const hero = h1 && h1.closest('section, header, article, [class*=hero]');
  let cta = null;
  if (hero) {
    const hc = [...hero.querySelectorAll('a[href], button, input[type=submit]')].filter(e => vis(e) && notNav(e));
    const after = hc.filter(e => h1.compareDocumentPosition(e) & Node.DOCUMENT_POSITION_FOLLOWING);
    cta = after.find(e => re.test(cls(e))) || hc.find(e => re.test(cls(e))) || after[0] || null;
  }
  if (!cta) cta = cands.find(e => re.test(cls(e)) && notNav(e));
  if (!cta) cta = [...main.querySelectorAll('form [type=submit], form button:not([type=button])')].find(vis);
  if (!cta) cta = cands.find(e => e.tagName === 'BUTTON');
  if (!cta) cta = cands.find(e => e.tagName === 'A' && !e.closest('nav'));
  out.cta = cta ? Object.assign(box(cta), {label: label(cta)}) : null;
  const sel = 'h1,h2,h3,h4,h5,h6,p,label,figcaption,svg text,a,button';
  const els = [...document.querySelectorAll(sel)].filter(e => vis(e) && (e.textContent || '').trim()
    && (!/^(A|BUTTON)$/.test(e.tagName) || getComputedStyle(e).display !== 'inline'));
  const rects = els.map(e => e.getBoundingClientRect());
  for (let i = 0; i < els.length; i++) for (let j = i + 1; j < els.length; j++) {
    const a = els[i], b = els[j];
    if (a.contains(b) || b.contains(a)) continue;
    const sa = a instanceof SVGElement, sb = b instanceof SVGElement;
    if (sa && sb) continue;
    const r1 = rects[i], r2 = rects[j];
    const iw = Math.min(r1.right, r2.right) - Math.max(r1.left, r2.left);
    const ih = Math.min(r1.bottom, r2.bottom) - Math.max(r1.top, r2.top);
    if (iw <= 0 || ih <= 0) continue;
    const small = Math.min(r1.width * r1.height, r2.width * r2.height);
    if (small > 0 && iw * ih / small > 0.3) out.overlaps.push(label(a) + ' x ' + label(b));
    if (out.overlaps.length >= 6) break;
  }
  return out;
}
"""

NODE_RUNNER = r"""
const { chromium } = require('playwright');
const MEASURE = %s;
(async () => {
  const [files, exe] = [JSON.parse(process.argv[2]), process.argv[3]];
  const b = await chromium.launch(exe ? {executablePath: exe} : {});
  const res = [];
  for (const f of files) {
    const r = {file: f};
    for (const [w, h] of [[360, 740], [1280, 900]]) {
      const p = await b.newPage({viewport: {width: w, height: h}});
      await p.goto('file://' + f, {waitUntil: 'load', timeout: 15000}).catch(() => {});
      await p.waitForTimeout(500);
      try { r[w] = await p.evaluate(MEASURE, [w, h]); } catch (e) { r[w] = {error: String(e)}; }
      await p.close();
    }
    res.push(r);
  }
  await b.close();
  console.log(JSON.stringify(res));
})();
"""


def node_module_dirs():
    out = []
    if os.environ.get("SLOP_PW_NODE_MODULES"):
        out.append(os.environ["SLOP_PW_NODE_MODULES"])
    out += [os.path.join(os.getcwd(), "node_modules"), os.path.join(os.path.dirname(HERE), "node_modules"),
            os.path.join(HERE, "node_modules")]
    npm = shutil.which("npm")
    if npm:
        try:
            g = subprocess.run([npm, "root", "-g"], capture_output=True, text=True, timeout=20).stdout.strip()
            if g:
                out.append(g)
        except Exception:
            pass
    out.append(PW_NODE_DIR)
    seen = []
    for d in out:
        if d not in seen:
            seen.append(d)
    return seen


def find_node_playwright():
    for d in node_module_dirs():
        if os.path.isdir(os.path.join(d, "playwright")):
            return d
    return None


def chrome_path():
    p = os.environ.get("SLOP_PW_CHROME") or PW_CHROME
    return p if p and os.path.exists(p) else ""


def render_measure(files):
    """Return a list of measurement dicts, or (None, reason) if unavailable."""
    files = [os.path.abspath(f) for f in files]
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
        res = []
        with sync_playwright() as pw:
            kw = {"executable_path": chrome_path()} if chrome_path() else {}
            b = pw.chromium.launch(**kw)
            for f in files:
                r = {"file": f}
                for w, h in ((360, 740), (1280, 900)):
                    pg = b.new_page(viewport={"width": w, "height": h})
                    try:
                        pg.goto("file://" + f, wait_until="load", timeout=15000)
                    except Exception:
                        pass
                    pg.wait_for_timeout(500)
                    r[w] = pg.evaluate(MEASURE_JS, [w, h])
                    pg.close()
                res.append(r)
            b.close()
        return res, None
    except ImportError:
        pass
    except Exception as e:      # python playwright without a browser: try node
        sys.stderr.write("python playwright failed (%s); trying node\n" % str(e).splitlines()[0][:120])
    node = shutil.which("node")
    nm = find_node_playwright()
    if not node or not nm:
        return None, ("python playwright not installed and no node playwright found (looked in: %s). "
                      "Install hint: npm i playwright (Chromium needed: npx playwright install chromium), "
                      "or set SLOP_PW_NODE_MODULES=/path/to/node_modules" % ", ".join(node_module_dirs()))
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as t:
        t.write(NODE_RUNNER % MEASURE_JS.strip())
        script = t.name
    try:
        env = dict(os.environ, NODE_PATH=nm)
        out = subprocess.run([node, script, json.dumps(files), chrome_path()],
                             capture_output=True, text=True, env=env, timeout=60 + 40 * len(files))
        if out.returncode != 0:
            return None, "node runner failed: " + out.stderr.strip()[-300:]
        return json.loads(out.stdout.strip().splitlines()[-1]), None
    finally:
        os.unlink(script)


def run_render(paths):
    files = [f for f in walk(paths) if f.endswith((".html", ".htm"))]
    res, why = render_measure(files)
    if res is None:
        print("--render skipped: " + why)
        return 0
    bad = False
    for r in res:
        m, d = r.get(360, r.get("360")), r.get(1280, r.get("1280"))
        hits = []
        if not m or "error" in m:
            hits.append(("WARN", "could not measure: %s" % (m or {}).get("error", "no result")))
        else:
            h1 = m.get("h1")
            if not h1:
                hits.append(("FAIL", "no visible h1"))
            elif h1["top"] + 24 > 740:
                hits.append(("FAIL", "h1 below the first 360x740 viewport (top at %dpx)" % h1["top"]))
            elif h1["top"] > 555:
                hits.append(("WARN", "h1 only in the bottom quarter of the first viewport (top at %dpx)" % h1["top"]))
            cta = m.get("cta")
            if not cta:
                hits.append(("FAIL", "no primary CTA found in main"))
            elif cta["bottom"] > 740 or cta["top"] < 0:
                hits.append(("FAIL", "primary CTA not in the first 360x740 viewport (%s at %dpx)" % (cta["label"], cta["top"])))
            if m["overflow"] > 361:
                hits.append(("FAIL", "horizontal overflow at 360px (scrollWidth %dpx)" % m["overflow"]))
            for o in m["overlaps"]:
                hits.append(("WARN", "text boxes overlap at 360px: " + o))
        for o in (d or {}).get("overlaps", []):
            hits.append(("WARN", "text boxes overlap at 1280px: " + o))
        fails = sum(1 for h in hits if h[0] == "FAIL")
        bad |= bool(fails)
        print("\n%s  —  render: %d FAIL, %d WARN" % (r["file"], fails, len(hits) - fails))
        for lvl, msg in hits:
            print("  %-4s [render] %s" % (lvl, msg))
    return 1 if bad else 0


def main(argv):
    flags = {a for a in argv if a.startswith("--")}
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        print(__doc__)
        return 2
    if "--contrast" in flags:
        return run_contrast(paths)
    if "--corpus" in flags:
        return run_corpus(paths)
    if "--render" in flags:
        return run_render(paths)
    as_json, strict = "--json" in flags, "--strict" in flags
    report, bad = {}, False
    totals = [0, 0, 0, 0]
    for f in walk(paths):
        hits = check(f)
        p_seed = _LAST_PAGE[0]
        report[f] = [{"level": l, "category": c, "key": k, "message": m} for l, c, m, k in hits]
        fails = sum(1 for h in hits if h[0] == "FAIL")
        warns = sum(1 for h in hits if h[0] == "WARN")
        kept = sum(1 for h in hits if h[0] == "OK*")
        totals = [totals[0] + 1, totals[1] + fails, totals[2] + warns, totals[3] + kept]
        if fails or (strict and warns):
            bad = True
        if not as_json:
            print(f"\n{f}  —  {fails} FAIL, {warns} WARN, {kept} kept with reason (OK*)")
            if p_seed is not None and p_seed.seed:
                s = p_seed.seed
                print("  seed: \"%s\" salt=%d -> %s / %s / %s / %s%s" % (
                    s["brief"], s["salt"], s["type"]["shortlist"][0], s["composition"]["name"],
                    s["color"]["strategy"], s["color"]["hue"], ("; %d WARN suppressed as seed-assigned"
                                                                % len(p_seed.suppressed)) if p_seed.suppressed else ""))
            order = {"FAIL": 0, "WARN": 1, "OK*": 2, "NOTE": 3}
            for l, c, m, k in sorted(hits, key=lambda h: (order.get(h[0], 9), h[1])):
                print(f"  {l:4} [{c if l == 'FAIL' else k}] {m}")
    if not as_json and totals[0] > 1:
        print("\nTotal: %d files, %d FAIL, %d WARN, %d kept with reason (OK*)" % tuple(totals))
    if as_json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
