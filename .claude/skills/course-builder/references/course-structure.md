# Course structure: files, config, and conventions

This is the on-disk contract the build scripts rely on. Follow it and
`build_course.py` renders the whole site with no per-course code changes.

## Directory layout

The course is built *in place* in a course root (a folder, often a git repo):

```
<course-root>/
├── course.json                     # branding + module names/blurbs (see below)
├── lessons/                        # you write these (Markdown)
│   ├── module-0-preflight/
│   │   └── 00-pre-flight.md
│   ├── module-1-foundations/
│   │   ├── 01-opening-keynote.md
│   │   └── 02-the-capability-curve.md
│   └── module-2-core-skills/
│       └── 03-....md
├── lessons-html/                   # GENERATED — do not hand-edit
│   ├── index.html                  # the landing page
│   └── module-*/*.html
├── index.html                      # GENERATED — root redirect into the course
├── PROGRESS.md                     # optional learner tracker (see below)
└── COURSE_OUTLINE.md               # optional human-readable outline
```

Rules the scripts enforce:

- Lesson files live **one folder deep** under `lessons/` (`lessons/*/*.md`).
- The folder name is `module-<N>-<slug>`; the file name is `<NN>-<slug>.md`
  where `NN` is the **global** lesson number, zero-padded, and drives ordering
  and prev/next links.
- Every lesson's first line is an H1 exactly like:
  `# Module N · Lesson M: Title` (note the middle dot `·`, U+00B7).
  Files that don't match are skipped with a warning.

## course.json

Drives all branding and the module headings on the landing page. Minimal but
complete example:

```json
{
  "title": "Building with Claude",
  "accent_word": "Claude",
  "tagline": "A hands-on course built from real talks. Learn to prompt, evaluate, and ship, step by step.",
  "source_label": "Code with Claude 2026 · London",
  "start_here": "start-here.html",
  "footer_note": "A self-paced course generated from source talks. Code snippets are illustrative reconstructions; adapt them to the current SDK.",
  "modules": {
    "0": {"name": "Pre-flight: getting ready", "blurb": "Optional on-ramp: accounts, tools, and refreshers to set up before Lesson 1."},
    "1": {"name": "Foundations", "blurb": "Why this matters and where the capability is going."},
    "2": {"name": "Core skills", "blurb": "The everyday fundamentals you'll use in every later module."}
  }
}
```

Fields:

- `title` — course name; shown in the nav, hero headline, footer, and page titles.
- `accent_word` *(optional)* — a word inside `title` to color coral in the hero
  headline. Omit if none.
- `tagline` — one-sentence hero subtitle on the landing page.
- `source_label` — small text in the top strip (e.g. the event or source).
- `start_here` *(optional)* — path to an orientation page; adds a hero button.
  Omit to hide the button.
- `footer_note` — the disclaimer/credit in the footer.
- `modules` — map of module number → `{name, blurb}`. Module `0` is treated as an
  optional pre-flight: it renders as a card but is **excluded from the headline
  counts** (modules / lessons / capstones describe the core curriculum).

## PROGRESS.md (optional learner tracker)

A simple, motivating spine. Include a north-star project (if the course has one),
a daily ritual, and a checklist mirroring the outline, plus a daily-log table:

```markdown
# My progress: {Course title}

**North-star project:** {optional single project every capstone builds toward}.
**Daily ritual:** watch the talk, read the lesson, build the capstone, commit + log, tick the box.
**Goal:** one lesson a day, about two hours.

## Lesson checklist
### Module 1: {name}
- [ ] **Lesson 1:** {title}
- [ ] **Lesson 2:** {title}

## Daily log
| Day | Date | Lesson | What I learned / built | What broke |
|----:|------|--------|------------------------|------------|
| 1 |  |  |  |  |
```

## COURSE_OUTLINE.md (optional, but write it first)

Before writing any lesson, draft the outline: modules with a one-line objective
each, and under each module the ordered lessons with their **"skill gained"**.
This is where you do the re-sequencing work and catch ordering bugs. It doubles
as a human-readable map. Format:

```markdown
## Module 1 — {name}: {module objective in one line}
1. **{Lesson title}** — {speaker}
   *Skill gained:* {the concrete thing the learner can do afterward}.
2. **{Lesson title}** — {speaker}
   *Skill gained:* {…}
```

## Build command

From anywhere:

```bash
python3 <skill>/scripts/build_course.py <course-root>
# or, from inside the course root:
python3 <skill>/scripts/build_course.py
```

It auto-installs `markdown` and `pygments` if missing, renders every lesson,
rebuilds the landing page, and writes the root redirect. Open
`lessons-html/index.html` to view the course.
