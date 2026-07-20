# Module 5 · Lesson 18: Permission rules and modes

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 5:** Claude Code configuration & workflows: making Claude Code do exactly what you allow and nothing you don't
> **Speaker:** Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 45 to 60 minutes (read plus lab)

---

## In one sentence

Claude Code decides what it may do through **permission rules** — allow, ask, and deny lists whose precedence is always deny → ask → allow — plus a **permission mode** that sets the default posture (prompt on first use, auto-accept edits, plan-only, and so on); learn the rule syntax for bash, paths, web fetch, and MCP, and you can hand an agent exactly the powers you intend and none you don't.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you write a real permission ruleset for **Atlas Support** — the
> multi-agent system this course builds end to end — that denies dangerous bash,
> asks before edits outside its own folder, and freely allows safe reads, and
> then you *prove each rule fires* by triggering it. Everything before the
> Capstone teaches the syntax and the precedence you will need there. If you want
> to see the finish line first, jump to the **"Capstone Project"** section, then
> come back.

## A few plain-language basics first

This lesson uses a handful of terms. Here they are in plain words:

- **Claude Code:** Anthropic's agentic coding tool — a command-line program (a "CLI") that runs an agent over your codebase, reading files, running commands, and editing code on your behalf.
- **Tool:** a specific capability the agent can invoke — reading a file, running a bash command, fetching a web page. Claude Code has many named tools (Bash, Read, Edit, Grep, Glob, WebFetch, and more). Every permission rule is about one of these tools.
- **Permission rule:** an allow / ask / deny rule that controls what Claude Code may do. Precedence is deny → ask → allow (the most restrictive match wins).
- **Permission mode:** the *default posture* for a session — for example, prompt me the first time each tool is used, or auto-accept file edits, or plan only and change nothing. Modes set the baseline; rules override it for specific tools.
- **`settings.json`:** the JSON file where Claude Code stores its configuration, including your permission rules. (You met the settings *scopes* — global, project, local — in the previous lesson.)
- **MCP (Model Context Protocol):** an open standard, created by Anthropic, for connecting agents to external tools and data through **MCP servers**. Tools that come from an MCP server have their own permission-rule syntax.

You do not need to memorize these. Each is explained again the first time it matters.

## Why this lesson matters

An agent that can edit your files and run shell commands is powerful and, unsupervised, dangerous. Permission rules are the seatbelt: they let you say "read anything, but never run `rm`, and always ask me before touching files outside this project." Andrew frames the whole system with a joke that is actually the key insight: it is a "tiered permission system that is tool-based access controls, or **tabback**" — his play on the familiar "role-based access controls (RBAC)." "You won't find that anywhere on the internet because I just came up with it," he says, but the point sticks: **in Claude Code, permissions are organized around tools, not roles.** Get the rule syntax and the deny → ask → allow precedence right and you control exactly what your agents can do. Get them wrong — a stray colon, a space in the wrong place, a tool you forgot exists — and the agent quietly routes around your rule. This is one of the most exam-dense topics in the course precisely because the syntax has so many small, testable details.

## Learning objectives

By the end of this lesson you will be able to:

1. Write **allow**, **ask**, and **deny** rules and predict which one wins using the **deny → ask → allow** precedence.
2. Name the tools permission rules cover (Bash, Read, Edit, WebFetch, MCP, sub-agents — and the "hidden" ones like Grep and Glob) and explain why denying one tool often is not enough.
3. Write correct **bash** patterns using the wildcard `*`, and know why *spaces matter*.
4. Write **read/edit path** patterns using the four path forms: `//` (filesystem root), `~` (home), `/` (project root), and relative (`./` or none).
5. Write **web_fetch** rules with `domain:` and recognize a bare rule as a catch-all.
6. Write **MCP** rules in `mcp__server` and `mcp__server__tool` form, and use `__*` to match all of a server's tools.
7. Recognize a **bare-name** tool rule (no parentheses) as total coverage for that tool.
8. Choose a **permission mode** — default, acceptEdits, plan, don't-ask, bypassPermissions — and say when each is safe.

