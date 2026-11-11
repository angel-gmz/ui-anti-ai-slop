#!/usr/bin/env python3
"""Scan game UI source for generic, generated-looking defaults.

Usage:
    python slop_scan.py <file-or-folder> [more paths...] [--json] [--strict]

Reads .html, .css, .js, .jsx, .ts, .tsx, .vue and .svelte files and reports
tells by severity (P0, P1, P2). Each rule ID is explained in
references/slop-tells.md.

Exit code is 1 when any unwaived P0 finding exists (or any P0/P1 with
--strict), otherwise 0. A finding is waived when the scanned source contains
a comment of the form:   slop-ok: <rule-id> <reason>

The checks are heuristics over source text. A clean scan means no obvious
defaults were found, not that the interface is good. Python 3.8+, no
dependencies.
"""
import colorsys
import json
import os
import re
import sys

EXTENSIONS = {".html", ".htm", ".css", ".scss", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", "vendor", ".next", "coverage"}
MAX_LOCATIONS = 5  # locations printed per rule; the rest are counted

GENERIC_FONTS = {
    "inter", "roboto", "arial", "helvetica", "helvetica neue", "system-ui", "-apple-system",
    "blinkmacsystemfont", "segoe ui", "sans-serif", "ui-sans-serif", "open sans", "lato",
}
REFLEX_FONTS = {
    "press start 2p", "orbitron", "audiowide", "cinzel", "cinzel decorative", "bangers",
    "poppins", "montserrat",
}
STOCK_COPY = [
    "lorem ipsum", "welcome to", "get started", "embark on", "epic adventure", "unleash",
    "level up your", "player 1", "item 1", "epic sword",
]
SAAS_GROUNDS = {"#0f172a", "#1e293b", "#111827", "#1f2937", "#020617", "#0b1120"}

# rule id -> (severity, one-line message)
RULES = {
    "emoji-icons": ("P0", "Emoji used in the UI. Draw icons as inline SVG in one style."),
    "glass-panels": ("P0", "backdrop-filter blur (glass panels). Build surfaces from the direction's material."),
    "purple-gradient": ("P0", "Gradient through purple/violet/indigo. Use flat color or a gradient with a physical cause."),
    "default-font": ("P0", "Generic or missing typeface. Choose a display face and a reading face and load them."),
    "focus-removed": ("P0", "outline removed and no focus style defined. Draw focus as the game's cursor."),
    "reflex-genre-font": ("P1", "Genre-default typeface. Keep it only if the direction chose it on purpose."),
    "gradient-text": ("P1", "Gradient-filled text. Give title lettering construction instead."),
    "one-shape": ("P1", "Only rounded rectangles; no clip-path, border-image or mask. Add a shape vocabulary."),
    "pill-everything": ("P1", "Fully rounded pills used repeatedly. Take shapes from the material."),
    "soft-web-shadow": ("P1", "Large soft drop shadows. Use hard offset shadows from one light direction."),
    "glow-spam": ("P1", "Blurred zero-offset glows used throughout. Reserve glow for one emissive element."),
    "stock-icon-set": ("P1", "General-purpose icon library. Draw a small custom set."),
    "native-controls": ("P1", "Stock browser controls (<progress>, <select>). Draw meters and selectors in the direction."),
    "transition-all": ("P1", "transition: all. Name the properties and time each by meaning."),
    "card-hover-lift": ("P1", "Hover lifts the element (translateY up). Use a cursor state and a physical press."),
    "no-reduced-motion": ("P1", "Animation without prefers-reduced-motion handling."),
    "no-focus-style": ("P1", "Buttons exist but nothing styles :focus or :focus-visible."),
    "div-buttons": ("P1", "Click handlers on non-button elements. Use <button>."),
    "tailwind-web-defaults": ("P1", "Web-app utility combos (rounded-xl + shadow-lg, bg-white/10, backdrop-blur)."),
    "saas-ground": ("P2", "Framework dark slate/navy as the base color. Tint the ground toward the world."),
    "no-tabular-nums": ("P2", "No tabular-nums anywhere. Changing numbers will jitter."),
    "uniform-easing": ("P2", "Only default easings. Use curves or steps that fit the material."),
    "labelled-values": ("P2", "Text-labelled values (\"Health: 100\"). Prefer shape, pips or icon plus numeral."),
    "stock-copy": ("P2", "Boilerplate or placeholder copy."),
    "selectable-stage": ("P2", "No user-select: none. The game surface will select like a document."),
}

EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿️]")
HEX = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
GRADIENT = re.compile(r"(?:linear|radial|conic)-gradient\(([^;{}]*)", re.I)
FONT_DECL = re.compile(r"(?:font-family|--[\w-]*font[\w-]*|fontFamily)\s*:\s*([^;}\n]+)", re.I)
SHADOW_DECL = re.compile(r"(?:box-shadow|text-shadow|boxShadow|textShadow)\s*:\s*([^;}\n]+)", re.I)
RADIUS_DECL = re.compile(r"(?:border-radius|borderRadius)\s*:\s*([^;}\n]+)", re.I)
WAIVER = re.compile(r"slop-ok:\s*([\w-]+)")


