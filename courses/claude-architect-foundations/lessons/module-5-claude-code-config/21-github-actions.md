# Module 5 · Lesson 21: Automating with Claude Code GitHub Actions

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 5:** Claude Code configuration & workflows: how to shape, secure, and automate the way Claude Code runs.
> **Speaker:** Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 45 to 60 minutes (read plus lab)

---

## In one sentence

You can put Claude Code inside your GitHub repository so that whenever you mention **`@claude`** in an issue or a pull-request comment, a GitHub Actions workflow spins up a fresh machine, runs Claude Code against your code, and lets it comment, push a branch, and open a pull request — and you get all of that with three pieces of setup: the Claude GitHub app, one workflow YAML file, and an `ANTHROPIC_API_KEY` secret.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you wire `@claude` into the **Atlas Support** repository and drive a single issue all the way to a pull request — writing an issue like a manager and watching Claude act on it like a teammate. Everything before the Capstone teaches the three moving parts and sets your expectations (spoiler: it works, and it is *slow*). If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Claude Code:** Anthropic's agentic coding tool — a command-line program that runs the agentic loop (gather context → act → verify) over your codebase. Same tool you have used in a terminal in the last few lessons; here it runs on a server instead of your laptop.
- **Repository (repo):** the folder of code that GitHub stores and version-controls for you.
- **Issue:** a GitHub "ticket" — a titled note describing a task, bug, or request. Teams use issues as their to-do list.
- **Pull request (PR):** a proposed set of code changes, bundled on their own branch, waiting to be reviewed and merged into the main code.
- **Branch:** a parallel copy of the code where changes can be made without touching the main version until you are ready to merge.
- **GitHub Actions:** GitHub's built-in automation system. You describe a job in a file; GitHub rents a fresh virtual machine and runs that job whenever a trigger (a push, a new issue, a comment) fires.
- **Workflow file:** the YAML file — kept in `.github/workflows/` in your repo — that tells GitHub Actions *when* to run and *what* to do.
- **YAML:** a plain-text format for configuration, built out of `key: value` lines and indented lists. The workflow file is written in it.
- **GitHub app:** a program you install onto a repo or organisation to grant it specific permissions (read code, write comments, and so on). The "Claude" GitHub app is what lets Claude Code act inside your repo.
- **Secret:** a value (like an API key) you store in GitHub encrypted, so a workflow can use it without the key ever appearing in your code.
- **API key:** a secret password string that identifies your Anthropic account so the API knows who to bill. Kept out of code, here stored as a GitHub secret.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

So far you have run Claude Code by sitting at a terminal and typing to it. This lesson unhooks it from your keyboard entirely. As Andrew frames it: "another way we can use Claude Code is with GitHub Actions. It allows us to trigger Claude Code based on workflows to perform tasks in our repo... actually performing work just like a developer on your team."

That changes the shape of the job. Instead of *doing* the work, you *describe* it — you write an issue, mention `@claude`, and a teammate-shaped agent picks it up. Andrew is candid about why that appeals to him: "if you move up in your career as a developer, you end up managing developers and writing issues and seeing it through that lens. That's the way I would probably like to work." There is one honest catch he repeats, and you should hear it now: it is slow. "The only downside — I like the workflow, but it's just slow, because you're not just waiting for Claude to execute, but for the GitHub action to execute, and it has to spin up that environment every time." Knowing both halves — the promise and the drag — is the point of the lesson.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain how Claude Code runs inside CI: a `@claude` mention fires a GitHub Actions workflow that runs Claude Code on a rented machine.
2. Name the three required pieces of setup — the Claude GitHub app, a workflow YAML file, and an `ANTHROPIC_API_KEY` secret — and say what each one does.
3. Install the Claude GitHub app from the Claude Code terminal with `/install-github-app`, and check that it is installed with the right permissions.
4. Read an illustrative `claude.yml` workflow: its triggers, its permissions, and the knobs you can tune (trigger phrase, model, max turns, system prompt).
5. Set realistic expectations — that CI runs are slow, and that you often have to steer the agent explicitly toward the workflow you want (branch, then PR).

## Prerequisites

