# Lesson template (the per-lesson skeleton)

Every lesson is a Markdown file that follows this exact skeleton. The order is
deliberate — it takes a beginner from "why am I here" to "I built the thing"
without ever leaving them behind. Write one `.md` file per lesson at
`lessons/module-N-slug/NN-slug.md` where `NN` is the **global** lesson number
(zero-padded), used for ordering and prev/next links.

The renderer (`scripts/build_lesson.py`) reads specific parts of this file to
build the page, so the marked fields are **structural, not optional**:

- The **H1** must be `# Module N · Lesson M: Title`. Everything before the
  first `: ` becomes the hero eyebrow; everything after becomes the big hero
  title (the last word is auto-colored coral).
- The **meta blockquote** (first blockquote, right after the H1) supplies the
  speaker, estimated time, and the "Watch the talk" link.
- The paragraph under **`## In one sentence`** becomes the hero lead.
- The heading containing **"Capstone"** becomes the dark project banner and gets
  the stable `#capstone` anchor.
- Headings named **"Learning objectives"** or **"Milestones"** turn their lists
  into check-off items (persisted in the browser).
- Callouts are ordinary blockquotes whose **first character is an emoji**:
  🔑 key idea · 💡 nuance/tip · ✅ do-this · ❌ pitfall · 🎯 goal · 🛠 project.

Keep the writing plain, warm, and concrete. Define every term the first time it
appears. Preserve the speaker's real quotes when you have the transcript.

---

## The skeleton (copy this, fill it in)

```markdown
# Module {N} · Lesson {M}: {Lesson Title}

> **Course:** {Course title}, a self-paced course
> **Module {N}:** {Module name}: {one-line module theme}
> **Speaker:** {Name, role, org — or "Self-guided" if no talk}
> **Source talk:** [{talk title}]({youtube-url}) · [full transcript]({transcript-path})
> **Estimated time:** {45 to 60} minutes (read plus exercises)

---

## In one sentence

{One dense sentence that captures the whole lesson. This is the promise. It also
becomes the hero lead, so make it self-contained and jargon-light.}

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you build {the thing}. Everything before the Capstone teaches
> the skills you will use there. If you want to see the finish line first, jump
> to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** The talk is recent, but the
> underlying concept is not. For the timeless, tool-agnostic version:
>
> - **[{Canonical source}]({url})** ({paper/book/doc}). {One line on why it is
>   the first-principles account of what this lesson teaches.}

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **{Term}:** {plain-language definition, one or two sentences, no jargon}.
- **{Term}:** {…}

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

{2–4 sentences. Connect to what the learner already knows, name the concrete
change in how they will build/think, and quote the speaker if you can.}

## Learning objectives

By the end of this lesson you will be able to:

1. {Verb-first, testable outcome.}
2. {…}
3. {…}

## Prerequisites

- {Earlier lesson(s) this builds on, or "None".}
- {Any tool/skill assumed, and where it was covered.}

---

## Part 1: {first idea}

{Teach one idea per Part. Lead with the speaker's framing, use their real
quotes, then explain it plainly. Use tables for comparisons and fenced code /
`text` diagrams for structure. Sprinkle callouts where a beginner would trip.}

> 🔑 **{The single most important takeaway of this part, in one line.}**

### {optional sub-point}

{…}

## Part 2: {second idea}

{…}

> ✅ **What to do about it:** {the concrete action this idea implies}.

## Part 3: {how the ideas combine}

{Show how the parts stack into the lesson's central capability. A small ASCII
diagram in a ```text block works well here.}

---

## Key takeaways

1. **{Bolded headline}.** {One line.}
2. {…}

## Common pitfalls

- ❌ {A mistake a beginner will actually make, and the fix implied.}
- ❌ {…}

---

## 🛠️ Capstone Project: {project name}

> This is the main hands-on project for the lesson. {One line on what the
> learner will feel/prove by building it. Keep it small on purpose.}

### What you will build

{2–4 sentences describing the artifact. Then a short list of its pieces, each
mapped to a lesson idea.}

### Why this is the perfect practice

| Lesson idea | Where you use it in {project} |
|---|---|
| {idea} | {milestone} |

### Milestones (build them in order, each one works on its own)

1. **{Milestone name}.** {What to do. Smallest working version in one line.}
2. **{…}.** {…}
7. **Stretch goals.** {Optional harder extensions.}

### How you will know you are done

- ✅ {Objective, checkable completion criterion.}
- ✅ {…}

> 💡 **Keep yourself honest:** {a one-line discipline tip specific to this build}.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice
> on one idea. Optional and independent; the Capstone already touches all of
> them, so feel free to skip straight to it.

### Exercise 1: {name} (foundational)
{One short paragraph.}

### Exercise 2: {name} (intermediate)
{…}

### Exercise 3: {name} (advanced)
{…}

---

## Cheat sheet

​```text
{A compact, scannable recap of the whole lesson: the key numbers, the named
framework, the do/don't list. This is what the learner screenshots.}
​```

## How this connects to the rest of the course

- **Earlier, Module {X} · Lesson {Y}:** {what it set up that this lesson used}.
- **Next, Module {X}:** {where these skills get practiced or deepened}.
- **Later, Module {X}:** {the advanced payoff}.

---

*Source: "{talk title}" by {speaker}, {event}. Code snippets and diagrams are
illustrative reconstructions of the patterns described in the talk. Adapt them
to the current SDK.*
```

---

## Notes on filling it in well

- **Every section earns its place, but not every section is mandatory.** For a
  lesson with no video (like a setup on-ramp), drop the "Watch the talk" link
  (leave the Source talk line without a URL and the button disappears) and the
  first-principles companion if there is no canonical source. Keep the rest.
- **Capstones ladder toward one thing.** If the course has a north-star project,
  frame each capstone as the component that project needs for this lesson. That
  turns 37 disconnected exercises into one build.
- **The glossary is a promise, not a dump.** Only list terms this lesson uses,
  and still re-define each one in context the first time it bites. Beginners
  read the glossary once and rely on the in-context re-definition.
- **Quotes are the backbone of trust.** When you have the transcript, quote the
  speaker directly and attribute it. Reconstructed code must be marked as
  illustrative (the footer disclaimer does this globally).
