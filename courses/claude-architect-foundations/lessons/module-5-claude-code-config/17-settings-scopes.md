# Module 5 · Lesson 17: Settings scopes and precedence

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 5:** Claude Code configuration & workflows: configure, secure, and automate Claude Code like an architect
> **Speaker:** Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 40 to 55 minutes (read plus lab)

---

## In one sentence

Claude Code reads its configuration from four stacked `settings.json` files — managed, user, project, and local — and when two of them set the same thing, one wins by a fixed precedence order, so an architect's job is to know which file lives where, which scope beats which, and roughly what the whole settings surface can do.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you configure the **Atlas Support** repo with both a shared
> **project** settings file and a personal **local** one, put a *conflicting*
> value in each, and run Claude Code to see with your own eyes which one wins.
> Everything before the Capstone gives you the map — the four scopes, where each
> file lives, and a guided tour of the settings groups. If you want to see the
> finish line first, jump to the **"Capstone Project"** section, then come back.

## A few plain-language basics first

This lesson uses a few terms. Here they are in plain words:

- **Claude Code:** Anthropic's agentic coding tool — a command-line program (a *CLI*) that runs an AI agent over your codebase. This whole module is about configuring it.
- **`settings.json`:** a plain text configuration file, written in **JSON** (a simple, widely used format of keys and values inside curly braces `{ }`). Claude Code reads it at startup to learn your preferences.
- **Scope:** *how widely* a setting applies — to your whole organization, to just you, to one project, or to just your private copy of one project. Each scope has its own settings file.
- **Precedence:** the tie-breaker rule. When two scopes set the same value to different things, *precedence* decides which one Claude Code actually uses.
- **Repo (repository):** a project folder tracked by **git**, the tool that versions your code and syncs it with teammates. Some settings files get *committed* (shared with the team via git); others are deliberately kept out.
- **Permission rule:** an allow / ask / deny rule controlling what Claude Code is allowed to do. You will meet these properly in the very next lesson; here they are just one of many settings groups.
- **MCP (Model Context Protocol):** an open standard, created by Anthropic, for connecting an agent to external tools and data through *MCP servers*. Settings can control which servers are allowed.
- **Hook:** a script Claude Code runs automatically at certain moments (for example, before it edits a file). Also just one settings group here; a later module covers hooks in depth.

You do not need to memorize these. Each is explained again the first time it matters.

## Why this lesson matters

Every later lesson in this module — permissions, sandboxing, hooks, MCP controls — is *set through a settings file*. If you do not know which file to edit, or why your change is being silently overridden by another scope, you will fight the tool instead of driving it. This lesson is the foundation the rest of the module stands on: it teaches you the four places settings can live, the exact order in which they override each other, and a fast tour of what you can actually configure. As Andrew frames the tour: "my goal here is not to make you remember them here. That's not important. What's important is to get exposure to understand what settings are available to us because we're going to repeat it out throughout this course when we need to look at those settings." So relax about memorizing every key — but do lock in the *scopes and precedence*, because that is the part that bites people.

## Learning objectives

By the end of this lesson you will be able to:

1. Name the four settings scopes — **managed**, **user**, **project**, **local** — and say who each is for.
2. State the file path where each scope's settings live, and which one is deliberately *not* committed to git.
3. State the precedence order and predict, for a conflicting value, which scope wins.
4. Recognize the main settings *groups* (auth, session, env, model, output, UI/spinners, permissions, MCP, hooks, observability) well enough to know where to look later — without memorizing every key.
5. Edit a settings file to change Claude Code's behavior, and describe when a change takes effect (and when you must restart the session).

## Prerequisites

- **Module 1** — you know what Claude Code is and have run a session.
- A working Claude Code install and a terminal. This lesson has you edit files and restart sessions.
- Comfort reading a small block of JSON. If `{ "key": "value" }` looks familiar, you are ready.

---

## Part 1: Four scopes, from the whole org down to just you