def collect_files(paths):
    files = []
    for path in paths:
        if os.path.isfile(path):
            files.append(path)
        elif os.path.isdir(path):
            for root, dirs, names in os.walk(path):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for name in sorted(names):
                    if os.path.splitext(name)[1].lower() in EXTENSIONS:
                        files.append(os.path.join(root, name))
        else:
            sys.exit(f"slop_scan: path not found: {path}")
    return files


def hue_sat(hex_color):
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    hue, light, sat = colorsys.rgb_to_hls(r, g, b)
    return hue * 360, sat, light


def is_purple_gradient(args):
    """True when a gradient runs through purple into blue, pink or more purple."""
    low = args.lower()
    named_purple = re.search(r"\b(purple|violet|indigo|fuchsia|magenta|rebeccapurple)\b", low)
    purples = cool = 0
    for match in HEX.finditer(args):
        hue, sat, light = hue_sat(match.group(0))
        if sat < 0.35 or light < 0.12 or light > 0.92:
            continue  # greys, near-black and near-white carry no hue
        if 250 <= hue <= 320:
            purples += 1
        elif 195 <= hue < 250 or 320 < hue <= 350:
            cool += 1
    return bool(named_purple) or (purples >= 1 and purples + cool >= 2)


def first_family(value):
    value = value.strip().strip("'\"`")
    if value.startswith("var("):
        return None
    first = value.split(",")[0].strip().strip("'\"`").lower()
    return first or None


def px_numbers(part):
    """Numeric lengths in a shadow layer, in order, ignoring anything inside color functions."""
    part = re.sub(r"(rgba?|hsla?|oklch|color-mix)\([^)]*\)", "", part)
    part = HEX.sub("", part)
    return [float(n) for n in re.findall(r"(?<![\w.#-])(-?\d*\.?\d+)(?:px)?(?![\w.%])", part)]


