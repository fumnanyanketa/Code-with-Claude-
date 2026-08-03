# Module 1 · Lesson 1: What the CCA-F exam is and how to pass it

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 1:** Foundations: how Claude agents work: the exam map and the loop everything builds on
> **Speaker:** Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 30 to 45 minutes (read plus planning)

---

## In one sentence

The Claude Certified Architect: Foundations (CCA-F) exam tests whether you can design and reason about Claude agents across five domains, and the fastest way through it is not to memorize the guide but to build every concept and verify it yourself — because the docs, the AI, and even the exam guide are often wrong.

> 🎯 **Where this lesson is heading.** It builds to a light **Capstone
> Project** where you write your own study plan and stand up a `PROGRESS.md`
> tracker you will tick off across the whole course. There is no code in this
> lesson — it is your orientation and your map. If you want to see the finish
> line first, jump to the **"Capstone Project"** section, then come back.

## A few plain-language basics first

This lesson uses a few terms that show up everywhere later. Here they are in plain words:

- **Certification:** a credential you earn by passing an exam, showing you can do a defined set of things. CCA-F is a certification from Anthropic (the company that makes Claude).
- **Domain:** one of the big subject areas an exam is divided into. CCA-F has five. Each domain is weighted, meaning some are worth more of your score than others.
- **Agent:** an AI that takes a *series* of actions on its own toward a goal, rather than answering in one shot. Most of this course is about designing agents well.
- **MCP (Model Context Protocol):** an open standard, created by Anthropic, for connecting agents to external tools and data. Anthropic invented it, so the exam wants you to know it cold.

You do not need to memorize these. Each is explained again the first time it matters.

## Why this lesson matters

You are about to spend real hours studying, and a map saves you from wandering. This lesson gives you the shape of the exam (how many questions, what score passes, how long you get), the five domains you will be graded on, and a study cadence that actually sticks. Just as important, it sets the *stance* the whole course takes. As Andrew puts it, "I found that often the docs were wrong, the exam guide was wrong, the AI was wrong. And so only by doing it, by going through the process, did we find out the real truth of these tools." That single idea — build it to learn it, then verify — is the difference between passing and getting stuck.

## Learning objectives

By the end of this lesson you will be able to:

1. State the CCA-F exam facts from memory: 60 questions, 720 (72%) to pass, 17 wrong allowed, 120 minutes, verbose multiple-choice.
2. Name the five exam domains and describe roughly how they map onto this course's modules.
3. Explain who the certification is for and how it is currently delivered.
4. Lay out a realistic study cadence and defend why cramming fails.
5. Adopt the course's core stance — build every concept and verify it, because the docs, the AI, and the exam guide are often wrong.

## Prerequisites

- **Module 0 · "Set up your architect's workbench"** (optional). If you already have a working environment and a Claude account, you can skip it. This lesson has no setup requirement — it is reading and planning only.
- Some developer experience is assumed for the course as a whole. As Andrew warns, "This is not an easy course despite them saying that it is. You need to have developer experience." You do not need it for *this* lesson, though.

---

## Part 1: What the CCA-F is, and who it is for

The **Claude Certified Architect: Foundations** is a certification from Anthropic. Its job, in Andrew's words, is to "teach you the broad underlying concepts of building agents, expose you to Claude's models, coding tools, and SDKs." It is aimed at people planning to **adopt Claude for real work inside an organization**, and it leans hard on **MCP** — because Anthropic created MCP and "they really want you to know it in this course."

The exam code is **CCA-F**. Be aware there is technically no official code; as Andrew notes, "this is what everybody is going with."

Consider this certification if any of these fit you:

- You want to **build agentic workflows** effectively.
- You are **adopting Claude as your primary AI driver** within your org.
- You are part of the **Claude partner network**, where it may be a requirement to advance.

> 💡 **A real access catch.** At the time of the course, the official exam is
> "only available to the Claude partner network" — your company needs to qualify
> (roughly ten-plus people and a certain size). If you cannot access the official
> exam yet, ExamPro offers its own version so you can still study and self-certify
> until it goes generally available.

