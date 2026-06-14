#!/usr/bin/env python3
"""Build a polished, self-contained HTML lesson page from a course markdown file.

Usage:  python3 build_lessons_html.py <input.md> <output.html>

Design goals: on-brand (Anthropic warm palette), readable, and interactive
(sticky TOC + scrollspy, reading progress, dark mode, copy buttons, styled
callouts, check-off for objectives/milestones). One template -> all 37 lessons.
"""
import html
import pathlib
import re
import sys

import markdown
from pygments.formatters import HtmlFormatter

TEMPLATE = r'''<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{TITLE}} | Building with Claude</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Lora:ital,wght@0,500;0,600;1,500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#faf9f5; --surface:#ffffff; --surface-2:#f3f0e7; --text:#2b2a27; --muted:#75716a;
  --accent:#c4623f; --accent-soft:#e9c8b9; --border:#e7e2d6; --shadow:0 1px 3px rgba(40,34,24,.06),0 8px 24px rgba(40,34,24,.05);
  --code-bg:#282320; --max:760px;
  --k:#3b82a6; --k-bg:#e8f1f5; --tip:#b8842f; --tip-bg:#faf2df; --ok:#3f8a52; --ok-bg:#e9f3ea;
  --no:#c0533f; --no-bg:#f7e9e5; --goal:#8257b8; --goal-bg:#f0e9f8; --note:#75716a; --note-bg:#f1efe8;
}
html[data-theme="dark"]{
  --bg:#1b1a17; --surface:#242220; --surface-2:#2e2b27; --text:#ece7dd; --muted:#a39d92;
  --accent:#e08a63; --accent-soft:#5a3f30; --border:#37332c; --shadow:0 1px 3px rgba(0,0,0,.4);
  --code-bg:#1f1c19;
  --k:#7fb6cf; --k-bg:#23323a; --tip:#d9aa55; --tip-bg:#352c1b; --ok:#7bc08c; --ok-bg:#1f2f23;
  --no:#e08a76; --no-bg:#352321; --goal:#b794e6; --goal-bg:#2c2436; --note:#a39d92; --note-bg:#2a2723;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,sans-serif;line-height:1.7;font-size:17px;-webkit-font-smoothing:antialiased}
#progress{position:fixed;top:0;left:0;height:3px;width:0;background:var(--accent);z-index:100;transition:width .1s linear}
.wrap{display:grid;grid-template-columns:280px minmax(0,1fr);gap:48px;max-width:1180px;margin:0 auto;padding:0 32px}
/* Sidebar / TOC */
aside{position:sticky;top:0;align-self:start;height:100vh;overflow-y:auto;padding:28px 0 60px}
.brand{font-weight:700;font-size:14px;letter-spacing:.02em;color:var(--accent);text-transform:uppercase;margin-bottom:4px}
.brand small{display:block;color:var(--muted);font-weight:500;text-transform:none;letter-spacing:0;font-size:12.5px;margin-top:2px}
.toc-title{font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:28px 0 10px}
.toc ul{list-style:none;margin:0;padding:0}
.toc li{margin:0}
.toc a{display:block;color:var(--muted);text-decoration:none;font-size:14px;padding:5px 12px;border-left:2px solid transparent;transition:.15s}
.toc a:hover{color:var(--text)}
.toc a.active{color:var(--accent);border-left-color:var(--accent);background:var(--surface-2)}
.toc .toc li li a{padding-left:26px;font-size:13px}
/* Main */
main{padding:42px 0 120px;min-width:0}
article{max-width:var(--max)}
h1{font-family:Lora,Georgia,serif;font-size:40px;line-height:1.15;margin:0 0 18px;font-weight:600;letter-spacing:-.01em}
h2{font-family:Lora,Georgia,serif;font-size:27px;margin:52px 0 14px;font-weight:600;padding-top:8px;letter-spacing:-.01em}
h3{font-size:20px;margin:34px 0 10px;font-weight:650}
h2+h3{margin-top:18px}
/* Capstone heading: a prominent "hands-on project" banner so skimmers notice it */
h2.capstone-h{background:linear-gradient(120deg,var(--goal-bg),var(--surface));border:1px solid var(--border);border-left:5px solid var(--goal);border-radius:14px;padding:22px 22px 18px;margin-top:60px;box-shadow:var(--shadow);position:relative}
h2.capstone-h::before{content:"HANDS-ON PROJECT";display:block;font-family:Inter,sans-serif;font-size:11px;font-weight:700;letter-spacing:.12em;color:var(--goal);margin-bottom:6px}
.toc a.toc-capstone{color:var(--goal);font-weight:600}
p,li{color:var(--text)}
a{color:var(--accent);text-decoration:none;border-bottom:1px solid var(--accent-soft)}
a:hover{border-bottom-color:var(--accent)}
ul,ol{padding-left:24px}
li{margin:6px 0}
hr{border:none;border-top:1px solid var(--border);margin:40px 0}
strong{font-weight:650}
/* Lesson meta hero */
.lesson-meta{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:18px 22px;margin:0 0 34px;box-shadow:var(--shadow);font-size:14.5px;line-height:1.9}
.lesson-meta p{margin:0;color:var(--muted)}
.lesson-meta strong{color:var(--text)}
/* Tables */
table{border-collapse:collapse;width:100%;margin:22px 0;font-size:15px;display:block;overflow-x:auto}
th,td{border:1px solid var(--border);padding:9px 13px;text-align:left;vertical-align:top}
th{background:var(--surface-2);font-weight:600}
tr:nth-child(even) td{background:var(--surface)}
/* Inline code */
code{font-family:"JetBrains Mono",ui-monospace,Menlo,Consolas,monospace;font-size:.86em;background:var(--surface-2);padding:.12em .4em;border-radius:5px;border:1px solid var(--border)}
/* Code blocks */
.codehilite,pre{position:relative;background:var(--code-bg);border-radius:12px;margin:20px 0;overflow:hidden;box-shadow:var(--shadow)}
.codehilite pre,pre{margin:0;background:transparent;box-shadow:none;border-radius:0}
.codehilite pre,pre>code{display:block;padding:40px 18px 18px;overflow-x:auto}
.codehilite code,pre code{background:none;border:none;padding:0;font-size:13.5px;line-height:1.65;color:#e8e2d6}
.code-bar{position:absolute;top:0;left:0;right:0;height:30px;display:flex;align-items:center;gap:7px;padding:0 14px;background:rgba(255,255,255,.04);border-bottom:1px solid rgba(255,255,255,.06)}
.code-bar .dot{width:11px;height:11px;border-radius:50%}
.dot.r{background:#e0655a}.dot.y{background:#e0b44f}.dot.g{background:#5cae6b}
.copy-btn{position:absolute;top:4px;right:8px;z-index:3;background:rgba(255,255,255,.08);color:#e8e2d6;border:1px solid rgba(255,255,255,.12);border-radius:7px;font-size:12px;padding:4px 10px;cursor:pointer;font-family:Inter,sans-serif;transition:.15s}
.copy-btn:hover{background:rgba(255,255,255,.16)}
.copy-btn.done{background:var(--accent);border-color:var(--accent);color:#fff}
/* Callouts (blockquotes tagged by leading emoji via JS) */
blockquote{margin:22px 0;padding:14px 18px;border-radius:12px;border:1px solid var(--border);background:var(--note-bg);border-left:4px solid var(--note)}
blockquote p{margin:6px 0}
blockquote p:first-child{margin-top:0}blockquote p:last-child{margin-bottom:0}
blockquote.cl-key{background:var(--k-bg);border-left-color:var(--k);border-color:transparent}
blockquote.cl-tip{background:var(--tip-bg);border-left-color:var(--tip);border-color:transparent}
blockquote.cl-ok{background:var(--ok-bg);border-left-color:var(--ok);border-color:transparent}
blockquote.cl-no{background:var(--no-bg);border-left-color:var(--no);border-color:transparent}
blockquote.cl-goal{background:var(--goal-bg);border-left-color:var(--goal);border-color:transparent}
/* Check-off items */
.checkable{list-style:none;padding-left:0}
.checkable li{position:relative;padding-left:34px;cursor:pointer}
.checkable li::before{content:"";position:absolute;left:0;top:4px;width:20px;height:20px;border:2px solid var(--accent);border-radius:6px;background:var(--surface);transition:.15s}
.checkable li.checked::before{background:var(--accent)}
.checkable li.checked::after{content:"✓";position:absolute;left:4px;top:2px;color:#fff;font-weight:700;font-size:14px}
.checkable li.checked{color:var(--muted)}
/* Topbar controls */
.controls{position:fixed;top:14px;right:18px;z-index:60;display:flex;gap:8px}
.ctrl{background:var(--surface);border:1px solid var(--border);border-radius:10px;width:40px;height:40px;cursor:pointer;font-size:17px;box-shadow:var(--shadow);color:var(--text);display:flex;align-items:center;justify-content:center}
.ctrl:hover{border-color:var(--accent)}
#menuBtn{display:none}
footer{max-width:var(--max);margin-top:60px;padding-top:24px;border-top:1px solid var(--border);color:var(--muted);font-size:14px}
/* Emoji bullets keep nice spacing */
h2:first-of-type{margin-top:8px}
@media(max-width:900px){
  .wrap{grid-template-columns:1fr;gap:0}
  aside{position:fixed;top:0;left:0;width:280px;height:100vh;background:var(--surface);border-right:1px solid var(--border);transform:translateX(-100%);transition:.25s;z-index:55;padding:24px;box-shadow:var(--shadow)}
  aside.open{transform:none}
  #menuBtn{display:flex}
  main{padding:64px 0 90px}
  body{font-size:16px}
  h1{font-size:31px}h2{font-size:23px}
}
</style>
</head>
<body>
<div id="progress"></div>
<div class="controls">
  <button class="ctrl" id="menuBtn" title="Contents">☰</button>
  <button class="ctrl" id="themeBtn" title="Toggle theme">🌙</button>
</div>
<div class="wrap">
  <aside id="sidebar">
    <div class="brand">Building with Claude<small>A self-paced course · Code with Claude 2026</small></div>
    <div class="toc-title">On this page</div>
    {{TOC}}
  </aside>
  <main>
    <article>
      <h1>{{TITLE}}</h1>
      <div class="lesson-meta">{{META}}</div>
      {{BODY}}
      <footer>Building with Claude, a self-paced course generated from the Code with Claude 2026 (London) talks. Code snippets are illustrative reconstructions of the approaches shown. Adapt them to the current SDK.</footer>
    </article>
  </main>
</div>
<style>{{PYGMENTS_CSS}}</style>
<script>
// Theme
const root=document.documentElement, tbtn=document.getElementById('themeBtn');
const saved=localStorage.getItem('cwc-theme'); if(saved){root.dataset.theme=saved}
const syncIcon=()=>tbtn.textContent=root.dataset.theme==='dark'?'☀️':'🌙'; syncIcon();
tbtn.onclick=()=>{root.dataset.theme=root.dataset.theme==='dark'?'light':'dark';localStorage.setItem('cwc-theme',root.dataset.theme);syncIcon()};
// Mobile menu
const sb=document.getElementById('sidebar');
document.getElementById('menuBtn').onclick=()=>sb.classList.toggle('open');
sb.addEventListener('click',e=>{if(e.target.tagName==='A')sb.classList.remove('open')});
// Reading progress
const prog=document.getElementById('progress');
addEventListener('scroll',()=>{const h=document.body.scrollHeight-innerHeight;prog.style.width=(h>0?scrollY/h*100:0)+'%'});
// Code blocks: window chrome + copy button
document.querySelectorAll('.codehilite, pre').forEach(block=>{
  if(block.parentElement.classList.contains('codehilite'))return;
  const bar=document.createElement('div');bar.className='code-bar';
  bar.innerHTML='<span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>';
  block.appendChild(bar);
  const btn=document.createElement('button');btn.className='copy-btn';btn.textContent='Copy';
  btn.onclick=()=>{const t=block.querySelector('code')?.innerText||block.innerText;
    navigator.clipboard.writeText(t.replace(/\nCopy$/,''));btn.textContent='Copied!';btn.classList.add('done');
    setTimeout(()=>{btn.textContent='Copy';btn.classList.remove('done')},1500)};
  block.appendChild(btn);
});
// Callout styling by leading emoji
const map={'🔑':'cl-key','💡':'cl-tip','✅':'cl-ok','❌':'cl-no','🎯':'cl-goal','🛠':'cl-goal'};
document.querySelectorAll('blockquote').forEach(q=>{
  const t=(q.textContent||'').trim();
  for(const e in map){if(t.startsWith(e)){q.classList.add(map[e]);break}}
});
// Interactive check-off for "objectives" and "milestone" lists
function makeCheckable(headingMatch){
  document.querySelectorAll('h2,h3').forEach(h=>{
    if(!headingMatch.test(h.textContent))return;
    let el=h.nextElementSibling;
    while(el&&!/^H[1-3]$/.test(el.tagName)){
      if(el.tagName==='OL'||el.tagName==='UL'){
        el.classList.add('checkable');
        el.querySelectorAll(':scope>li').forEach(li=>{
          const key='cwc-chk:'+location.pathname+':'+li.textContent.slice(0,60);
          if(localStorage.getItem(key))li.classList.add('checked');
          li.addEventListener('click',ev=>{if(ev.target.tagName==='A')return;
            li.classList.toggle('checked');
            li.classList.contains('checked')?localStorage.setItem(key,'1'):localStorage.removeItem(key)});
        });
      }
      el=el.nextElementSibling;
    }
  });
}
makeCheckable(/learning objectives|milestones/i);
// Scrollspy
const links=[...document.querySelectorAll('.toc a')];
const ids=links.map(a=>a.getAttribute('href')).filter(h=>h&&h.startsWith('#')).map(h=>h.slice(1));
const heads=ids.map(id=>document.getElementById(id)).filter(Boolean);
const spy=()=>{let cur=heads[0]?.id;for(const h of heads){if(h.getBoundingClientRect().top<140)cur=h.id}
  links.forEach(a=>a.classList.toggle('active',a.getAttribute('href')==='#'+cur))};
addEventListener('scroll',spy);spy();
</script>
</body>
</html>
'''