def scan(files):
    found = {}       # rule id -> list of "file:line"
    waived = set()
    seen = {"css": False, "font_decl": False, "focus_style": False, "outline_none": [],
            "button": False, "motion": False, "reduced": False, "tabular": False,
            "custom_ease": False, "user_select": False, "shape": False, "markup": False}
    radius_lines, pill_lines, glow_lines, soft_lines = [], [], [], []

    def hit(rule, path, line_no):
        found.setdefault(rule, []).append(f"{path}:{line_no}")

    for path in files:
        try:
            with open(path, encoding="utf-8", errors="replace") as handle:
                text = handle.read()
        except OSError as error:
            print(f"slop_scan: cannot read {path}: {error}", file=sys.stderr)
            continue

        waived.update(WAIVER.findall(text))
        low = text.lower()
        seen["css"] |= "{" in text and ":" in text
        seen["markup"] |= "<" in text and ">" in text
        seen["focus_style"] |= bool(re.search(r":focus(-visible|-within)?\b", low))
        seen["button"] |= "<button" in low or "onclick" in low
        seen["motion"] |= "@keyframes" in low or bool(re.search(r"\btransition\s*:", low))
        seen["reduced"] |= "prefers-reduced-motion" in low
        seen["tabular"] |= "tabular-nums" in low
        seen["custom_ease"] |= "cubic-bezier(" in low or "steps(" in low or "linear(" in low
        seen["user_select"] |= "user-select" in low or "userselect" in low
        seen["shape"] |= bool(re.search(r"clip-path|clippath|border-image|borderimage|mask(-image)?\s*:", low))

        for number, line in enumerate(text.split("\n"), 1):
            lower = line.lower()

            if EMOJI.search(line):
                hit("emoji-icons", path, number)
            if re.search(r"backdrop-?filter\s*:\s*[^;]*blur|backdrop-blur", line, re.I):
                hit("glass-panels", path, number)
            for gradient in GRADIENT.finditer(line):
                if is_purple_gradient(gradient.group(1)):
                    hit("purple-gradient", path, number)
            if re.search(r"\b(from|via|to)-(purple|violet|indigo|fuchsia)-\d{3}\b", line):
                hit("purple-gradient", path, number)

            for declaration in FONT_DECL.finditer(line):
                seen["font_decl"] = True
                family = first_family(declaration.group(1))
                if family in GENERIC_FONTS:
                    hit("default-font", path, number)
                elif family in REFLEX_FONTS:
                    hit("reflex-genre-font", path, number)
            for font in REFLEX_FONTS:
                if "family=" + font.replace(" ", "+") in lower:
                    hit("reflex-genre-font", path, number)

            if re.search(r"background-clip\s*:\s*text|bg-clip-text", lower):
                hit("gradient-text", path, number)
            if re.search(r"outline\s*:\s*(none|0)\b", lower):
                seen["outline_none"].append(f"{path}:{number}")

            for declaration in RADIUS_DECL.finditer(line):
                value = declaration.group(1).lower()
                if re.search(r"\b(9999?|999)\d*px|\b[5-9]\d\d+px|\b100vmax", value):
                    pill_lines.append(f"{path}:{number}")
                if not re.fullmatch(r"\s*(0|0px|50%|inherit|none)\s*", value):
                    radius_lines.append(f"{path}:{number}")
            if re.search(r"\brounded-full\b", line):
                pill_lines.append(f"{path}:{number}")

            for declaration in SHADOW_DECL.finditer(line):
                for layer in re.split(r",(?![^(]*\))", declaration.group(1)):
                    if "inset" in layer:
                        continue
                    numbers = px_numbers(layer)
                    if len(numbers) < 3:
                        continue
                    x, y, blur = numbers[0], numbers[1], numbers[2]
                    if x == 0 and y == 0 and blur >= 6:
                        glow_lines.append(f"{path}:{number}")
                    elif blur >= 16 and abs(y) >= 4:
                        soft_lines.append(f"{path}:{number}")
            if re.search(r"drop-shadow\(\s*0(px)?\s+0(px)?\s+([6-9]|\d\d+)px", lower):
                glow_lines.append(f"{path}:{number}")

            if re.search(r"lucide|heroicons|font-?awesome|feather-icons|material-icons|material-symbols|bootstrap-icons|react-icons", lower):
                hit("stock-icon-set", path, number)
            if re.search(r"<progress\b|<select\b", lower):
                hit("native-controls", path, number)
            if re.search(r"transition(-property)?\s*:\s*all\b|\btransition-all\b", lower):
                hit("transition-all", path, number)
            if re.search(r"<(div|span|li|img|p|td)\b[^>]*\bonclick\s*=", lower):
                hit("div-buttons", path, number)
            if re.search(r"rounded-(xl|2xl|3xl)[^\"'`]*shadow-(lg|xl|2xl)|shadow-(lg|xl|2xl)[^\"'`]*rounded-(xl|2xl|3xl)|bg-white/(5|10|20)\b", line):
                hit("tailwind-web-defaults", path, number)
            if any(ground in lower for ground in SAAS_GROUNDS) or re.search(r"\bbg-(slate|gray|zinc)-(900|950)\b", lower):
                hit("saas-ground", path, number)
            if re.search(r">[^<>{};=]*\b(hp|health|score|ammo|lives|level|gold|coins|energy|mana)\s*:\s*(<|\d|\$\{|$)", lower):
                hit("labelled-values", path, number)
            if any(phrase in lower for phrase in STOCK_COPY):
                hit("stock-copy", path, number)

        # hover lift can span lines, so match on the whole file
        for block in re.finditer(r":hover[^{}]*\{([^}]*)\}", text):
            if re.search(r"translatey\(\s*-", block.group(1).lower()):
                hit("card-hover-lift", path, text.count("\n", 0, block.start()) + 1)

    # project-level rules
    anchor = files[0] if files else "."
    if seen["markup"] and not seen["font_decl"] and "default-font" not in found:
        found["default-font"] = [f"{anchor}: no font-family declared anywhere"]
    if seen["outline_none"] and not seen["focus_style"]:
        found["focus-removed"] = seen["outline_none"]
    elif seen["button"] and not seen["focus_style"]:
        found["no-focus-style"] = [f"{anchor}: no :focus or :focus-visible rule found"]
    if len(radius_lines) >= 6 and not seen["shape"]:
        found["one-shape"] = radius_lines
    if len(pill_lines) >= 3:
        found["pill-everything"] = pill_lines
    if len(glow_lines) >= 4:
        found["glow-spam"] = glow_lines
    if len(soft_lines) >= 2:
        found["soft-web-shadow"] = soft_lines
    if seen["motion"] and not seen["reduced"]:
        found["no-reduced-motion"] = [f"{anchor}: animations or transitions without a reduced-motion rule"]
    if seen["motion"] and not seen["custom_ease"]:
        found["uniform-easing"] = [f"{anchor}: no cubic-bezier() or steps() anywhere"]
    if seen["css"] and seen["markup"] and not seen["tabular"]:
        found["no-tabular-nums"] = [f"{anchor}: tabular-nums not used"]
    if seen["css"] and seen["markup"] and not seen["user_select"]:
        found["selectable-stage"] = [f"{anchor}: user-select not set"]

    return found, waived