> 🔑 **CCA-F is a foundations-level, org-adoption certification centered on building Claude agents and knowing MCP.**

## Part 2: The five domains (your exam map)

The exam is divided into **five domains**, each weighted differently. These domains are also the backbone of how this course is sequenced. Here they are, with the course modules that carry them:

| # | Domain | What it covers | Where this course teaches it |
|---|---|---|---|
| 1 | **Agentic architecture and orchestration** | How agents are structured: the agentic loop, coordinators, sub-agents, parallel agents | The foundations you are in now, then the orchestration modules |
| 2 | **Tool design and MCP integration** | Giving agents tools; building and wiring MCP servers | The tools and MCP modules |
| 3 | **Claude Code configuration and workflows** | Configuring and driving Anthropic's agentic coding tool | The Claude Code modules |
| 4 | **Prompt engineering and structured output** | Steering the model; making it return machine-readable JSON | The prompting and structured-output modules |
| 5 | **Context management and reliability** | Sessions, context windows, keeping agents dependable | The reliability and context modules near the end |

Two things worth knowing about the weighting and overlap:

- **Claude Code is a big slice.** This is *not* a Claude Code course, but "the middle section here has a lot of Claude Code in it." Andrew estimates roughly half of Domain 2 and all of Domain 3 overlap with his separate *Claude Code Essentials* course — about 30% of the total. If you have taken that, "you are doing really well."
- **Domains 1 and 5 are the new, hard, valuable part.** As Andrew says, "the new content here in Domain 1, especially Domain 5, are extremely valuable, but they're completely new concepts for most people."

> ✅ **What to do about it:** copy this five-row table into your notes now. Every module you finish, mark which domain it just strengthened. That turns a pile of lessons into visible exam coverage.

## Part 3: The exam facts (memorize these)

The exam is delivered through **SkillJar** (the platform Anthropic uses to serve it). Here are the numbers, straight from the course:

```text
Questions:        60, multiple choice
Passing score:    720 out of 1000 (72%)
Wrong allowed:    up to 17
Exam time:        120 minutes (2 hours)
Seat time:        150 minutes (includes intro/instructions)
Pace:             ~2 minutes per question
```

A few notes that matter more than they look:

- **72% is a notch higher than usual.** Andrew points out that comparable certs "usually there's 70%; this one's 72%." Do not plan to squeak by.
- **The questions are verbose on purpose.** They are multiple choice, but "the questions are very verbose... like they're writing solution architect professional questions." The difficulty is often in *parsing* the question, not the concept. That is exactly why you get two minutes each — "take your time reading the questions and absorbing what they're trying to say."
- **You have time.** Two minutes per question is generous. Read carefully; do not rush.

> 🔑 **60 questions, 720 (72%) to pass, 17 wrong allowed, 120 minutes, verbose multiple-choice.** If you remember one slide from this lesson, make it this one.

## Part 4: A realistic study cadence

Andrew's time estimates: a beginner should plan around **30 hours** (possibly more, because the concepts are genuinely new), while an experienced developer doubling the roughly 12 hours of course material lands near **24 hours**. His recommended split is about **50% lectures and labs, 50% practice exams**.

The cadence that works:

- **About one hour a day.** Steady beats heroic.
- **Do not cram it into a single day.** In Andrew's words, "you'll burn out and you won't keep the information."
- **Do not stretch it out forever, either** — "do not take too long, as it will leave your mind."
- **Practice exams are half the work.** ExamPro provides paid practice exams (usually one free), and repeated practice is how the verbose question style stops tripping you.

> 💡 **On the official Anthropic material.** Anthropic has its own free courses with
> "really nice diagrams," but they are concept-based. Andrew is blunt that they are
> "simply not enough" as a sole source: "there's people failing because it doesn't
> stick unless you do it." Treat the official content as a good *second* source, not
> your primary one.

## Part 5: The course's core stance — build it, then verify

This is the idea to carry through every remaining lesson. The concepts here are new enough that the usual sources cannot be trusted at face value. Andrew found this the hard way: "often the docs were wrong, the exam guide was wrong, the AI was wrong. And so only by doing it... did we find out the real truth of these tools."

