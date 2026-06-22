# Repository STATUS — deep-dive audit

*Audit date: 2026-06-22 (refreshed). Branch audited from: `claude/adoring-goldberg-ea136u`. This file reports only what is actually in the files, not what branch names or commit messages claim.*

> **Refresh note (what the first pass under-stated):** the earlier version of this file
> asserted the branch facts without showing an *authoritative server-side* branch count, and
> it predated its own STATUS.md commit. This pass fixes both: branch count is now taken from
> `git ls-remote --heads origin` (the server, not the local clone), the orphan/shared-history
> question is answered explicitly, and the branch table reflects that `adoring-goldberg` is now
> exactly **1 commit ahead** of `youtube` — and that single commit is *this STATUS.md and nothing
> else*. No substantive findings changed; all were independently re-verified.

---

## 0. Diagnostic — authoritative branch count

Queried the server directly, not the local clone:

```
git ls-remote --heads origin   →  2 branches (AUTHORITATIVE)
git branch -r (locally visible) →  2 branches
```

- **Server is the source of truth: there are exactly 2 branches.** Local clone matches (2 = 2); nothing hidden.
- **Both branches share history** (merge-base = `ebb25d5`). **Neither is an orphan.** `youtube` (40 commits) is a strict ancestor of `adoring` (41 commits).
- This is **one project on two branches**, not two separate projects.

---

## TL;DR

This repo is **two things stacked on top of each other**:

1. **A transcript archive** of the *Code with Claude 2026 (London)* conference — 37 talks, plain + timestamped text. **Real, complete, useful.**
2. **A self-paced course ("Building with Claude")** re-sequenced from those transcripts into 9 modules / 38 lesson Markdown files (~162,000 words), rendered to HTML with a working Python build pipeline, a landing page, and a GitHub Pages deploy. **Substantially complete as reading material.**
3. **An "AtlasOS" north-star project scaffold** — 8 component folders that are **empty except for README stubs with TODO checklists.** Zero implementation. This is the learner's intended homework, and **none of it has been started.**

The content/archive is genuinely done. The "build a platform as you learn" half is 100% scaffold, 0% built. The daily-progress log is empty (Day 1 blank, no lesson boxes ticked).

---

## 1. Branch-by-branch

**2 branches, both confirmed against the server. No `main` / default branch exists.** They share history (not orphans); the only difference between them is this STATUS.md.

| Branch | Last commit | vs `youtube` (de-facto base) | Commits | What's actually inside | Flag |
|---|---|---|---|---|---|
| `claude/youtube-playlist-transcripts-qkwwis` | 2026-06-16 (`ebb25d5`) | base | 40 | The full repo: transcripts, course, HTML, AtlasOS scaffold. **This is the branch the GitHub Pages workflow deploys from** (`.github/workflows/pages.yml` triggers only on push to this branch). | Active / canonical |
| `claude/adoring-goldberg-ea136u` | 2026-06-22 (`b7fc021`) | +1 / −0 | 41 | Identical tree to `youtube` **plus this STATUS.md** (the only added file, 109 lines). No other unique content. | Audit branch (otherwise a duplicate) |

**Findings:**
- **No unmerged or stranded work** anywhere. `youtube` is a strict ancestor of `adoring`; the lone extra commit is the audit file itself.
- **Without STATUS.md the two branches are byte-for-byte identical.** `adoring-goldberg` exists only as a duplicate pointer (now carrying this report).
- **Stale content:** the last *real* work (everything except STATUS.md) is 2026-06-16 — ~6 days before this audit. Not abandoned, but idle.
- **Deploy mismatch risk:** the Pages workflow only republishes on pushes to `claude/youtube-playlist-transcripts-qkwwis`. Work landing on any other branch (including this audit branch) will **not** trigger a site rebuild.
- **No orphan branches, no hidden branches, no second project.** What you see is the whole repo.

---

## 2. What this project actually is

A **personal learning curriculum built from conference talks.** Someone scraped two YouTube playlists from *Code with Claude 2026 (London)*, transcribed 37 talks (via captions where available, Whisper audio transcription otherwise — 2 talks were deleted by the uploader and are unrecoverable), then hand-wrote those into a structured 9-module self-paced course about building with Claude (prompting, evals, Claude Code, managed agents, cloud deploy, leadership, case studies).

Layered on top is **"AtlasOS"** — a fictional north-star product (a fleet of cooperating AI agents: Atlas/Cortex/Scout/Forge/Pulse/Herald/Warden) that the learner is *supposed* to build incrementally, one component per module, as they work through the course. It exists only as a design brief + architecture doc + roadmap + empty component folders.

In plain language: **it's a course you read, plus a project skeleton you're meant to fill in yourself, plus the raw transcripts both were made from.** It is not a software product, library, or app.

---

## 3. Built vs stubbed