There is not *one* `settings.json`. As Andrew puts it: "there's a settings JSON file, but there's a little bit more to it because you have to take in consideration at what scope it is being utilized at." Claude Code layers **four** settings files, each covering a different *scope* — a different breadth of who and what the setting applies to. Working from the widest to the narrowest:

- **Managed settings** — "the highest level of settings for cloud code. This is for organization-wide instructions and it's going to be managed by your IT and DevOps team." This is the lockdown layer: a company sets it once, and individuals cannot override it. **Some settings can *only* live here** (you will see which in the tour).
- **User settings** — "your personal preferences across all projects." This is *you*, everywhere. Set your spinner style or language once and it follows you into every repo.
- **Project settings** — settings that belong to a specific project and are **checked into git**, so the whole team shares them. Think: the permission rules and MCP servers this repo needs.
- **Local settings** — "project specific, but it doesn't get checked into your git repo." This is your *private* override for one project — your personal tweaks that you do not want to force on teammates.

> 🔑 **Four scopes, widening out: managed (the org) → user (you, everywhere) → project (this repo, shared) → local (this repo, just you, uncommitted).**

The single most important distinction between the two project-level scopes: **project** is committed and shared; **local** is *never* committed. That is why `.local` exists — so you can bend a shared project's config to your own taste without changing what your teammates get.

## Part 2: Where each file actually lives

Knowing the scopes is half of it. The other half is knowing which file on disk to open. Here is where each one lives. (Paths use `~` for your home directory, the standard shorthand on macOS and Linux; on Windows the home directory is your user folder.)

| Scope | File | Committed to git? | Who controls it |
|---|---|---|---|
| **Managed** | `managed-settings.json` in a system location (e.g. `/etc/claude-code/` on Linux, `/Library/Application Support/ClaudeCode/` on macOS) | No — it lives on managed machines | IT / DevOps, org-wide |
| **User** | `~/.claude/settings.json` | No — it is in your home dir | You, across all projects |
| **Project** | `.claude/settings.json` (inside the repo) | **Yes** — shared with the team | The team |
| **Local** | `.claude/settings.local.json` (inside the repo) | **No** — add it to `.gitignore` | You, for this repo only |

Andrew's own words tie the pattern together: managed settings live "on your servers" in a special `managed-settings.json`; user settings live in "your home directory... tilde /cloud [`~/.claude`]"; project settings sit in "your repo... in a similar folder" (`.claude/`); and "local will just have `local` [in the name]... and that's how you're going to distinguish it" — `settings.local.json`.

> 💡 **The naming is the whole trick.** All four are `settings.json` *except* local,
> which is `settings.local.json`. The `.local.` in the middle of the filename is
> how Claude Code — and you — tell the personal, uncommitted one apart from the
> shared one. A file named `local.settings.json` is just a typo, not a local
> settings file; Andrew catches himself on exactly this in the lab.

## Part 3: Precedence — who wins when two scopes disagree

This is the part to actually internalize. When the same setting appears in two files, Claude Code does not merge them or pick at random — it applies a fixed **precedence** order. Andrew states the governing idea plainly: "the priority of what takes precedence is what's higher in scope. So something higher in scope is going to take precedence over settings in the lower scope."

The top of that order is never in doubt: **managed wins over everything.** That is the entire point of the managed layer — so an organization can enforce a rule no individual can undo.

Below managed, the rule that actually bites day to day is: **the more specific the scope, the more it wins.** Your private, per-repo override beats the shared project file, which beats your global defaults. Concretely, from strongest to weakest:

```text
Highest precedence (wins the conflict)
  1. MANAGED    managed-settings.json      org lockdown, cannot be overridden
  2. LOCAL      .claude/settings.local.json your private, uncommitted per-repo override
  3. PROJECT    .claude/settings.json       the shared, committed team config
  4. USER       ~/.claude/settings.json     your global default across all projects
Lowest precedence (loses the conflict)
```