So the course is deliberately **implementation-focused**. The method is simple and repeats every lesson: **look at a code example, then go implement it** — and when a tool, a doc, or the AI tells you something, confirm it by running it. You will see concrete examples of the sources being wrong very soon (for instance, an SDK that was recently *renamed*, so the AI keeps reaching for the old name). Those are not gotchas to catch you out; they are the reason the labs exist.

> 🔑 **Build every concept and verify it yourself. The docs, the AI, and the exam guide are often wrong — running it is the only way to the truth.**

One practical consequence: this course does **not** cover installing the Agent SDK or Claude Code. Andrew keeps that in his separate *Claude Code Essentials* course on purpose — "I just don't want this course to get bloated and have repetitive content," and setup instructions age faster than concepts. Module 0 of this course points you to that setup; the assumption from here on is that your workbench already runs.

---

## Key takeaways

1. **CCA-F is a foundations-level Anthropic certification** for building Claude agents and adopting Claude in an org, with a heavy emphasis on MCP.
2. **Five weighted domains** structure both the exam and this course: agentic architecture, tool/MCP design, Claude Code, prompting/structured output, and context/reliability. Domains 1 and 5 are the new, hard, valuable part.
3. **The numbers:** 60 questions, 720 (72%) to pass, 17 wrong allowed, 120 minutes, verbose multiple-choice delivered on SkillJar.
4. **Study steadily** — about an hour a day, roughly half labs and half practice exams — not in one burnout day and not dragged out until it fades.
5. **The core stance is build-and-verify.** Do the labs; never trust the docs, the AI, or the guide without running it.

## Common pitfalls

- ❌ **Treating it as a memorization exam.** The verbose questions reward understanding you can only get by building. Reading the guide alone is how people fail.
- ❌ **Using Anthropic's concept courses as your only source.** Nice diagrams, but "not enough" on their own — pair them with hands-on work.
- ❌ **Assuming "not an easy course" means "skip setup."** It assumes developer experience; make sure your Module 0 workbench actually runs before Lesson 2.
- ❌ **Cramming.** One marathon day burns you out and the material evaporates. One hour a day sticks.
- ❌ **Trusting a doc or the AI because it sounds confident.** Later lessons show all three being wrong. Verify by running it.

---

## 🛠️ Capstone Project: Your CCA-F study plan and progress tracker

> This is the hands-on piece for an orientation lesson: not code, but the plan
> and the tracker you will lean on for the rest of the course. It is small on
> purpose, and finishing it means you leave Lesson 1 with a real map, not just
> good intentions.

### What you will build

Two small artifacts, both plain text files in a folder you control:

- **`STUDY-PLAN.md`** — your personal calendar and target date, built from the exam facts and cadence in this lesson.
- **`PROGRESS.md`** — a living checklist you tick off after each lesson, tracking which of the five domains you have strengthened. This is the tracker the whole course leans on, and it is the "piece Atlas Support will stand on": Atlas Support is the one multi-agent system this course builds across every lesson, and your progress tracker is where you will record each component as you add it.

### Why this is the perfect practice

| Lesson idea | Where you use it in your plan/tracker |
|---|---|
| The five domains | Five checkboxes to cover in `PROGRESS.md` |
| Exam facts (60Q / 72% / 120 min) | A target-score line and a practice-exam schedule in `STUDY-PLAN.md` |
| One-hour-a-day cadence | A dated study calendar, not a single cram block |
| 50% labs / 50% practice | Two columns in your tracker so neither half is neglected |
| Build-and-verify stance | A "verified by running it" checkbox on every lab |

### Milestones (build them in order, each one works on its own)