### Genuinely built (real content)
- ✅ **37 transcripts**, plain + timestamped = **74 files**, none empty. (`transcripts/`)
- ✅ **38 lesson Markdown files** (37 lessons + Module 0 pre-flight), ~162k words, substantive. Each of the 37 lessons carries a "First-principles companion" with paper links. (`lessons/`)
- ✅ **HTML build pipeline** — 5 Python scripts (`extract_transcripts.py`, `transcribe_audio.py`, `build_lessons_html.py`, `build_index.py`, `build_course.py`) that render lessons → HTML with home/prev/next nav.
- ✅ **40 rendered HTML files** + landing page + `start-here.html`, in sync with the Markdown. (`lessons-html/`)
- ✅ **Navigation/index docs:** `README.md`, `COURSE_OUTLINE.md`, `TABLE_OF_CONTENTS.md` — all detailed and consistent.
- ✅ **GitHub Pages deploy** workflow + root redirect (`index.html`) + `.nojekyll`.
- ✅ **AtlasOS design docs** — `00-company-brief.md`, `01-architecture.md`, `02-roadmap.md` are thoughtful and complete *as documents*.

### Stubbed / placeholder / empty
- ❌ **All 8 AtlasOS component folders** (`orchestrator/`, `agents/`, `memory/`, `prompts/`, `evals/`, `tools/`, `deploy/`, `ops/`) contain **only an 11–17 line README with a TODO checklist.** No code, no configs, no agents. `find atlas -type f ! -name '*.md'` returns nothing.
- ❌ **Every course capstone** (the actual "build it" exercise in each lesson, e.g. "CurveRider", "Scout") is **unbuilt.**
- ❌ **`PROGRESS.md` daily log is empty** — Day 1 row blank, zero of 38 lesson checkboxes ticked.

### Rough % complete
| Lens | Estimate |
|---|---|
| As a **transcript archive** | ~95% (2 talks permanently unrecoverable) |
| As a **readable course** | ~90% (content + rendering + nav all done; minor polish only) |
| As the **"build AtlasOS as you learn" portfolio** | **~5%** (docs/scaffold only; zero capstones built; progress log empty) |
| **Whole repo, weighted by stated ambition** | **~45%** |

---

## 4. What's left, and the single biggest blocker

**What's left:** the entire *practice* half — building the 37 lesson capstones and assembling them into AtlasOS, plus filling the daily log.

**Single biggest blocker:** this is **work only a human learner can do, one lesson per day over ~weeks.** The "incomplete" portion is, by design, homework — not an engineering gap an agent can close in one pass. Until someone actually sits and works the course, the AtlasOS half stays a skeleton. There is no technical blocker; the blocker is **time + human effort + a decision to commit to the program.**

Secondary blocker: **the deploy is wired to one specific branch**, so the published site can silently go stale if work continues elsewhere.

---

## 5. Quick wins (nearly done)

- **Consolidate branches.** The two branches are identical; one is redundant. Pick the canonical branch (the youtube one, since the workflow targets it) and delete or repoint the other.
- **Establish a real default branch.** There's no `main`/`HEAD`. Set one so "ahead/behind" and PRs have a base.
- **Point Pages at the canonical branch deliberately** (or to `main` once it exists) so deploys aren't tied to a long random branch name.
- **Seed `PROGRESS.md` Day 1.** A single filled row turns the empty log into a working ritual.
- **Reconcile the "37 vs 39" count** once in the README header so the headline number is unambiguous (37 transcribed, 2 removed = 39 listed).

---

## 6. Blunt recommendation: **KEEP the archive + course; ARCHIVE the AtlasOS ambition until someone commits to it.**

- The **transcript archive and the written course are worth keeping and publishing** — they're real, polished, and self-contained. Low maintenance, clear value.
- The **AtlasOS north-star is not a project that's "behind schedule"; it's an unstarted curriculum.** Don't treat its emptiness as a bug to fix or a thing to "finish" with code generation — that would defeat the learning purpose. Either commit to working it lesson-by-lesson, or **archive the scaffold honestly** as "intended exercises, not yet built" so no one mistakes it for in-progress engineering.
- **Don't discard anything** — there's no dead/broken code and no stranded work. But **do collapse the duplicate branch** and establish a default branch; the current two-identical-feature-branches-no-main setup is the only structurally messy thing here.
- This is a **standalone learning repo**; there's nothing here to merge into another project.

---

## Next actions

- [ ] Designate a default branch (create `main` from `ebb25d5`) so the repo has a base for PRs and diffs.
- [ ] Delete or repoint the redundant `claude/adoring-goldberg-ea136u` branch after STATUS.md is reviewed; keep one canonical branch.
- [ ] Update `.github/workflows/pages.yml` to deploy from the canonical/default branch instead of a hard-coded feature-branch name.
- [ ] Decide explicitly: **commit to working the course** (start ticking `PROGRESS.md`) **or archive the AtlasOS scaffold** as "exercises, not built."
- [ ] Add one honest line to `atlas/README.md` stating the components are unimplemented stubs, so it's not mistaken for in-progress code.
- [ ] Seed `PROGRESS.md` Day 1 and tick Module 0/Lesson 1 to make the daily ritual real.
- [ ] Reconcile the talk count (37 transcribed / 2 removed / 39 listed) consistently across `README.md`, `COURSE_OUTLINE.md`, and `TABLE_OF_CONTENTS.md`.