Read it as a fallback chain from the bottom up: your **user** settings are the baseline you carry everywhere; a **project** can override that baseline for one repo; your **local** file can override the project just for you; and **managed** can override anything, for the whole org.

> 🔑 **Managed beats local beats project beats user. The narrower and more personal
> the scope (short of the org lockdown), the more it wins.**

> 💡 **A build-and-verify note — the one place the spoken order can mislead.**
> Andrew's slide walks the scopes top-to-bottom as managed → user → project →
> local, and it is easy to hear that as the precedence order too. But think about
> what `.local` is *for*: it is your personal, uncommitted override of the shared
> project file. An override that could not out-rank the thing it overrides would
> be useless. So in a real conflict, **local wins over project, and both win over
> user** — the opposite of the "local is lowest" reading. This course's whole
> method is *build it and check it*, and this is a perfect case: do not take the
> ordering (or this lesson) on faith. The Capstone has you set the same key in
> project and local, run Claude Code, and watch which value it actually uses.

## Part 4: A tour of the settings surface (for exposure, not memorization)

Now the map of *what* you can configure. Andrew is emphatic about how to take this: "my goal here is not to make you remember them here... What's important is to get exposure." So skim it. The point is to know a group *exists* so you can find it later — "we'll figure it out as we go." Almost everything below goes in the ordinary `settings.json`; a few are **managed-only**, flagged as such.

| Group | What it controls | Notable items |
|---|---|---|
| **Authentication** | How Claude Code logs in and gets credentials | Custom API-key helper script; AWS SSO refresh/login; force a login method (Claude AI vs API console); export native credentials |
| **Session & storage** | Where sessions live and how long | `cleanupPeriodDays` (**default 30**); set it to **0** to delete sessions at startup and disable persistence entirely; custom auto-memory directory (**not allowed in project settings**); plans directory |
| **Environment variables** | Env vars applied to every session | An `env` block so a variable is set for all runs |
| **Model** | Which model, and from where | Override the default model; restrict the list of choosable models; map model IDs to a provider (e.g. Amazon Bedrock); thinking-always-on; per-session opt-in "fast mode" |
| **Output & language** | How responses read | Output style (`explanatory`, `learning`, …); **preferred response language**; git-instruction inclusion |
| **Git attribution** | Commit authorship | Note: the `includeCoAuthoredBy` option is now **deprecated** |
| **Announcements & updates** | Startup messages and updates | Cycled startup messages (handy for team reminders); auto-update channel |
| **UI & spinners** | The look of the running indicator | Show turn duration; **spinner verbs** (the words that animate while it works); spinner tips on/off and overrides; reduce spinners/shimmers/flashes for accessibility |
| **Agent team** | Multi-agent teammate layout | Teammate mode: inline, split-pane, or split panes in **tmux** (a terminal tool for split screens) |
| **Permission rules** | What Claude may do | `allow` / `ask` / `deny` for tools (read, edit, bash, web fetch, MCP, sub-agents); extra directory access; default mode; disable bypass-permissions mode — **the whole next lesson** |
| **MCP servers** | Which MCP servers are trusted | Auto-approve all; approve specific; disable specific; **allow-list by server name (managed-only)** |
| **Plugin marketplace** | Where plugins may come from (**managed-only**) | Restrict to known marketplaces; block marketplaces; trust-warning text |
| **Managed lockdown flags** | Org restrictions (**managed-only**) | Allow managed permission rules only; restrict to MCP servers and hooks only |
| **Hooks** | Scripts run at lifecycle moments | Enable/disable; allowed hook URLs; allowed env vars; the hooks themselves — **its own module later** |
| **Observability, status line, IO, misc** | Telemetry and terminal polish | OpenTelemetry (OTEL) headers helper; status-line config; custom file-suggestion script; `respectGitIgnore` (hide git-ignored files from the picker) |