- **Module 5, earlier lessons** — you are comfortable running Claude Code in a terminal and know it can use tools and be configured. The immediately prior lesson, **"Built-in tools, status, and debug,"** covered checking Claude Code's state; you will use that same "is it installed / am I logged in?" habit here.
- **A GitHub account and a repo you administer.** Installing an app onto a repo needs admin rights. Andrew notes you "must be a repo" admin to install the app.
- **An Anthropic API key with a little credit on it.** As you will see, the subscription that powers your interactive Claude Code does *not* power the GitHub Action — the Action bills the API directly. Five dollars of credit is plenty.

---

## Part 1: How Claude Code runs in CI — the `@claude` mention

Start with the mental model. Everything you have done with Claude Code until now happened on *your* machine. GitHub Actions moves it onto *GitHub's* machine. "CI" (continuous integration) just means "automation that GitHub runs for you on a fresh server when something happens in the repo."

The trigger is a mention. As Andrew reads it off the docs: "with a simple `@claude` mention in your PR or issue, Claude can analyze your code and create pull requests, implement fixes and bugs — all while following your project standards." You type `@claude` into an issue body or a comment, and that is the starting gun.

Here is the chain of events, end to end:

```text
  you open an issue (or comment) that contains "@claude ..."
            │
            ▼
  GitHub Actions sees the trigger and starts a job
            │
            ▼
  a fresh virtual machine boots  ── (this is the slow part)
            │
            ▼
  the job installs Claude Code and checks out your repo
            │
            ▼
  Claude Code runs the agentic loop against your code,
  reading the issue as its instructions
            │
            ▼
  it can: comment back on the issue, push a branch,
          open a pull request
```

Notice what Andrew observed while watching a real run: "post-run Claude — so it's actually installing Claude Code. And that's probably why you need the API token." The machine starts empty every time. It has to download and install Claude Code, then log in *using your API key* (not your subscription — there is no logged-in browser session on a rented server). That is the whole reason the API key is mandatory, and a big part of why runs are slow.

> 🔑 **Claude Code in CI is the same agent you already know, relocated to a throwaway server that GitHub boots on a trigger. `@claude` is the trigger; the workflow file and the API key are what make the server able to run it.**

### What it can actually do

Once running, it behaves like a developer working your ticket. In Andrew's live test it read the issue, checked items off, wrote comments back onto the issue, created branches, and eventually opened pull requests. The marketing line — "instant PR creations, automate code implementations, follow your coding standards, secure by default" — is real, though as Andrew wryly notes, "that description kind of undersells it" in some ways and oversells the smoothness in others. You will see the rough edges in Part 4.

## Part 2: The three pieces of setup

There are exactly three things to put in place. Miss any one and nothing happens (Andrew spent a good while discovering this — his first issue "did not trigger anything" because the setup was incomplete).

| # | Piece | What it is | Where it lives |
|---|---|---|---|
| 1 | **Claude GitHub app** | A GitHub app that grants Claude permission to read your code and write comments, branches, and PRs | Installed on the repo (or org), under **Settings → GitHub Apps** |
| 2 | **Workflow YAML** | The file telling GitHub Actions *when* to run (which triggers) and *what* to run (the Claude Code action) | `.github/workflows/claude.yml` in your repo |
| 3 | **`ANTHROPIC_API_KEY` secret** | Your Anthropic API key, stored encrypted, so the Action can log Claude Code in and pay for the run | **Settings → Secrets and variables → Actions → repository secrets** |

Two things trip people up here, so name them now:

- **The "GitHub app" is the real GitHub app, not a desktop application.** Andrew second-guessed this exact phrase: "install the GitHub app... Oh, so I think what it's saying is the actual GitHub app, not the desktop application." It is the *Claude* app you add to your repo's installed apps.
- **The API key is separate from your subscription.** Andrew expected his Claude subscription to cover the Action and was surprised: "since we already have a subscription, I would assume we wouldn't need an API key, but maybe we do." The docs settle it — "it says Anthropic API key, so that makes me think you can't use it with the subscription." You buy a little API credit (he loaded five dollars) from the Anthropic developer console, which is a different balance from your Claude subscription.

> 💡 **A recurring theme in this course:** the docs, the AI's answers, even your own assumptions are often wrong — the way to the truth is to build it and verify. Andrew *assumed* his subscription would pay for the Action. It does not. He only learned that by trying it and reading the error-shaped hints. When something surprises you here, trust the run over the assumption.

