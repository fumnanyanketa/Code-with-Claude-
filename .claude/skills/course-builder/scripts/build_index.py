#!/usr/bin/env python3
"""Build the course landing page (lessons-html/index.html) from the lesson files.

Generic, config-driven version. Scans lessons/**/*.md, reads each H1
("# Module N · Lesson M: Title") and the Speaker / Estimated time from the meta
blockquote, groups by module, and writes an index page in the same LMS style as
the lessons. Module names, blurbs, and course branding come from course.json.

Usage (normally called by build_course.py):
    python3 build_index.py [course-root]   # default: current directory
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else pathlib.Path.cwd()
LESSONS = ROOT / "lessons"
CFG_PATH = ROOT / "course.json"

cfg = json.loads(CFG_PATH.read_text()) if CFG_PATH.exists() else {}
COURSE = cfg.get("title", "The Course")
ACCENT = cfg.get("accent_word", "")            # a word in the title to color coral
TAGLINE = cfg.get("tagline", "A hands-on, self-paced course.")
FOOTER_NOTE = cfg.get("footer_note", "A self-paced course.")
START_HERE = cfg.get("start_here", "")          # optional path to an orientation page
MODULES = {int(k): v for k, v in cfg.get("modules", {}).items()}

# Headline = course title with the accent word (if any) colored.
if ACCENT and ACCENT in COURSE:
    head_html = html.escape(COURSE).replace(html.escape(ACCENT), f'<span class="a">{html.escape(ACCENT)}</span>', 1)
else:
    head_html = html.escape(COURSE)

lessons = []
for md in sorted(LESSONS.glob("*/*.md")):
    text = md.read_text()
    m = re.match(r"#\s+Module\s+(\d+)\s+·\s+Lesson\s+(\d+):\s+(.+)", text)
    if not m:
        continue
    mod, num, title = int(m.group(1)), int(m.group(2)), m.group(3).strip()
    sm = re.search(r"\*\*Speaker:?\*\*\s*(.+)", text)
    speaker = sm.group(1).strip() if sm else ""
    tm = re.search(r"\*\*Estimated time:?\*\*\s*(.+)", text)
    time = re.sub(r"\s*\(.*\)", "", tm.group(1)).strip() if tm else ""
    href = str(md.relative_to(LESSONS)).replace(".md", ".html")  # index sits inside lessons-html
    lessons.append((mod, num, title, speaker, time, href))

lessons.sort(key=lambda x: x[1])
by_mod = {}
for L in lessons:
    by_mod.setdefault(L[0], []).append(L)

cards = []
for mod in sorted(by_mod):
    items = ""
    for (_, num, title, speaker, time, href) in by_mod[mod]:
        sub = " · ".join(x for x in [html.escape(speaker), html.escape(time)] if x)
        items += (f'<a class="lesson" href="{html.escape(href)}">'
                  f'<span class="num">{num:02d}</span>'
                  f'<span class="ltext"><span class="lt">{html.escape(title)}</span>'
                  f'<span class="ls">{sub}</span></span>'
                  f'<span class="arr">&#8594;</span></a>')
    mname = MODULES.get(mod, {}).get("name", f"Module {mod}")
    mblurb = MODULES.get(mod, {}).get("blurb", "")
    cards.append(
        f'<section class="modcard"><div class="modhead"><span class="modtag">Module {mod}</span>'
        f'<h2>{html.escape(mname)}</h2>'
        f'<p>{html.escape(mblurb)}</p></div>'
        f'<div class="lessons">{items}</div></section>')

# Headline counts describe the core curriculum (Modules 1+); an optional
# pre-flight (Module 0) is rendered as a card but not counted in the stats.
core_modules = len([m for m in by_mod if m >= 1])
core_lessons = len([L for L in lessons if L[0] >= 1])

start_btn = (f'<div style="margin-top:30px"><a href="{html.escape(START_HERE)}" '
             f'style="display:inline-flex;align-items:center;gap:9px;background:#18c4a0;color:#04231c;'
             f'font-weight:600;border-radius:999px;padding:13px 26px;text-decoration:none;font-family:Inter">'
             f'New here? Start with the orientation &#8594;</a></div>') if START_HERE else ""

PAGE = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(COURSE)} | A self-paced course</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{{--navy:#0a1a2f;--navy-2:#0f243d;--navy-3:#15314f;--teal:#18c4a0;--teal-d:#0fa385;--coral:#f24d63;--ink:#152230;--muted:#5f6c7b;--line:#e9eef2;--soft:#f4fbf9;--shadow:0 10px 30px rgba(13,30,52,.08)}}
*{{box-sizing:border-box}}
body{{margin:0;background:#fff;color:var(--ink);font-family:Inter,system-ui,sans-serif;line-height:1.7;-webkit-font-smoothing:antialiased;overflow-x:hidden}}
a{{text-decoration:none;color:inherit}}
h1,h2{{font-family:Poppins,sans-serif;letter-spacing:-.01em}}
.wrap{{max-width:1100px;margin:0 auto;padding:0 26px}}
.hero{{position:relative;background:radial-gradient(120% 120% at 80% 0%,var(--navy-3),var(--navy) 60%);color:#eaf1f8;overflow:hidden;text-align:center;padding:80px 0 90px}}
.hero::before{{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.12) 1.3px,transparent 1.3px);background-size:22px 22px;opacity:.22;mask:radial-gradient(70% 70% at 50% 20%,#000,transparent)}}
.blob{{position:absolute;border-radius:50%;filter:blur(10px);opacity:.5}}
.blob.t{{width:240px;height:240px;background:rgba(24,196,160,.30);top:-70px;left:6%}}
.blob.c{{width:170px;height:170px;background:rgba(242,77,99,.26);bottom:-50px;right:10%}}
.hero .in{{position:relative;z-index:2}}
.eyebrow{{display:inline-flex;gap:8px;color:var(--teal);font-weight:600;letter-spacing:.04em;text-transform:uppercase;font-size:14px;margin-bottom:16px}}
.hero h1{{font-size:52px;line-height:1.08;margin:0 0 16px;color:#fff;font-weight:800}}
.hero h1 .a{{color:var(--coral)}}
.hero p{{color:#b9c6d6;font-size:18px;max-width:40em;margin:0 auto 26px}}
.stats{{display:flex;gap:34px;justify-content:center;flex-wrap:wrap;margin-top:30px}}
.stat .n{{font-family:Poppins;font-weight:800;font-size:30px;color:#fff}}
.stat .l{{color:#9fb0c2;font-size:13.5px}}
main{{padding:64px 0 100px}}
.intro{{text-align:center;max-width:40em;margin:0 auto 50px;color:var(--muted)}}
.modcard{{border:1px solid var(--line);border-radius:20px;padding:26px;margin:22px 0;box-shadow:var(--shadow)}}
.modhead{{margin-bottom:16px}}
.modtag{{display:inline-block;background:var(--soft);color:var(--teal-d);font-weight:700;font-size:12px;letter-spacing:.08em;text-transform:uppercase;padding:5px 12px;border-radius:999px}}
.modhead h2{{font-size:24px;margin:12px 0 4px}}
.modhead p{{margin:0;color:var(--muted);font-size:15px}}
.lessons{{display:grid;gap:10px;margin-top:8px}}
.lesson{{display:flex;align-items:center;gap:16px;padding:14px 16px;border:1px solid var(--line);border-radius:14px;transition:.15s;background:#fff}}
.lesson:hover{{border-color:var(--teal);box-shadow:var(--shadow);transform:translateY(-1px)}}
.lesson .num{{font-family:Poppins;font-weight:800;color:var(--teal);font-size:18px;min-width:34px}}
.ltext{{display:flex;flex-direction:column;flex:1;min-width:0}}
.lt{{font-weight:600}}
.ls{{color:var(--muted);font-size:13px}}
.arr{{color:var(--teal);font-size:20px}}
footer{{background:var(--navy);color:#aebccb;text-align:center;padding:40px 26px;font-size:14px}}
.logo{{font-family:Poppins;font-weight:800;font-size:22px;color:#fff}}
.logo .d{{color:var(--teal)}}
@media(max-width:700px){{.hero h1{{font-size:34px}}.hero{{padding:56px 0 64px}}.stats{{gap:22px}}}}
</style></head>
<body>
<header class="hero"><span class="blob t"></span><span class="blob c"></span>
  <div class="in wrap">
    <span class="eyebrow">&#10022; Self-paced course</span>
    <h1>{head_html}</h1>
    <p>{html.escape(TAGLINE)}</p>
    <div class="stats">
      <div class="stat"><div class="n">{core_modules}</div><div class="l">modules</div></div>
      <div class="stat"><div class="n">{core_lessons}</div><div class="l">lessons</div></div>
      <div class="stat"><div class="n">{core_lessons}</div><div class="l">hands-on capstones</div></div>
    </div>
    {start_btn}
  </div>
</header>
<main class="wrap">
  <div class="intro">Work top to bottom, or jump to the module that fits you. Every lesson defines its terms in plain language, pulls code from the original talk, and ends with a project you build yourself.</div>
  {''.join(cards)}
</main>
<footer><div class="logo">{html.escape(COURSE)}<span class="d">.</span></div>
<p>{html.escape(FOOTER_NOTE)}</p></footer>
</body></html>'''

out = ROOT / "lessons-html" / "index.html"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(PAGE)
print(f"wrote {out} with {len(lessons)} lessons across {len(by_mod)} modules")