> 💡 **The two things to actually take from the tour.** First: a handful of
> settings are **managed-only** — MCP allow-lists by name, plugin-marketplace
> rules, and the lockdown flags — because they are org-level guardrails an
> individual should not be able to loosen. Second: `cleanupPeriodDays` defaults to
> **30**, so sessions older than a month are cleaned up; if that matters to you,
> back them up or raise the number. Everything else you can look up when you need
> it.

## Part 5: When does a settings change take effect?

You edit a settings file — does Claude Code pick it up immediately? Andrew tests exactly this in the lab and reaches a clear, useful conclusion: **not live.** He changes his spinner verbs mid-session, keeps working, and the old verbs keep showing. He hunts for a reload: "how can we reload our settings... without having to completely go out?" He tries the built-in reload options — "refresh or reload, reload plugins, remote environment. I don't see any option there." His verdict: "really seems like the only way to reload it is to exit it out. I'm just not convinced that changing settings takes effect until you go in and leave again."

So the reliable rule: **edit the file, then exit and restart the Claude Code session.** On the next launch, the new settings are in force. (Exiting and re-entering is exactly what makes his `computing` spinner verb finally appear.)

> ✅ **What to do about it:** treat settings edits like config, not like chat.
> Change the file, quit the session, relaunch. If a change "isn't working,"
> restart before you assume the setting is wrong — nine times out of ten it just
> had not been reloaded.

---

## Key takeaways

1. **Four scopes, widening out.** Managed (org) → user (you, everywhere) → project (this repo, shared) → local (this repo, just you). Each is a `settings.json`; only local is `settings.local.json`.
2. **Locations matter.** Managed in a system path; user in `~/.claude/`; project and local both in the repo's `.claude/`. Project is committed to git; **local is not**.
3. **Precedence: managed > local > project > user.** Managed always wins (org lockdown); below it, the narrower/more-personal scope wins. Local overrides the shared project file — that is what `.local` is *for*.
4. **The surface is broad; the goal is exposure.** Know the groups exist (auth, session, env, model, output, UI, permissions, MCP, hooks, observability). A few are managed-only. Do not memorize keys.
5. **Changes need a restart.** There is no reliable live reload — edit, then exit and relaunch the session.

## Common pitfalls

- ❌ **Editing the wrong scope.** You put a fix in your **user** file, but the **project** (or **local**) file already sets that key — so your change is overridden and looks broken. Check which scope owns the value.
- ❌ **Assuming project beats local.** It is the reverse. Your uncommitted `settings.local.json` overrides the shared `settings.json`. If a teammate's setting "won't stick," a personal local override may be shadowing it.
- ❌ **Committing `settings.local.json`.** It is meant to stay out of git. Commit it and you push your private overrides onto the whole team. Add it to `.gitignore`.
- ❌ **Filename typos.** `local.settings.json` or `settings.local.jsonc` will simply be ignored. It must be exactly `settings.local.json`. Andrew narrowly avoids this in the lab.
- ❌ **Expecting a live reload.** You change a setting, it doesn't take effect, you conclude it is unsupported. Restart the session first.
- ❌ **Trying to loosen a managed-only setting from user/project.** MCP name allow-lists, marketplace rules, and lockdown flags only work in `managed-settings.json`. By design, you cannot override them.

---

## 🛠️ Capstone Project: Configure Atlas Support and prove precedence

> This is the hands-on piece for the lesson. It is small on purpose. By the end
> you will have felt the precedence rule instead of just reading it — you will
> set the *same* value in two scopes and watch Claude Code pick a winner.

**Atlas Support** is the one system this course builds end to end — a multi-agent support assistant that grows lesson by lesson. Everything Atlas Support does later (permissions, MCP tools, hooks, hardened config) is switched on through the settings files you are about to create. This Capstone lays that foundation: a repo with a shared **project** config and your personal **local** override, plus a small experiment that proves how they interact.

### What you will build

A `.claude/` folder inside an `atlas-support` repo containing two settings files:

- **`.claude/settings.json`** — the shared, committed **project** config (the team's baseline).
- **`.claude/settings.local.json`** — your private, uncommitted **local** override.

You will put a **conflicting value** in both — a harmless, visible one like the spinner verbs — then run Claude Code and confirm which scope's value actually appears.

### Why this is the perfect practice

| Lesson idea | Where you use it in the Capstone |
|---|---|
| Four scopes | You create the project and local files by hand |
| File locations & naming | You place them in `.claude/` with the exact `settings.local.json` name |
| Committed vs not | You add `settings.local.json` to `.gitignore` |
| Precedence (local > project) | You set the same key in both and observe the winner |
| Restart to reload | You relaunch the session to make each change take effect |
| The settings surface | You touch a real group (UI/spinners, and optionally language) |

### Milestones (build them in order, each one works on its own)

1. **Make the repo and the `.claude/` folder.** Create an `atlas-support` directory, run `git init`, and make a `.claude/` folder inside it. Add a tiny file (a `README.md` with "hello") so the repo isn't empty. Smallest working version: the folder exists.

   > 💡 **A build-and-verify moment baked in.** Andrew expected `claude` — and
   > even `claude` running `/init` — to create the `.claude/` folder and a
   > settings file for him. In the lab it *did not*: "we still don't have a claude
   > directory... I thought for certain that was going to create it for us." Do not
   > assume the tool scaffolds these. If the folder or file is missing, make it
   > yourself. That expectation-vs-reality gap is exactly the course's method:
   > check, don't assume.

2. **Write the project settings.** In `.claude/settings.json`, set the spinner verbs to one clearly recognizable value — for example a single verb, `"Building"`, in **replace** mode so only your verb shows. (Spinner-verb configuration is illustrative; look up the exact key in Claude Code's settings schema, as Andrew does when he searches it for "spinner verbs" and the `mode` of `append` vs `replace`.)

   ```json
   // .claude/settings.json  (project — committed; illustrative)
   {
     "spinnerVerbs": { "mode": "replace", "verbs": ["Building"] }
   }
   ```

3. **Prove it works, alone.** Launch Claude Code in the repo, give it any small task, and confirm the spinner now says **Building**. Remember: if you edited while a session was open, **exit and relaunch** — there is no live reload.

4. **Add the conflicting local override.** Create `.claude/settings.local.json` with the *same* key set to a *different* value — for example `"Computing"` (Andrew's own choice: "so now my sanity is back"). Restart the session.

   ```json
   // .claude/settings.local.json  (local — NOT committed; illustrative)
   {
     "spinnerVerbs": { "mode": "replace", "verbs": ["Computing"] }
   }
   ```

5. **Observe the winner and name the rule.** Run a task again. You should see **Computing**, not Building — **local beat project**. Write one sentence in your notes stating the rule you just verified: *local overrides project.* If instead you assumed project would win, you have just learned the lesson the hard way, which is the best way.

6. **Keep local out of git.** Add `.claude/settings.local.json` to `.gitignore` and confirm `git status` no longer lists it. Your private override must never be pushed to the team.

7. **Stretch goals.**
   - **User scope:** copy the spinner setting into `~/.claude/settings.json` (Andrew does this so he "never ever" sees the default verbs again), then open a *different* repo with no spinner setting and confirm your user default now applies there.
   - **Language override:** add a preferred-response-language setting (Andrew tries Japanese) and confirm Claude Code replies in that language even when you ask in English — "Oh, it did. Perfect." Spell the key correctly, as he warns: "to make it work, I think you got to spell language correctly."
   - **Three-way conflict:** set the same key in user, project, and local, and confirm local still wins — then reason about what a **managed** file would do on top.

### How you will know you are done

- ✅ An `atlas-support` repo exists with `.claude/settings.json` and `.claude/settings.local.json`.
- ✅ Both files set the same spinner-verb key to *different* values.
- ✅ Running Claude Code shows the **local** value, and you can state why (local > project).
- ✅ `settings.local.json` is git-ignored and does not appear in `git status`.
- ✅ You can name all four scopes, their file locations, and the precedence order from memory.

> 💡 **Keep yourself honest:** the milestone is not "I wrote two files." It is "I
> saw the local value win and can explain the precedence." If you only read the
> rule and nodded, you skipped the lesson — run it and watch the spinner change.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice
> on one idea. Optional and independent; the Capstone already touches all of
> them, so feel free to skip straight to it.

### Exercise 1: Locate every file (foundational)
On your own machine, find (or note the path of) all four settings files: managed, user (`~/.claude/settings.json`), project, and local. State which of the four are — or would be — committed to git.

### Exercise 2: Predict the winner (intermediate)
Given `model` set to different values in user, project, and local (no managed file), write down which value Claude Code uses *before* testing, then verify with a quick change and restart. Then imagine a managed file also sets `model`; state the new winner.

### Exercise 3: A managed-only guardrail (advanced)
Pick one **managed-only** setting from the tour (an MCP name allow-list, a marketplace restriction, or a lockdown flag). Explain in two or three sentences *why* it makes sense that an individual user cannot set it in their user or project file — connect it to who the managed scope is for.

---

## Cheat sheet

```text
CLAUDE CODE SETTINGS — SCOPES & PRECEDENCE
------------------------------------------
FOUR SCOPES (widening out)
  MANAGED   org-wide, IT/DevOps    some settings ONLY here
  USER      you, all projects
  PROJECT   this repo, shared
  LOCAL     this repo, just you    NOT committed

WHERE THEY LIVE
  MANAGED   managed-settings.json  (system path: /etc/claude-code, /Library/... )
  USER      ~/.claude/settings.json
  PROJECT   .claude/settings.json           <- committed to git
  LOCAL     .claude/settings.local.json     <- git-ignore this one

PRECEDENCE (who wins a conflict)   highest -> lowest
  MANAGED  >  LOCAL  >  PROJECT  >  USER
  (managed = org lockdown; below it, narrower/more-personal wins)
  Rule that bites: LOCAL overrides PROJECT overrides USER.

RELOAD
  No reliable live reload. Edit -> EXIT -> relaunch session.

SETTINGS GROUPS (exposure, don't memorize)
  auth · session/storage (cleanupPeriodDays=30, 0=disable persistence)
  env · model · output+language · git-attribution (co-author deprecated)
  announcements/updates · UI+spinners (spinner verbs!) · agent team
  permissions (next lesson) · MCP servers (name-allowlist = managed-only)
  plugin marketplace (managed-only) · lockdown flags (managed-only)
  hooks (own module) · observability/status-line/IO (respectGitIgnore)

GOTCHAS
  * settings.local.json must be EXACT — typos are ignored
  * don't commit the .local file
  * managed-only settings can't be set from user/project
  * project does NOT beat local (it's the reverse)
```

## How this connects to the rest of the course

- **Earlier, Module 4 · "MCP — discovery, resources, and building a server":** you gave Atlas Support external tools via MCP. *Which* of those servers are trusted is governed by the MCP settings group you just toured — and, at the org level, by managed-only allow-lists.
- **Next, "Permission rules and modes":** the single biggest settings group gets its own lesson. You will write `allow` / `ask` / `deny` rules — and now you know exactly which scope's file to put them in, and that managed rules will out-rank yours.
- **Later, across Module 5:** sandboxing, hooks, and hardened configuration all flow through these same four files. The scope-and-precedence model from this lesson is the frame you will use every time you change how Claude Code behaves.

---

*Source: reconstructed from the "Claude Certified Architect: Foundations" course by Andrew Brown (ExamPro). Code snippets and settings keys are illustrative reconstructions of the patterns described in the course — confirm exact setting names against Claude Code's current settings schema, exactly as Andrew does in the lab.*