## Prerequisites

- **Module 5 · Lesson 17 · "Settings scopes and precedence"** — you should know that permission rules live in `settings.json` and that global, project, and local scopes stack. This lesson goes deep on the *contents* of the permissions block.
- A working Claude Code install (covered in Module 0's setup pointer). You will run a few interactive sessions.
- Comfort reading a small JSON object. No prior security knowledge needed.

---

## Part 1: The three permission levels and their precedence

Every permission rule sets one of three levels for a tool action:

- **allow** — Claude may do it, no prompt.
- **ask** — Claude must ask you first; you approve or reject in the moment.
- **deny** — Claude may not do it, ever, no prompt to override.

They live in a `permissions` block in `settings.json`, each level an **array** of rule strings:

```json
{
  "permissions": {
    "deny":  ["Bash(rm *)"],
    "ask":   ["Edit(~/**)"],
    "allow": ["Read(/**)"]
  }
}
```

> 💡 **A tiny gotcha Andrew hit live:** each level must be an **array** (`[ ]`),
> even when empty. Leaving one as `{}` or a bare value throws an *"incorrect type
> for array"* error. If your settings file is complaining, check that `allow`,
> `ask`, and `deny` are all `[...]`.

### The precedence: deny → ask → allow

Here is the rule that shows up on the exam more than any other detail in this lesson. When more than one rule matches an action, they are **evaluated in the order deny → ask → allow**, and the **most restrictive** (Andrew also says "least permissive" — same thing) match wins:

```text
Does a DENY rule match?  -> BLOCK. Stop. Nothing overrides this.
Else does an ASK rule match?  -> PROMPT the user.
Else does an ALLOW rule match?  -> ALLOW silently.
Else -> fall back to the permission MODE (see Part 5).
```

As Andrew puts it: "a deny will always rule over an ask and allow, and an ask will happen before an allow happens." So if you `allow` all `git` commands but `deny` `git push`, then `git push` is blocked — deny beats allow even though both match. This is exactly the behavior you will prove in the Capstone.

> 🔑 **deny → ask → allow. The most restrictive matching rule wins, and deny can never be overridden by an allow.**

### The tools these rules cover

Rules attach to Claude Code's **tools**. Andrew's first pass names the obvious ones: **bash, read, edit, web fetch, MCP, and agents** (specifically sub-agents). But — and this is a lesson in itself — that list is *incomplete*, which is the whole point of Part 2.

## Part 2: Denying one tool is not enough (the "hidden tools" lesson)

This part is the most important practical idea in the lesson, and Andrew learned it *on camera* by being surprised. It is a perfect example of the course's core stance: **build it and verify, because the docs and your assumptions are often wrong.**

He denies **bash** and asks Claude to run `ls`. Claude replies: "I don't have access to the bash tool… I can use the **glob** tool to list files" — and lists the directory anyway. Denying bash did not stop it; Claude simply reached for a *different* tool that achieves the same thing.

Then he denies **read** and asks Claude to show a file's contents. Claude does it again. When he asks how, Claude explains: "I used the **Grep** tool, not read or bash. I searched the pattern in the file, which effectively" reads it. Grep and Glob are their **own dedicated tools**, separate from both `read` and `bash`.

Digging into the Claude Code source, Andrew finds the real, longer tool list — the one that is not obvious from the docs:

```text
Read, Write, Edit, Grep, Glob, Bash, Agent (sub-agents),
WebFetch, WebSearch, Task, NotebookEdit ...
```

"We have a tool that we're not aware of. It's not in the docs," he says. So to actually stop Claude from reading a file, he has to deny the *combination*: `Read`, `Grep`, and `Glob`, plus any `Bash` command (like `cat`) that could reach the file. Only then does Claude finally report: "I don't have the remaining tools I can use to retrieve it." As Andrew concludes: "it needs a combination of tools to achieve its goals."

> 🔑 **A capable agent routes around a single deny. To truly block a capability,
> deny every tool that can reach it — for reading a file that means `Read`,
> `Grep`, `Glob`, and file-touching `Bash` commands, not just `Read`.**

> ❌ **The trap:** writing `deny: ["Read(...)"]` and believing the file is now
> off-limits. Grep and Glob will happily read around it. Always think in terms of
> *capabilities*, then deny *all the tools* that grant that capability.

## Part 3: Rule syntax — the details the exam loves

Every rule is `ToolName(pattern)`. The pattern syntax differs by tool. Here is each one, carefully.

### Bash: the wildcard `*`, and spaces matter

The Bash tool takes one input: a shell command. So a bash rule matches against that command string, using `*` as a wildcard that stands in for "anything":

```text
Bash(npm run *)      matches: npm run build, npm run test, ...
Bash(git *)          matches: git status, git commit, git push, ...
Bash(* --version)    wildcard at the FRONT
Bash(git * origin)   wildcard in the MIDDLE
```

You can put `*` **before, after, or in the middle**. The one caveat Andrew stresses: **spaces matter.**

```text
Bash(ls *)   matches "ls la"      (space, then anything)
Bash(ls *)   does NOT match "lsof" (no space — "lsof" is one word)
```

The space in `ls *` means "the command `ls`, a space, then arguments." `lsof` has no space after `ls`, so it slips past. If you meant to catch both, you would need a different pattern. This is a classic exam trick.

### Read and Edit: the four path forms

Read and Edit rules match **file paths**, and there are exactly **four** ways to anchor a path — memorize these:

| Form | Anchor | Example | Means |
|---|---|---|---|
| `//` | Filesystem **root** | `Read(//etc/hosts)` | Absolute, from the OS root (note: *double* slash) |
| `~` | Your **home** directory | `Edit(~/.bashrc)` | The usual Linux home shortcut |
| `/` | **Project** root | `Edit(/src/**)` | The root of the current project (single slash) — *not* the OS root |
| `./` or nothing | **Relative** | `Read(./notes.txt)` | Relative to the current directory |

The one that trips people: a **single** `/` is the **project** root, while a **double** `//` is the **filesystem** root. In plain Linux a single `/` means the OS root — here it does not. As Andrew says, "that can trip some people up, but that's what it does." (`**` is the usual "any nested path" glob you can append to any of these.)

### Web fetch: `domain:` and the bare catch-all

The WebFetch tool's rule needs one thing — a **domain**:

```text
WebFetch(domain:example.com)     allow/ask/deny fetches to example.com
```

"The only thing it really needs is a domain," Andrew notes — you write `domain:` then the host. And there is a special case that generalizes to *every* tool: a **bare rule with no parentheses is a catch-all.**

```text
"deny": ["WebFetch"]     deny ALL fetches, every domain
"ask":  ["WebFetch"]     ask on ALL fetches
"allow":["WebFetch"]     allow ALL fetches
```

### MCP: `mcp__server` and `mcp__server__tool`

Tools that come from an **MCP server** (an external tool provider — see the MCP glossary term above) use a double-underscore syntax:

```text
mcp__github              match EVERYTHING from the "github" MCP server
mcp__github__*           match ALL tools on that server (explicit wildcard)
mcp__github__get_issue   match ONE specific tool on that server
```

You name the server (as it appears in Claude's directory), optionally then a tool. Andrew flags his own confusion honestly — "why wouldn't the wildcard be the same thing as the server? There's probably some distinction, I can't really tell what it is" — so do not over-think the `mcp__server` vs `mcp__server__*` difference; both effectively cover the whole server. MCP is also the **one exception** to the bare-name rule below: there is no bare `mcp` catch-all — `mcp__` alone "is not a thing," you must name a server.

### Bare-name tool rules: total coverage

Pulling the catch-all idea together: **a tool name with no parentheses gives total coverage of that tool** — no domain filter, no path pattern, no command pattern.

```text
WebFetch    all fetches, all domains
Read        all reads, all files
Edit        all edits, all files
Bash        all bash commands
```

"You're getting the picture here," Andrew says. The lone exception is MCP, which always needs a server name.

> 🔑 **Bare `ToolName` = everything that tool can do. `ToolName(pattern)` = only
> matches. MCP is special: it always needs `mcp__server`.**

## Part 4: A compact syntax reference

Screenshot this. It is the whole of Part 3 on one card.

```text
RULE SHAPE:  ToolName(pattern)     |  bare ToolName = catch-all (all uses)

BASH        Bash(git *)            * before / after / middle
            Bash(ls *)             SPACES MATTER: matches "ls la", not "lsof"

READ/EDIT   four path anchors:
            //path     -> filesystem root   (double slash)
            ~/path     -> home directory
            /path      -> PROJECT root       (single slash — not OS root!)
            ./path     -> relative (or no prefix at all)
            append ** for nested paths, e.g. Edit(/src/**)

WEBFETCH    WebFetch(domain:example.com)
            WebFetch                -> bare = all domains

MCP         mcp__server             -> whole server
            mcp__server__*          -> all tools on server
            mcp__server__tool_name  -> one tool
            (no bare "mcp" catch-all — must name a server)

PRECEDENCE  deny  >  ask  >  allow   (most restrictive match wins;
                                       deny is final)
```

## Part 5: Permission modes — the default posture

Rules decide specific tools. The **permission mode** sets the *baseline* for everything a rule does not explicitly cover. As Andrew says, "in the lieu of having permission rules, this is what it's going to do." There are five:

| Mode | Behavior | When it's safe |
|---|---|---|
| **default** | Prompts for permission on the **first use of each tool**. | Everyday work. The safe baseline. |
| **acceptEdits** | Auto-accepts **file edits** for the session (still asks for other tools). | When you trust the edits and want flow — e.g. a scoped refactor you are watching. |
| **plan** | Claude can **analyze but not modify files or run commands** — auto-denies anything not pre-approved. | Reconnaissance: "tell me how you'd do it" before it touches anything. |
| **don't-ask** (a.k.a. don't-bother-asking) | **Auto-denies all tools** unless pre-approved via allow rules. | Locked-down runs where only your explicit allow-list may act. |
| **bypassPermissions** | **Skips all permission prompts.** | Almost never. Reserved for sandboxed/throwaway environments — see the next lesson. |

Two practical facts Andrew demonstrates:

- **You can launch in a mode:** `--permission-mode plan` starts a session in plan mode.
- **`Shift+Tab` toggles between three of them** in the interactive shell — **default** (no label), **plan** ("plan mode"), and **acceptEdits** ("accept edits"). The other two — **don't-ask** and **bypassPermissions** — are *not* reachable by toggling; you set them at launch or in settings. "As soon as we toggle out, we don't have it anymore," he notes.

### A verify-it moment: plan mode "didn't stick"

True to the course's stance, Andrew tests plan mode and finds it did not behave exactly as the slide promised — "our plan didn't stick to its plan mode… if you're expecting it not to muck with stuff, just be aware of that." The lesson is not "the mode is broken," it is the recurring one: **modes and docs describe intent; verify the actual behavior in your own session before you rely on it.**

> 💡 **Two footguns Andrew hit that will save you an hour.** (1) A **stray colon**
> inside a rule string silently stopped his `ask` rule from ever firing — the
> rule was malformed, so nothing matched it. Copy the exact syntax. (2) There is
> **no caching** of tool decisions: with an `ask` rule, Claude prompts you *every
> single time*, not just once. What *looked* like caching was really the mode
> (default only prompts on the *first* use of a tool) plus that colon typo. Also
> reassuring: editing `settings.json` **takes effect immediately** — Claude
> re-reads it every time.

---

## Key takeaways

1. **Three levels, one precedence.** allow / ask / deny, evaluated **deny → ask → allow**; the most restrictive matching rule wins and deny is final.
2. **Rules are tool-based ("tabback").** Every rule targets a tool: Bash, Read, Edit, WebFetch, MCP, sub-agents — plus hidden ones like Grep, Glob, Write, WebSearch.
3. **Deny the capability, not one tool.** Claude routes around a single deny using Grep/Glob/Bash. Block *every* tool that reaches the goal.
4. **Bash wildcards care about spaces.** `Bash(ls *)` matches `ls la` but not `lsof`.
5. **Four path anchors:** `//` filesystem root, `~` home, `/` project root, `./` (or nothing) relative. Single `/` is the *project* root, not the OS root.
6. **web_fetch needs `domain:`; a bare tool name is a catch-all** for that tool. MCP uses `mcp__server[__tool]` and has no bare catch-all.
7. **Five modes** set the baseline: default, acceptEdits, plan, don't-ask, bypassPermissions. `Shift+Tab` only cycles the first three.
8. **Verify behavior yourself** — plan mode did not behave exactly as advertised, and a colon typo silently broke an ask rule.

## Common pitfalls

- ❌ **Denying `Read` and thinking a file is safe.** Grep and Glob read around it. Deny `Read`, `Grep`, `Glob`, and file-reading `Bash` commands together.
- ❌ **Forgetting spaces in bash patterns.** `Bash(ls *)` will not catch `lsof`. Write the pattern to match what you actually mean.
- ❌ **Confusing `/` with `//`.** Single slash is the *project* root; double slash is the *filesystem* root. They point at completely different places.
- ❌ **Leaving `allow`/`ask`/`deny` as a non-array.** Each must be `[...]` even when empty, or settings throws an "incorrect type for array" error.
- ❌ **A typo (like a stray colon) in a rule string.** A malformed rule silently never matches — the tool behaves as if the rule isn't there. Verify by triggering it.
- ❌ **Reaching for `bypassPermissions` for convenience.** It skips *all* prompts. Save it for sandboxed throwaway environments (next lesson).
- ❌ **Trusting a mode's description without testing.** Plan mode surprised Andrew. Confirm the real behavior in a session before you depend on it.

---

## 🛠️ Capstone Project: A permission ruleset for Atlas Support (and proof each rule fires)

> This is the main hands-on project for the lesson. You will write a real
> `settings.json` permissions block for **Atlas Support** — the multi-agent
> support system this course builds across every lesson — and then *prove* each
> rule works by triggering it and watching the outcome. Small on purpose, but it
> exercises every idea above.

### What you will build

Atlas Support runs agents over a repo. You want those agents to **read freely**, **never run destructive shell commands**, and **ask before editing anything outside their own working folder**. You will encode that as a permissions block, then run Claude Code and confirm the behavior with your own eyes.

The ruleset has three parts, each mapped to a lesson idea:

- A **deny** list for dangerous bash (Part 1 precedence + Part 3 bash wildcards).
- An **ask** list for edits outside the agent folder (Part 3 path anchors).
- An **allow** list for safe reads, safe edits, and safe commands (bare-name and pattern rules).

### Why this is the perfect practice

| Lesson idea | Where you use it in Atlas Support |
|---|---|
| deny → ask → allow precedence | `git push` is denied even though `git *` is allowed |
| Bash wildcard + spaces | `Bash(rm *)` and `Bash(sudo *)` in the deny list |
| Path anchors (`/`, `~`, `//`) | Allow edits in `/agents/**`, ask on `~/**` and `//**` |
| Hidden tools / deny the capability | Locking a secrets file needs Read + Grep + Glob denied |
| web_fetch `domain:` | Allow one docs domain, deny bare `WebFetch` for the rest |
| Permission modes | Run the whole test in `plan` first, then `default` |

### A starting ruleset (illustrative — adapt paths to your repo)

```json
{
  "permissions": {
    "deny": [
      "Bash(rm *)",
      "Bash(sudo *)",
      "Bash(git push *)",
      "Read(/secrets/**)",
      "Grep(/secrets/**)",
      "Glob(/secrets/**)"
    ],
    "ask": [
      "Edit(~/**)",
      "Edit(//**)"
    ],
    "allow": [
      "Read(/**)",
      "Edit(/agents/**)",
      "Bash(ls *)",
      "Bash(git *)",
      "WebFetch(domain:docs.anthropic.com)"
    ]
  }
}
```

Read it top to bottom: destructive bash and the secrets folder are **denied** outright; edits to home or the filesystem root trigger an **ask**; reads anywhere in the project, edits inside `/agents/`, safe listing, git, and one docs domain are **allowed**. Note two deliberate overlaps you will exploit as proofs: `git *` is allowed *and* `git push *` is denied; the secrets folder is denied for `Read`, `Grep`, *and* `Glob` together.

### Milestones (build them in order, each one works on its own)

1. **Stand up the block.** Put the JSON above in your project's `settings.local.json`, adjusting `/agents` and `/secrets` to real folders in your repo (create a throwaway `agents/` and a `secrets/api-key.txt` with junk data). Confirm Claude Code loads it with no "incorrect type for array" error. *Smallest version:* just the three empty arrays, then fill them in.
2. **Prove an allow fires (silently).** Ask Claude to read a normal project file. It should read it with no prompt — `Read(/**)` allowed it. You now have a working baseline.
3. **Prove deny beats allow.** Ask Claude to run `git status` (allowed by `Bash(git *)`), then `git push` (denied by `Bash(git push *)`). The first runs; the second is blocked. You just watched **deny → allow** precedence in action, on two rules that both match.
4. **Prove ask fires every time.** Ask Claude to edit a file in your **home** directory (e.g. `~/atlas-notes.txt`). It prompts (`Edit(~/**)`). Approve it, then ask again — it prompts **again**. Confirm there is no caching: ask is every time.
5. **Prove the capability lock — not just one tool.** Ask Claude to reveal `secrets/api-key.txt`. With only `Read(/secrets/**)` denied, watch it try `Grep` or `Glob` instead. Then add the `Grep` and `Glob` denies (already in the block above) and try again — now it reports it has no tool left to reach the file. This is the Part 2 lesson, reproduced with your own hands.
6. **Prove the edit boundary.** Ask Claude to edit `/agents/router.py` (allowed, silent) and then to edit a file *outside* the agent folder, say `/README.md` — since `/README.md` matches neither an allow nor a deny, it falls back to your **mode**; and an edit to `~/README.md` hits the **ask**. Confirm the "asks outside the folder" behavior you designed.
7. **Do the whole run in plan mode first.** Launch with `--permission-mode plan`, repeat a couple of the tests, and note what changes (it should refuse to modify or execute). Then switch to `default` (via `Shift+Tab`) and rerun. Record any surprise — remember Andrew's plan mode "didn't stick."
8. **Stretch goals.** Add `WebFetch(domain:docs.anthropic.com)` proof: allow one fetch, then try a *different* domain and confirm it is not silently allowed. Add a bare `"deny": ["WebSearch"]` and prove the catch-all form blocks all searches. Finally, move the block from `settings.local.json` up to project `settings.json` and confirm precedence with the previous lesson's scopes.

### How you will know you are done

- ✅ A `permissions` block loads cleanly with all three arrays present.
- ✅ You have **watched** each of these happen: an allowed read with no prompt; `git status` allowed but `git push` denied (deny beats allow); an edit to home prompting *every* time; the secrets file blocked only after Read + Grep + Glob are all denied; an edit inside `/agents/` allowed and one outside triggering an ask.
- ✅ You ran the suite once in `plan` mode and once in `default`, and noted any difference.
- ✅ You can explain, for any rule in your block, *why* a given action was allowed, asked, or denied — citing the deny → ask → allow order.

> 💡 **Keep yourself honest:** a rule only counts as "working" when you have
> *triggered it and seen the outcome* — not when it looks right in the JSON.
> Andrew's whole permissions video is him discovering that his rules did not do
> what he assumed. Verify every one.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice
> on one idea. Optional and independent; the Capstone already touches all of
> them, so feel free to skip straight to it.

### Exercise 1: Predict the outcome (foundational)
Given `deny: ["Bash(git push *)"]`, `allow: ["Bash(git *)"]`, decide what happens for `git status`, `git commit -m "x"`, and `git push origin main`. Then check yourself against the precedence rule.

### Exercise 2: Fix the pattern (intermediate)
A teammate writes `Bash(ls*)` and is surprised it does not match `ls -la`. Explain why (hint: spaces), and write the version that matches `ls -la` but still would not match `lsof`.

### Exercise 3: Lock a folder for real (advanced)
Write the *minimum* set of deny rules that truly prevents Claude from reading anything under `/private/`, accounting for hidden tools. List every tool you had to name and say why each was necessary.

---

## Cheat sheet

```text
PERMISSION RULES & MODES — Claude Code
--------------------------------------
LEVELS      allow (silent) · ask (prompt) · deny (block)
PRECEDENCE  deny > ask > allow   (most restrictive match wins; deny is final)
FALLBACK    no rule matches -> the permission MODE decides

RULE SHAPE  ToolName(pattern)   |   bare ToolName = catch-all (all uses)

TOOLS       Bash Read Edit WebFetch WebSearch Grep Glob Write Agent Task
            NotebookEdit  + MCP tools
            ! deny one tool != block capability — Grep/Glob read around Read

BASH        Bash(git *)   * before/after/middle
            Bash(ls *)    SPACES MATTER: "ls la" yes, "lsof" no

PATHS       //x = filesystem root   ~/x = home
            /x  = PROJECT root       ./x (or none) = relative     append **

WEBFETCH    WebFetch(domain:example.com)   |  bare WebFetch = all domains
MCP         mcp__server | mcp__server__* | mcp__server__tool  (no bare "mcp")

MODES       default ......... prompt on first use of each tool   (safe baseline)
            acceptEdits ..... auto-accept file edits this session
            plan ............ analyze only; no edits/commands
            don't-ask ....... auto-deny all unless pre-approved (allow-list only)
            bypassPermissions skip ALL prompts  (danger — sandbox only)
            Shift+Tab cycles: default <-> plan <-> acceptEdits  (other 2: launch flag)
            launch:  --permission-mode plan

GOTCHAS     arrays required ([]) · a typo (stray ':') silently breaks a rule
            ask = every time (no caching) · settings.json reloads instantly
            VERIFY behavior — plan mode didn't fully "stick"
```

## How this connects to the rest of the course

- **Earlier, Module 5 · Lesson 17 · "Settings scopes and precedence":** taught *where* permission rules live (global/project/local `settings.json`) and how those scopes stack. This lesson filled in *what goes inside* the permissions block and how a single rule is evaluated.
- **Next, Module 5 · "Sandboxing and dangerous permissions":** picks up the scariest mode from Part 5 — `bypassPermissions` (a.k.a. dangerously-skip-permissions) — and shows how a **sandbox** makes it survivable by isolating bash tools. Remember Andrew's note: a sandbox only limits *bash*; WebFetch sits outside it.
- **Later, across Atlas Support:** every agent you give tools and MCP servers will need a permissions block like the one you just wrote. When Atlas Support gains MCP tools and hardened config, the `mcp__server__tool` and deny → ask → allow patterns from this lesson are exactly what keep it safe in production.

---

*Source: reconstructed from the "Claude Certified Architect: Foundations" course by Andrew Brown (ExamPro). Code snippets and JSON blocks are illustrative reconstructions of the patterns described in the talk; adapt them to the current Claude Code version and your own repo paths.*
