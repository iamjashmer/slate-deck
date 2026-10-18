#!/usr/bin/env python3
"""Check a .slate deck folder before opening it in Slate.

Usage: validate_deck.py <Deck.slate>

Errors (exit 1) are things Slate cannot open or will show broken.
Warnings are things worth fixing: off-theme colors, missing notes, network use.
"""
import json
import re
import sys
import uuid
from html.parser import HTMLParser
from pathlib import Path

THEMES = {"april", "april-night", "chalkboard", "notebook", "ocean", "sunrise", "minimal", "classic", "light", "dark"}
TRANSITIONS = {"none", "fade", "push", "zoom"}
CHART_TYPES = {"bar", "line", "pie"}


class SlideScan(HTMLParser):
    """Collects what the checks need from one slide."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.urls = []          # (tag, attr, value)
        self.ids = []
        self.boxes = []         # style strings of [data-box] elements
        self.charts = 0
        self.chart_json = []    # text of JSON scripts inside data-chart figures
        self.text = []
        self._in_chart = 0
        self._json_script = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for name in ("src", "href"):
            if a.get(name):
                self.urls.append((tag, name, a[name]))
        if a.get("id"):
            self.ids.append(a["id"])
        if "data-box" in a:
            self.boxes.append(a.get("style") or "")
        if "data-chart" in a:
            self.charts += 1
            self._in_chart += 1
        if tag == "script" and self._in_chart and (a.get("type") or "") == "application/json":
            self._json_script = True
            self.chart_json.append("")

    def handle_endtag(self, tag):
        if tag == "script":
            self._json_script = False
        if tag == "figure" and self._in_chart:
            self._in_chart -= 1

    def handle_data(self, data):
        if self._json_script:
            self.chart_json[-1] += data
        elif data.strip():
            self.text.append(data.strip())


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    deck = Path(sys.argv[1]).expanduser()
    errors, warnings = [], []
    err = errors.append
    warn = warnings.append

    if not deck.is_dir():
        print(f"error: {deck} is not a folder")
        return 1
    if deck.suffix != ".slate":
        warn(f"the folder name should end in .slate so Slate can open it (rename to {deck.name}.slate)")

    slides_dir = deck / "slides"
    notes_dir = deck / "notes"
    assets_dir = deck / "assets"
    manifest = {}
    manifest_path = deck / "deck.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            err(f"deck.json is not valid JSON: {e}")
            manifest = {}
    else:
        warn("no deck.json: slides will be taken from slides/*.html in name order")

    theme = manifest.get("theme", "april")
    if theme not in THEMES:
        err(f"deck.json theme '{theme}' is not one of: {', '.join(sorted(THEMES - {'light', 'dark'}))}")
    if manifest.get("transition", "none") not in TRANSITIONS:
        err(f"deck.json transition must be one of {sorted(TRANSITIONS)}")

    entries = manifest.get("slides")
    if entries is None:
        files = sorted(p.name for p in slides_dir.glob("*.html")) if slides_dir.is_dir() else []
        entries = [{"file": f} for f in files]
    if not entries:
        err("the deck has no slides: add HTML files to slides/")

    seen_ids = set()
    notes_missing = []
    for n, entry in enumerate(entries, 1):
        where = f"slide {n}"
        if not isinstance(entry, dict) or "file" not in entry:
            err(f"{where}: each deck.json slide needs a \"file\"")
            continue
        name = entry["file"]
        where = f"slide {n} ({name})"
        if "id" in entry:
            try:
                sid = str(uuid.UUID(str(entry["id"])))
                if sid in seen_ids:
                    err(f"{where}: duplicate id {sid}")
                seen_ids.add(sid)
            except ValueError:
                err(f"{where}: id must be a UUID, or leave it out")
        if entry.get("transition", "none") not in TRANSITIONS:
            err(f"{where}: transition must be one of {sorted(TRANSITIONS)}")
        path = slides_dir / name
        if not path.is_file():
            err(f"{where}: slides/{name} does not exist")
            continue
        html = path.read_text(encoding="utf-8")
        if not html.strip():
            err(f"{where}: the file is empty")
            continue

        notes_name = entry.get("notes") or (Path(name).stem + ".md")
        if not (notes_dir / notes_name).is_file():
            notes_missing.append(n)

        full = re.match(r"\s*<(!doctype|html)", html, re.I) is not None
        if full:
            if "_slate/theme.css" not in html:
                warn(f"{where}: full page without _slate/april.css and _slate/theme.css will not follow the theme")
        elif re.search(r"<(html|head|body)\b", html, re.I):
            err(f"{where}: a fragment must not contain <html>, <head> or <body>; start the file with <!doctype html> to make it a full page")

        scan = SlideScan()
        scan.feed(html)
        dupes = {i for i in scan.ids if scan.ids.count(i) > 1}
        if dupes:
            err(f"{where}: duplicate ids {sorted(dupes)}")
        for tag, attr, url in scan.urls:
            if url.startswith(("http://", "https://", "//")):
                if tag in ("script", "link"):
                    warn(f"{where}: loads {url} from the network; the slide breaks when presenting offline")
            elif url.startswith("assets/"):
                if not (assets_dir / url[len("assets/"):].split("?")[0]).is_file():
                    err(f"{where}: {attr}=\"{url}\" but that file is not in assets/")
            elif url.startswith("/") or re.match(r"[a-zA-Z]:\\", url):
                err(f"{where}: absolute path {url}; copy the file into assets/ and use assets/<name>")
        for style in scan.boxes:
            if "left" not in style or "top" not in style:
                warn(f"{where}: a data-box element needs left and top in its style")
        if scan.charts != len(scan.chart_json):
            err(f"{where}: each data-chart figure needs a <script type=\"application/json\"> with its data")
        for text in scan.chart_json:
            try:
                data = json.loads(text)
                labels, values = data.get("labels", []), data.get("values", [])
                if data.get("type", "bar") not in CHART_TYPES:
                    err(f"{where}: chart type must be one of {sorted(CHART_TYPES)}")
                if len(labels) != len(values) or not labels:
                    err(f"{where}: chart labels and values must be non-empty and the same length")
                if not all(isinstance(v, (int, float)) for v in values):
                    err(f"{where}: chart values must be numbers")
            except (json.JSONDecodeError, AttributeError):
                err(f"{where}: chart data is not valid JSON")
        literal_colors = re.findall(r"#[0-9a-fA-F]{6}\b|rgb\(", html)
        if len(literal_colors) > 3:
            warn(f"{where}: {len(literal_colors)} literal colors; use theme tokens like var(--navy) so the slide follows the theme")
        if not full and "stage" not in html:
            warn(f"{where}: no <main class=\"stage\">; content will sit against the top-left edge")

    if notes_missing:
        warn(f"no presenter notes for slide(s) {', '.join(map(str, notes_missing))}")
    if assets_dir.is_dir():
        for asset in assets_dir.iterdir():
            if " " in asset.name:
                warn(f"assets/{asset.name}: rename without spaces")

    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    status = "FAILED" if errors else "OK"
    print(f"{status}: {deck.name}, {len(entries)} slides, theme {theme}, "
          f"{len(entries) - len(notes_missing)} with notes, {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
