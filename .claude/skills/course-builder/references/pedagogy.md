# Pedagogy: how to turn transcripts into a course a beginner can actually follow

This file explains the *why* behind the structure so you can apply judgment, not
just fill templates. The goal of every course this skill produces: **a motivated
beginner can start from scratch and move, lesson by lesson, toward a real
capability they can demonstrate.** Everything below serves that.

## The core problem

Raw transcripts (conference talks, lectures, tutorial series) are optimized for a
*live audience that already has context*, delivered in *presentation order*.
A self-paced beginner has neither the context nor a reason to follow the original
order. So the job is not "clean up the transcript" — it is **re-teach the
material as a learning path**, adding the scaffolding a live talk assumes.

Two levels of design do this: the **macro** (how the whole course is sequenced)
and the **micro** (how each lesson is built). The lesson skeleton lives in
`lesson-template.md`; this file covers the thinking that drives both.

## Macro: sequence for learning, not for delivery

1. **Re-sequence into a path.** Ignore the order the material was delivered in.
   Order it so each piece depends only on earlier pieces. Group related pieces
   into **modules** that go foundational → advanced. Within a module, lessons do
   the same. A learner should never hit a term or tool that a later lesson was
   supposed to introduce.

2. **Name the skill gained.** For every lesson, state the one concrete thing the
   learner can *do* afterward ("choose a model by cost-per-successful-outcome",
   not "understand models"). Progression is measured in capabilities, not topics.
   This also exposes ordering bugs: if lesson B's skill needs lesson D's skill,
   reorder.

3. **Add an optional on-ramp (Module 0) when there's a gap.** Most instructional
   material quietly assumes prerequisites (can code a little, can use a terminal,
   has an account somewhere). Be honest about that gap in a short, optional
   "pre-flight" lesson that installs tools, creates accounts, and does a first
   trivial success — so the real Lesson 1 is spent learning, not fighting setup.
   Mark it optional so people who don't need it skip cleanly.

4. **Interleave, don't silo.** End lessons with "how this connects" notes and add
   "reinforces Lesson X" pointers. Knowledge sticks when it is linked, and it
   stops each lesson from feeling like an island.

5. **Give the course a spine (optional but powerful).** A single north-star
   project that every capstone contributes a component to turns a pile of
   exercises into one thing the learner builds across the whole course. A daily
   ritual (watch → read → build → commit → tick) in a `PROGRESS.md` gives them a
   cadence and a visible finish line.

## Micro: the beginner-safe devices (why each part of a lesson exists)

Each device in `lesson-template.md` solves a specific way beginners get lost:

- **"In one sentence"** — orientation. A learner who knows the destination reads
  everything else as steps toward it instead of disconnected facts.
- **"Where this lesson is heading" + a jump-to-capstone link** — reduces anxiety.
  Showing the finish line first lets nervous learners commit before diving in.
- **First-principles companion** — durability. Tools and model names rot; linking
  each lesson to the timeless idea underneath keeps it valuable and teaches the
  learner to separate the concept from the product.
- **Plain-language glossary, up front** — removes the single biggest beginner
  blocker: undefined jargon. Define terms *before* they're needed, then again
  *in context* the first time they bite. Tell the learner not to memorize — the
  in-context re-definition is the real teaching.
- **"Why this matters"** — motivation. Adults learn what they see a reason to
  learn. Connect to what they already know and name the concrete change.
- **Learning objectives / prerequisites** — a contract. The learner knows what
  they'll be able to do and what they need first. (Objectives also become
  check-off items in the rendered page.)
- **Numbered Parts, one idea each** — cognitive load. Small, self-contained
  chunks with the speaker's real quotes keep faith with the source and are easy
  to hold in mind.
- **Color-coded callouts** — signposting. 🔑 marks the load-bearing idea, 💡 a
  nuance, ✅ the action to take, ❌ the trap, 🎯 the goal. A beginner skimming
  still catches the essentials.
- **Key takeaways + common pitfalls** — consolidation and failure-proofing.
  Pitfalls are especially valuable: naming the mistake a beginner *will* make is
  worth more than another correct example.
- **Capstone with milestones + done-criteria** — the whole point. "Never just
  read, always build." Milestones each work on their own (so a stuck learner
  still shipped something), and objective done-criteria let them self-assess.
- **Graded practice exercises** — optional reps at foundational / intermediate /
  advanced so both the shaky and the confident learner have a right-sized rep.
- **Cheat sheet** — retention. The one artifact they'll screenshot and return to.
- **"How this connects"** — the interleaving, at the lesson level.

## The writing voice

- Warm, plain, and concrete. Short sentences. Second person ("you").
- Define before you use; never assume. When in doubt, over-explain a term once
  rather than lose the reader.
- Faithful to the source: quote the speaker, attribute it, and mark reconstructed
  code as illustrative. Never invent claims the transcript doesn't support.
- Encouraging without hype. The learner should feel capable, not sold to.

## What "good" looks like

A finished lesson passes this test: **a smart person who has never touched the
subject can read it top to bottom, understand every sentence, and finish the
capstone without asking anyone for help.** If any sentence would stop such a
reader, it needs a definition, an example, or a cut.