def main(argv):
    flags = {a for a in argv if a.startswith("--")}
    paths = [a for a in argv if not a.startswith("--")]
    if not paths or "--help" in flags:
        print(__doc__)
        return 0 if "--help" in flags else 2

    files = collect_files(paths)
    if not files:
        sys.exit("slop_scan: no .html, .css, .js, .jsx, .ts, .tsx, .vue or .svelte files found")
    found, waived = scan(files)

    findings = []
    for rule, locations in found.items():
        severity, message = RULES[rule]
        findings.append({"rule": rule, "severity": severity, "message": message, "count": len(locations),
                         "locations": locations[:MAX_LOCATIONS], "waived": rule in waived})
    findings.sort(key=lambda f: (f["severity"], f["rule"]))

    active = [f for f in findings if not f["waived"]]
    counts = {level: sum(1 for f in active if f["severity"] == level) for level in ("P0", "P1", "P2")}
    failing = counts["P0"] + (counts["P1"] if "--strict" in flags else 0)

    if "--json" in flags:
        print(json.dumps({"files": len(files), "counts": counts, "findings": findings}, indent=2))
    else:
        print(f"slop_scan: {len(files)} file(s) scanned")
        for finding in findings:
            tag = "waived" if finding["waived"] else finding["severity"]
            print(f"\n[{tag}] {finding['rule']} ({finding['count']})")
            print(f"    {finding['message']}")
            for location in finding["locations"]:
                print(f"    - {location}")
            if finding["count"] > MAX_LOCATIONS:
                print(f"    - and {finding['count'] - MAX_LOCATIONS} more")
        print(f"\nP0: {counts['P0']}   P1: {counts['P1']}   P2: {counts['P2']}   waived: {len(findings) - len(active)}")
        if not findings:
            print("No obvious defaults found. That is not the same as good: do the swap, dashboard, squint and direction tests.")
        elif failing:
            print("Fix the findings above (see references/slop-tells.md for each rule), then scan again.")
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