def convert(md_path: str, out_path: str) -> None:
    raw = pathlib.Path(md_path).read_text()

    # Pull the first H1 as the page title.
    m = re.match(r"#\s+(.+)\n", raw)
    title = m.group(1).strip() if m else "Lesson"
    body_src = raw[m.end():] if m else raw

    # Pull the first blockquote block as the meta hero.
    meta_html = ""
    bm = re.match(r"\s*((?:^>.*\n?)+)", body_src, re.M)
    if bm:
        meta_md = "\n".join(ln.lstrip(">").strip() for ln in bm.group(1).strip().splitlines())
        meta_html = markdown.markdown(meta_md, extensions=["extra", "nl2br"])
        body_src = body_src[bm.end():]

    md = markdown.Markdown(
        extensions=["fenced_code", "tables", "toc", "sane_lists", "attr_list", "codehilite"],
        extension_configs={
            "codehilite": {"guess_lang": False, "css_class": "codehilite"},
            "toc": {"toc_depth": "2-3"},
        },
    )
    body_html = md.convert(body_src)
    toc_html = md.toc

    # Make any "Capstone" section stand out (prominent banner + highlighted TOC link).
    body_html = re.sub(
        r'(<h2 id="[^"]*")(>\s*(?:🛠️?\s*)?Capstone)',
        r'\1 class="capstone-h"\2', body_html)
    toc_html = re.sub(
        r'(<a href="#[^"]*")(>\s*(?:🛠️?\s*)?Capstone)',
        r'\1 class="toc-capstone"\2', toc_html)

    pyg_css = HtmlFormatter(style="gruvbox-dark").get_style_defs(".codehilite")

    out = (TEMPLATE
           .replace("{{TITLE}}", html.escape(title))
           .replace("{{META}}", meta_html)
           .replace("{{TOC}}", toc_html)
           .replace("{{BODY}}", body_html)
           .replace("{{PYGMENTS_CSS}}", pyg_css))
    pathlib.Path(out_path).write_text(out)
    print(f"wrote {out_path} ({len(out)//1024} KB)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: build_lessons_html.py <input.md> <output.html>")
    convert(sys.argv[1], sys.argv[2])