## Part 3: Installing the app and reading the workflow file

### Installing the Claude GitHub app

The easiest path runs from the Claude Code terminal itself. As Andrew puts it: "the easiest way to set this up is through Claude Code and just the terminal — open Claude, run install GitHub app." That is the slash command **`/install-github-app`**. It checks the GitHub CLI, confirms your account, and walks you through installing the app and granting permissions.

A sanity check while you are there: go to your repo's **Settings → GitHub Apps** and confirm the Claude app is listed. Andrew found his was already installed from an earlier step — "is it installed? It already is installed" — which is common if you created the repo through Claude. The permissions the app needs are read-and-write access to **code**, **actions**, **metadata**, **issues**, and **discussions**. If you granted the app blanket access to the repo, you already have these; Andrew confirmed his by hunting for the word "permissions": "read and write code, discussions, issues — so yes, it has that access. There should be nothing preventing it from being able to respond."

> ✅ **What to do about it:** run `/install-github-app`, then eyeball **Settings → GitHub Apps** and confirm the app is present with read/write on code, actions, issues. If it is, you can skip most of the manual dance Andrew went through.

### The workflow file, part by part

The workflow lives at `.github/workflows/claude.yml`. (The folder name is fixed — Andrew's own reminder: "GitHub workflows... `.github/workflows`." The `.yml` vs `.yaml` extension does not matter.) Here is an illustrative reconstruction of what such a file contains. Do not memorise it — read it for the shape.

```yaml
# .github/workflows/claude.yml — ILLUSTRATIVE reconstruction
name: Claude

# WHEN to run: the triggers. This is the part Andrew says you can "adjust
# however you want" — comment on an issue, comment on a PR, a new issue,
# an assignment, a review submitted.
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
  issues:
    types: [opened, assigned]
  pull_request_review:
    types: [submitted]

jobs:
  claude:
    runs-on: ubuntu-latest      # the throwaway machine GitHub boots for you

    # WHAT it may touch. These mirror the app permissions from Part 2.
    permissions:
      contents: write           # read code and push branches
      issues: write             # comment on issues
      pull-requests: write      # open and comment on PRs
      actions: read
      id-token: write

    steps:
      - uses: actions/checkout@v4      # put your repo onto the machine

      - name: Run Claude Code
        uses: anthropics/claude-code-action@v1
        with:
          # the SECRET from Part 2 — this is what pays for and authenticates the run
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}

          # --- optional knobs Andrew points out you can tune ---
          # trigger_phrase: "@claude"     # defaults to @claude; you can rename the bot
          # model: "claude-sonnet-4-5"    # pick the model instead of the default
          # max_turns: "15"               # cap how many loop steps it may take
          # system_prompt: "Follow our branching strategy: branch, then open a PR."
```

Walk the three regions:

- **`on:` — the triggers.** These decide what wakes Claude up. Andrew: "you can tell it where to trigger — when you create a new comment, or a comment on a pull request, or open a new issue, or assign it, or submit it." His practical discovery: an issue *comment* is the most reliable trigger. His first plain issue did nothing until he commented on it — "does it also trigger on issue comment? Yes, yes, yes." Keep `issue_comment` in your triggers.
- **`permissions:` — what it may touch.** Same list as the app permissions, expressed for the Action. Without `contents: write` it cannot push a branch; without `pull-requests: write` it cannot open a PR.
- **`with: anthropic_api_key:` — the key.** `${{ secrets.ANTHROPIC_API_KEY }}` pulls in the secret you stored in Part 2. This is the line that connects the file to your Anthropic credit.

Andrew flags the tuning knobs after seeing a live run pick Sonnet on its own: "I would imagine if we needed to adjust it, we could go into that GitHub Actions file and say hey, use this model. Yeah, we can right here — how many turns, what kind of model, additional system prompt, things we can tweak." Those are the commented lines above. The **`system_prompt`** knob is your best lever for the workflow problems you are about to meet.

> 🔑 **The workflow file answers two questions: *when* does Claude wake up (`on:`) and *what is it allowed to do* (`permissions:`), plus it hands Claude the API key. Everything else — model, turns, system prompt — is optional tuning.**

## Part 4: Setting expectations — slow, and it needs steering

This is the part most tutorials skip, and Andrew's whole live run is a lesson in it. Two truths.

**First: it is slow.** Every trigger boots a fresh machine and reinstalls Claude Code before any work starts. Andrew, mid-run: "the annoying part is that it probably will have to trigger every time... and that's a little bit slow. You don't want to wait like three minutes every time you reply to it." His verdict is worth quoting in full: "if it was faster, this would probably be my preferred method of working... but it's too slow, so I would not drive it that way in reality. It is cool to see, and if you're on the management side, at least use it to review things or assist you."

**Second: it needs steering.** In Andrew's run, Claude did the *implementation* readily but did not follow the workflow he wanted without being told. It wrote changes and commented, but "it didn't make a pull request." He had to ask again — "where's the pull request? Can you make one, please?" — and even then hit friction: there was no `main` branch to target (he had to create one), and Claude noted it could not auto-link a branch to an issue ("GitHub doesn't have automatic association with existing branches; you can link them from the issue sidebar"). The fix for all of this is to be explicit up front, in the issue and in the `system_prompt`: tell it to branch, implement, then open a PR into `main`.

Andrew's closing takeaways from the mess are genuinely useful design advice:

- **Break work into small files.** "You'd have to break up your code into a lot of small files, otherwise it's going to be really hard to tell what's going on" — big files make the diffs and merge conflicts unreadable.
- **Force a specific workflow.** "If we were spending more time with this, I'd spend more time trying to force it through a very specific workflow" — pin down branch → implement → PR so results land where you expect.
- **Use human-readable names.** He fought machine-generated branch and issue names: "can I make more human-readable names?" Yes — say so in the issue.

> ❌ **The trap:** expecting `@claude` to read your mind and produce a clean, correctly-targeted PR from a vague issue on the first try. It often will not. Andrew's run proves that a bare "implement this" gets you an implementation but not the *workflow* around it. State the branch-and-PR steps explicitly.

---

## Key takeaways

1. **`@claude` in an issue or PR comment is the trigger.** It fires a GitHub Actions workflow that runs Claude Code on a rented server against your repo.
2. **Three pieces, all required.** The Claude GitHub app (permissions), the `claude.yml` workflow file (triggers + what to run), and the `ANTHROPIC_API_KEY` secret (auth + billing). Miss one and nothing happens.
3. **The API key is separate from your subscription.** The Action bills the API directly; buy a little API credit and store it as a repo secret. Your Claude subscription does not cover it.
4. **Install via `/install-github-app` from the Claude Code terminal,** then confirm it under Settings → GitHub Apps with read/write on code, actions, and issues.
5. **It is slow, and it needs steering.** Every run reinstalls Claude Code on a fresh machine (minutes). Be explicit in the issue and the `system_prompt` about branching and opening a PR, or you get an implementation without the workflow around it.

## Common pitfalls

- ❌ **Assuming your subscription pays for it.** It does not. Load API credit and add the `ANTHROPIC_API_KEY` secret, or the Action fails to authenticate. (Andrew learned this the hard way.)
- ❌ **Only putting `@claude` in the issue title or body and expecting instant action.** Andrew's first issue triggered nothing; the reliable path was to *comment* `@claude` on the issue. Keep `issue_comment` in your triggers and mention it in a comment.
- ❌ **No `main` (or target) branch to merge into.** Claude created branches but had nowhere to open the PR against until Andrew made a `main` branch and set it as default. Have a default branch first.
- ❌ **Vague issues.** "Implement this" gets you code but not a branch-then-PR workflow. Spell out the steps: branch, implement, open a PR into `main`.
- ❌ **One giant file.** Big changes become unreadable diffs and painful merge conflicts. Break the code into small files so you can actually review what Claude did.
- ❌ **Expecting speed.** Each trigger reboots and reinstalls. Do not use it for rapid back-and-forth; use it for "write the ticket, walk away, review later."

---

## 🛠️ Capstone Project: give Atlas Support a `@claude` teammate

> This is the main hands-on project for the lesson. You will wire `@claude` into the **Atlas Support** repository and drive one issue from "ticket" to "pull request." Keep it small — one page, one PR. The goal is to feel the manager's workflow end to end and to feel, first-hand, both the promise and the slowness Andrew warns about.

### What you will build

A working GitHub Actions integration on the Atlas Support repo — the same north-star project you have been growing all course — so that a teammate (you) can file an issue, mention `@claude`, and have Claude open a pull request implementing it. Its pieces map straight onto the lesson:

- the **Claude GitHub app** installed on the repo (Part 2, Part 3);
- a **`.github/workflows/claude.yml`** file with sensible triggers and permissions (Part 3);
- an **`ANTHROPIC_API_KEY` repository secret** funded with a little API credit (Part 2);
- one **issue → PR** round trip you drive by commenting `@claude` (Part 1, Part 4).

You are not building new Atlas Support *features* here — you are installing the automation rail future features could be requested on. Think of it as giving Atlas Support a project-management surface: issues in, pull requests out.

### Why this is the perfect practice

| Lesson idea | Where you use it in the Capstone |
|---|---|
| `@claude` is the trigger | You comment `@claude` on an issue to start a run |
| Three pieces of setup | Install the app, add `claude.yml`, add the secret |
| API key ≠ subscription | Fund a small API balance and store it as a repo secret |
| Workflow triggers & permissions | Your `on:` and `permissions:` blocks in `claude.yml` |
| It is slow, and needs steering | You wait through the run and explicitly ask for a branch + PR |

### Milestones (build them in order, each one works on its own)

1. **Confirm the app.** From the Atlas Support repo checkout, run `/install-github-app` in Claude Code (or open **Settings → GitHub Apps**). Success = the Claude app is listed with read/write on code, actions, and issues. This milestone stands alone: even with nothing else done, you have granted Claude access to the repo.
2. **Fund and store the key.** In the Anthropic developer console, load a few dollars of credit and create an API key named for this repo. Add it under **Settings → Secrets and variables → Actions** as a repository secret called `ANTHROPIC_API_KEY`. Success = the secret appears in the list (its value is hidden). On its own, this is a reusable, funded key any workflow can now reference.
3. **Add the workflow file.** Create `.github/workflows/claude.yml` from the illustrative file in Part 3. Keep `issue_comment` among the triggers, keep `contents/issues/pull-requests: write` in permissions, and reference `${{ secrets.ANTHROPIC_API_KEY }}`. Commit it. Success = the file is on your default branch and shows up under the repo's **Actions** tab as a known workflow.
4. **Make sure there is a target branch.** Confirm the repo has a `main` (or your chosen default) branch and that it is set as default. Success = you can see `main` in the branch dropdown. (Andrew hit exactly this gap; do not skip it.)
5. **File the issue and mention `@claude`.** Open an issue titled something concrete — "Add an individual product page" or, in Atlas spirit, "Add a `/status` help page for support agents." In a **comment**, write: *"`@claude` please implement this: create the page, put it on a new branch, then open a pull request into `main`."* Success = the Actions tab shows a run kicking off. (Expect to wait a few minutes — this is the slow part.)
6. **Drive it to a PR and review.** Watch the run. If Claude implements but does not open a PR, comment again asking explicitly for the pull request into `main`. When the PR appears, open it, read the diff, and merge it. Success = a merged PR whose changes came from your issue.
7. **Stretch goals.** Add a `system_prompt:` to `claude.yml` that states your branch-then-PR workflow, so you do not have to ask twice. Pin a `model:` and a `max_turns:` cap. Rename the trigger phrase from `@claude` to your own bot name. Try assigning the issue to trigger a run instead of commenting, and note which trigger feels more reliable.

### How you will know you are done

- ✅ Your repo has all three pieces: the app installed, `.github/workflows/claude.yml` committed, and an `ANTHROPIC_API_KEY` secret present.
- ✅ Commenting `@claude` on an issue starts a run you can watch in the **Actions** tab.
- ✅ That run produced a pull request that you reviewed and merged, and the merged code matches what the issue asked for.
- ✅ You can state, from experience, roughly how long a cold run takes and one thing you had to say explicitly to get the branch-and-PR workflow you wanted.

> 💡 **Keep yourself honest:** Andrew's method is to *verify by doing*, not by trusting the marketing. Do not declare victory when the run "succeeds" — open the actual PR, read the actual diff, and merge it. A green check does not mean the page works; the file on `main` is the proof.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Read the triggers (foundational)
Open your `claude.yml` and, without running anything, list every event that will wake Claude up. For each, write one sentence describing the human action that fires it (e.g. "someone comments on an issue"). Then remove one trigger you do not want and explain what you gave up. This builds the habit of reading `on:` as "who can start a run."

### Exercise 2: Steer with a system prompt (intermediate)
Add a `system_prompt:` to the workflow that spells out your workflow: "Always create a feature branch, implement there, and open a pull request into `main` with a human-readable title." File a fresh issue that only says *"`@claude` implement a simple About page."* Confirm Claude now branches and opens a PR *without* you asking a second time. Compare against the Capstone run where you had to ask twice.

### Exercise 3: Measure and tune the slowness (advanced)
Trigger a run and note the wall-clock time from comment to PR. Then add `max_turns:` and pin a faster `model:` (e.g. a current Sonnet) in the workflow, trigger the same kind of issue again, and compare. Write two sentences on what changed and whether the trade-off (speed vs. thoroughness) is worth it for your use case — echoing Andrew's core complaint that the whole method lives or dies on speed.

---

## Cheat sheet

```text
CLAUDE CODE IN GITHUB ACTIONS — mention @claude, it acts in your repo.

HOW IT WORKS:
  @claude in an issue/PR comment  ->  GitHub Actions boots a fresh VM
  -> installs Claude Code, checks out repo  -> runs the agentic loop
  -> can comment, push a branch, open a PR.
  (The fresh-VM install is why it's SLOW and why the API key is required.)

THE THREE PIECES (miss one = nothing happens):
  1. Claude GitHub app     Settings -> GitHub Apps
                           needs read/write: code, actions, metadata, issues, discussions
  2. Workflow YAML         .github/workflows/claude.yml
                           on: (triggers)  +  permissions:  +  anthropic_api_key
  3. ANTHROPIC_API_KEY     Settings -> Secrets and variables -> Actions -> repo secrets
                           SEPARATE from your subscription — fund API credit ($5 is plenty)

INSTALL:  open Claude Code in the repo, run  /install-github-app   (must be repo admin)

WORKFLOW KNOBS you can tune in claude.yml:
  trigger_phrase   default "@claude" (rename your bot)
  model            e.g. claude-sonnet-4-5
  max_turns        cap loop steps
  system_prompt    STATE your workflow: "branch, implement, open a PR into main"

EXPECTATIONS (Andrew's hard-won notes):
  - SLOW: minutes per run; not for rapid back-and-forth.
  - Comment @claude on the issue — a bare issue body may not trigger.
  - Have a default (main) branch to target, or there's nowhere to open the PR.
  - Vague issue -> code but no PR. Ask explicitly, or bake it into system_prompt.
  - Small files + human-readable names -> reviewable diffs, fewer merge nightmares.
  - Verify by opening the PR and reading the diff — green check != working page.
```

## How this connects to the rest of the course

- **Earlier, Module 5 · Lesson 20 ("Built-in tools, status, and debug"):** you learned to check Claude Code's state — is it installed, am I logged in. You lean on exactly that instinct here: Andrew's CI troubleshooting was, at heart, "is Claude installed on this machine, and is it authenticated?" — just answered on a rented server via the API key instead of a login.
- **Earlier, the whole of Module 5:** configuration and permissions gave Claude Code its guardrails; the `permissions:` block and `system_prompt:` in the workflow are those same guardrails expressed for CI.
- **Next, Module 6 · Lesson 22 ("Sessions: resume, fork, and rewind"):** you return to running Claude Code interactively, where you *can* have the fast back-and-forth that GitHub Actions is too slow for — resuming and branching a conversation non-destructively. The contrast is deliberate: Actions is for "write the ticket, walk away"; sessions are for "stay in the loop and steer."
- **Later, across Atlas Support:** the issue-to-PR rail you built is how a team could *request* new Atlas Support behaviour — escalation rules, new tools, hardened config — as tickets, letting the agent draft the change and you review it. It is the management-shaped complement to the hands-on building you do everywhere else.

---

*Source: reconstructed from the CCA-F course by Andrew Brown (ExamPro). The workflow YAML and commands are illustrative reconstructions of the patterns described in the course — action names, versions, and inputs change, so adapt them to the current `anthropics/claude-code-action` and GitHub Actions syntax.*
