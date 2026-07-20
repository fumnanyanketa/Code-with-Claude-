#!/usr/bin/env python3
"""Build the whole course: render every lesson (with prev/next/home links) + the index.

Generic, config-driven. Point it at a course root that contains:
    course.json                 (branding + module names/blurbs)
    lessons/module-N-slug/NN-slug.md

It writes lessons-html/ next to lessons/, mirroring the folder structure, plus
lessons-html/index.html (the landing page) and a root index.html redirect.

Usage:
    python3 build_course.py [course-root]      # default: current directory

Dependencies (markdown, pygments) are auto-installed on first run if missing.
"""
import importlib
import os
import pathlib
import re
import subprocess
import sys

# --- bootstrap dependencies so the script "just works" ----------------------
for pkg in ("markdown", "pygments"):
    try:
        importlib.import_module(pkg)
    except ImportError:
        print(f"installing {pkg} ...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", pkg], check=True)

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_lesson as bl  # noqa: E402

ROOT = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else pathlib.Path.cwd()
LESSONS = ROOT / "lessons"
OUT_ROOT = ROOT / "lessons-html"
CFG_PATH = ROOT / "course.json"

if not LESSONS.exists():
    sys.exit(f"no lessons/ directory under {ROOT}")

cfg = bl.load_cfg(str(CFG_PATH))

items = []
for md in LESSONS.glob("*/*.md"):
    text = md.read_text()
    m = re.match(r"#\s+Module\s+\d+\s+·\s+Lesson\s+(\d+):\s+(.+)", text)
    if not m:
        print("skip (no 'Module N · Lesson M: Title' H1):", md)
        continue
    num = int(m.group(1))
    title = m.group(2).strip()
    out = (OUT_ROOT / md.relative_to(LESSONS)).with_suffix(".html")
    items.append({"num": num, "title": title, "md": md, "out": out})

items.sort(key=lambda x: x["num"])

for i, it in enumerate(items):
    it["out"].parent.mkdir(parents=True, exist_ok=True)
    prev = nxt = None
    if i > 0:
        p = items[i - 1]
        prev = {"title": p["title"], "href": os.path.relpath(p["out"], it["out"].parent)}
    if i < len(items) - 1:
        n = items[i + 1]
        nxt = {"title": n["title"], "href": os.path.relpath(n["out"], it["out"].parent)}
    home = os.path.relpath(OUT_ROOT / "index.html", it["out"].parent)
    bl.convert(str(it["md"]), str(it["out"]), cfg=cfg, home=home, prev=prev, nxt=nxt)

print(f"rendered {len(items)} lessons")

# Rebuild the landing page.
subprocess.run([sys.executable, str(pathlib.Path(__file__).resolve().parent / "build_index.py"), str(ROOT)], check=True)

# Root redirect so opening the project root lands on the course.
(ROOT / "index.html").write_text(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta http-equiv="refresh" content="0; url=lessons-html/index.html">'
    '<link rel="canonical" href="lessons-html/index.html">'
    f'<title>{cfg.get("title", "Course")}</title></head>'
    '<body style="font-family:system-ui;text-align:center;padding:60px">'
    'Redirecting to the course. If nothing happens, open '
    '<a href="lessons-html/index.html">the course</a>.</body></html>')

print(f"done. open {OUT_ROOT / 'index.html'}")