1. **Make the folder and `PROGRESS.md`.** Create a folder for your CCA-F work and add a `PROGRESS.md` with five domain checkboxes and a row per lesson (Lesson · domain · lab done · verified). The smallest working version is five lines you can tick.
2. **Write `STUDY-PLAN.md`.** Record the exam facts (60 questions, 720/72% to pass, 17 wrong allowed, 120 minutes) and pick a realistic finish date at about one hour a day.
3. **Schedule practice exams.** Add at least two practice-exam checkpoints to the plan — one midway, one near the end — so the "50% practice" half is real.
4. **Add the verify column.** In `PROGRESS.md`, give every lab row a "verified by running it" box, so the course's core stance is baked into your tracking.
5. **Tick Lesson 1.** Mark this orientation lesson complete against Domain 1. You have officially started.
6. **Stretch goals.** Put the folder under version control (`git init`) so your progress has history; add a one-line "what surprised me / what the docs got wrong" note per lesson to build the build-and-verify habit early.

### How you will know you are done

- ✅ A `PROGRESS.md` exists with all five domains listed and Lesson 1 checked off.
- ✅ A `STUDY-PLAN.md` states the exam facts and a dated, roughly one-hour-a-day schedule with at least two practice-exam checkpoints.
- ✅ Every planned lab has a "verified by running it" box waiting to be ticked.
- ✅ You can recite the five exam facts without looking.

> 💡 **Keep yourself honest:** a lab only counts when you have *run* it and seen the output yourself — not when you read the code and it looked right. That one rule is the whole course in miniature.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice
> on one idea. Optional and independent; the Capstone already touches all of
> them, so feel free to skip straight to it.

### Exercise 1: Recite the facts (foundational)
Close this page and write down, from memory: number of questions, passing score and percentage, wrong answers allowed, and time limit. Check yourself against Part 3.

### Exercise 2: Map a question to a domain (intermediate)
Take any practice question you can find and decide which of the five domains it belongs to. If you cannot place it, that domain is a gap — note it in `PROGRESS.md`.

### Exercise 3: Plan backward from a date (advanced)
Pick a target exam date. Working back at one hour a day and a 50/50 lab-to-practice split, lay out which weeks cover which domains. If it does not fit, adjust the date rather than the cadence.

---

## Cheat sheet

```text
CCA-F — Claude Certified Architect: Foundations
------------------------------------------------
WHAT   Anthropic foundations cert: building Claude agents, org adoption, MCP-heavy
CODE   CCA-F (unofficial; what everyone uses)
FOR    Agentic-workflow builders · orgs adopting Claude · Claude partner network
ACCESS Official exam via SkillJar; currently partner-network only. ExamPro has a version.

EXAM FACTS (memorize)
  Questions ....... 60, multiple choice (verbose)
  Pass ............ 720 / 1000 = 72%
  Wrong allowed ... 17
  Time ............ 120 min exam · 150 min seat · ~2 min/question

FIVE DOMAINS
  1. Agentic architecture and orchestration   <- new + hard
  2. Tool design and MCP integration
  3. Claude Code configuration and workflows   } ~30% overlaps Claude Code Essentials
  4. Prompt engineering and structured output
  5. Context management and reliability        <- new + hard, high value

STUDY CADENCE
  ~30h beginner / ~24h experienced · 50% labs · 50% practice exams
  ~1 hour/day · don't cram (burnout) · don't drag (forgetting)
  Official Anthropic courses = good 2nd source, not enough alone

CORE STANCE
  Build it -> run it -> verify it.
  Docs, AI, and the exam guide are OFTEN WRONG. Truth = doing it.
```

## How this connects to the rest of the course

- **Earlier, Module 0 · "Set up your architect's workbench":** installed the tools and accounts this course assumes, so from here on you spend your time learning, not fighting setup.
- **Next, Module 1 · "The agentic loop and Claude Code":** you meet the single repeating cycle — gather context, take action, verify — that every agent in this course runs on, and see it live in Claude Code. This is where Domain 1 truly begins.
- **Later, across the course:** each module deepens one of the five domains and adds a component to **Atlas Support**, the multi-agent system you build end to end. Your `PROGRESS.md` from this lesson's capstone is where you will track all of it.

---

*Source: reconstructed from the "Claude Certified Architect: Foundations" course by Andrew Brown (ExamPro). Any code snippets and diagrams elsewhere in this course are illustrative reconstructions of the patterns described; adapt them to the current SDK.*
