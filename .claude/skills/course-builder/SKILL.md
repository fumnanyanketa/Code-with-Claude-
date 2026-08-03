---
name: course-builder
description: >-
  Turn transcripts of talks, lectures, tutorials, or video lessons into a
  polished, self-paced HTML course that a total beginner can follow from
  scratch. Use this whenever the user wants to convert one or more transcripts
  (or a video/talk series, or pasted lecture text, or YouTube links) into a
  structured "course", "curriculum", "lesson", "learning path", or "training",
  or says things like "make a course out of this", "turn these talks into
  lessons", "build a curriculum from this transcript", or "teach this to a
  beginner". Trigger even if they don't say the word "course" but clearly want
  instructional material sequenced and explained for learners. This skill
  handles the whole pipeline: re-sequencing raw material into a learning path,
  writing beginner-friendly lessons (glossaries, plain-language explanations,
  hands-on capstones), and rendering them to a styled, interactive course site.
---

# Course Builder

Turn raw instructional material into a self-paced course that moves a beginner,
lesson by lesson, from zero to a demonstrable skill. The output is a set of
Markdown lessons rendered into a polished, interactive HTML site (dark navy hero,
teal/coral accents, sticky TOC, copy-buttons, check-off capstones).

**Read `references/pedagogy.md` before writing anything** — it explains *why* the
structure is what it is, which is what lets you apply judgment instead of just
filling blanks. Two more references carry the details:

- `references/lesson-template.md` — the exact per-lesson skeleton (and which
  parts the renderer depends on).
- `references/course-structure.md` — on-disk layout, `course.json`, `PROGRESS.md`.

The design philosophy in one line: **re-teach the material as a learning path,
adding the scaffolding a live talk assumes** — because raw transcripts are
optimized for a live audience in delivery order, and a self-paced beginner has
neither the context nor a reason to follow that order.

## The pipeline

Work through these five stages. Confirm the plan (stage 2) with the user before
writing all the lessons — sequencing is the highest-leverage decision and the
cheapest to change on paper.

### 1. Ingest the material

Gather every transcript. Accept whatever form the user has:

- **Pasted text or files** — use directly. Save raw transcripts under
  `transcripts/` in the course root so lessons can link to them.
- **YouTube / video links** — you need the transcript text, not the video. Try
  `WebFetch` on the URL to pull captions/description; if that doesn't yield a
  usable transcript, tell the user plainly and ask them to paste the transcript
  (YouTube's "Show transcript" panel, or any captions file). Don't hallucinate
  content you can't see — a course is only as trustworthy as its source.
- **Audio the user will provide** — if they have audio but no text, they'll need
  a transcription step first; point that out rather than guessing at content.

Skim everything before sequencing. Note the natural topics, the difficulty of
each, and what depends on what.

### 2. Sequence into a learning path (get sign-off)

This is the core intellectual work. Following `references/pedagogy.md`:

- Re-order the material so each piece depends only on earlier pieces. Ignore the
  order it was delivered in.
- Group into **modules** (foundational → advanced); order lessons the same way
  inside each module.
- For every lesson, name the **skill gained** (a concrete thing the learner can
  *do* afterward). Use this to catch ordering bugs.
- Decide whether a **Module 0 pre-flight** on-ramp is warranted (does the
  material assume tools/accounts/prior knowledge a true beginner lacks?).
- Decide whether the course has a **north-star project** every capstone builds
  toward.

Write this up as `COURSE_OUTLINE.md` (format in `references/course-structure.md`)
and as `course.json`. **Show the user the outline and confirm** before drafting
lessons. A quick "here's the module/lesson plan and what each one teaches — good?"
saves a lot of rework.

### 3. Write the lessons

One Markdown file per lesson at `lessons/module-N-slug/NN-slug.md`, each
following `references/lesson-template.md` exactly (the H1 format, meta
blockquote, "In one sentence", glossary, objectives, numbered Parts, callouts,
capstone with milestones, cheat sheet, and connections).

Hold every lesson to the bar in `references/pedagogy.md`: *a smart person who has
never touched the subject can read it top to bottom, understand every sentence,
and finish the capstone without asking anyone for help.* Concretely:

- Define every term the first time it appears; keep an up-front glossary too.
- Preserve the speaker's real quotes and attribute them; mark reconstructed code
  as illustrative.
- Make each capstone small, buildable in milestones that each stand alone, with
  objective done-criteria.

For a **long single transcript**, split it into several lessons at natural topic
boundaries rather than making one giant lesson — a beginner needs chunks.

When there are many lessons, writing them is highly parallelizable: each lesson
is independent once the outline is fixed. If subagents are available, dispatch a
batch of lessons in parallel, giving each subagent the transcript excerpt, the
lesson's slot in the outline (number, title, skill gained, neighbors), and
`references/lesson-template.md` + `references/pedagogy.md` to follow. Then review
for consistency.

### 4. Render to HTML

From the course root (or pass it as an argument):

```bash
python3 <skill-path>/scripts/build_course.py <course-root>
```

It auto-installs `markdown` and `pygments` if missing, renders every lesson with
prev/next/home nav, rebuilds the landing page from `course.json`, and writes a
root `index.html` redirect. Open `lessons-html/index.html` to view it.

The three scripts are generic and config-driven — never fork them per course.
All branding flows from `course.json`; all content from the lesson Markdown.

### 5. Add the spine and hand off

- Write `PROGRESS.md` (tracker with the north-star project, daily ritual, and a
  checklist mirroring the outline) — see `references/course-structure.md`.
- Tell the user how to view it (open `lessons-html/index.html`), how to add or
  edit a lesson (edit the Markdown, re-run the build), and how to publish (it's
  static HTML — any static host or GitHub Pages works).

## What makes a course from this skill good

The rendered site is only the surface. The value is the pedagogy: honest
sequencing, every term defined, motivation before mechanics, and a hands-on
capstone at the end of every lesson so the learner is always building, never just
reading. Optimize for the beginner who is starting from scratch — if any sentence
would stop them, it needs a definition, an example, or a cut.
