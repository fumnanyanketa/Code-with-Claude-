# Claude Certified Architect: Foundations — Course Outline

*Reconstructed from Andrew Brown's CCA-F prep course (ExamPro) and **re-sequenced
as a learning path**. The original course walks the exam guide, which interleaves
the five exam domains; here the material is reordered so each lesson depends only
on earlier ones. Work top to bottom.*

**North-star project — "Atlas Support":** you build **one** multi-agent system
that grows across the whole course. It starts as a single API call, becomes a
tool-using loop, then a hub-and-spoke coordinator, gains parallelism, hooks, MCP
tools, hardened permissions, session/context discipline, reliability checks, and
batch processing — and ends as a **support agent that escalates to a human**.
Every capstone adds one component to it.

**The five exam domains** (how they map to modules): D1 Agentic architecture &
orchestration → Modules 1 & 3; D2 Tool design & MCP → Module 4; D3 Claude Code
config & workflows → Module 5; D4 Prompt engineering & structured output →
Module 2; D5 Context management & reliability → Module 6.

**Exam facts:** code CCA-F · 5 domains · 60 questions · pass 720/72% (17 wrong
allowed) · 120 minutes · verbose multiple-choice.

---

## Module 0 — Pre-flight: set up your workbench *(optional on-ramp)*
*Objective: install everything and make your first call, so every later lab just runs.*

0. **Set up your architect's workbench** — self-guided
   *Skill gained:* a working toolchain (Python, the Anthropic SDK, the Claude Agent SDK, Claude Code, an API key), a hello-world call, and a reusable response-parser + logging helper you'll use in every lab.

## Module 1 — Foundations: how Claude agents actually work *(Domain 1 core)*
*Objective: the exam map plus the agentic loop, tools, and stop-reason loop everything else is built on.*

1. **What the CCA-F exam is and how to pass it** — orientation
   *Skill gained:* know the exam's shape, the five domains, the scoring, and a realistic study plan; set expectations for a hands-on, verify-everything approach.
2. **The agentic loop and Claude Code** — Domain 1
   *Skill gained:* explain the gather-context → take-action → verify loop, what Claude Code is, its surfaces, and which model (opus/sonnet/haiku) fits which job.
3. **Tools and the stop-reason loop** — Domain 1
   *Skill gained:* implement the core loop by hand — call the API, read `stop_reason`, run the tool, append the `tool_result`, and repeat until `end_turn`.
4. **Loop antipatterns and ending the loop correctly** — Domain 1
   *Skill gained:* drive control flow off `stop_reason` (never by parsing text) and cap runaway loops with a max-iteration break.

## Module 2 — Prompting and structured output *(Domain 4)*
*Objective: steer the model reliably before you orchestrate many of them.*

5. **Prompting that steers the model** — Domain 4
   *Skill gained:* use few-shot examples and goal/quality-criteria prompting (over rigid step lists), and write specific prompts that avoid vague-prompt false positives.
6. **Forcing structured output** — Domain 4
   *Skill gained:* use `tool_choice` (auto/any/tool/none) and a JSON input schema with enums and required fields to force clean, machine-readable output — and avoid the force-`tool` infinite-loop trap.

## Module 3 — Orchestration: multi-agent architectures *(Domain 1, advanced)*
*Objective: the heart of Domain 1 — turn one agent into a reliable coordinated system.*

7. **Code-driven vs model-driven decisions** — Domain 1
   *Skill gained:* choose deliberately between deterministic control (if/else, state machines) and letting the model route, and know the cost/reliability trade-offs.
8. **Hub-and-spoke: your first coordinator** — Domain 1
   *Skill gained:* build a coordinator that owns routing, context, and aggregation, with sub-agents exposed to it as tools.
9. **Task decomposition done right** — Domain 1
   *Skill gained:* decompose work into non-overlapping partitions, enforce coverage, and route dynamically to only the sub-agents a task needs.
10. **Refinement loops and observability** — Domain 1
    *Skill gained:* add an evaluation step that re-delegates gaps (with an iteration cap), and instrument the coordinator with logging and message capture.
11. **Failure recovery and a clean coordinator refactor** — Domain 1
    *Skill gained:* handle sub-agent failures with typed, structured error context, and refactor into stateless prompts/tools/lib modules with JSON logs.
12. **The Claude Agent SDK and the Agent (task) tool** — Domain 1
    *Skill gained:* port the coordinator to the Agent SDK (decorator tools, internal MCP), use the Agent tool to spawn isolated sub-agents, and read agent-definition fields (and where the Python SDK lags TypeScript).
13. **Running agents in parallel** — Domain 1
    *Skill gained:* prompt for parallel vs sequential tool calls and run several research agents simultaneously, each with its own loop and logs.
14. **Gates, hooks, and handoff protocols** — Domain 1
    *Skill gained:* enforce prerequisites with gates, run pre/post-tool hooks (roll-your-own and SDK-native), and build a structured human-handoff/escalation package.
15. **Prompt chaining vs adaptive decomposition** — Domain 1
    *Skill gained:* choose between fixed sequential pipelines and findings-driven adaptive investigation, and preserve source provenance instead of blob synthesis.

## Module 4 — Tools and MCP integration *(Domain 2)*
*Objective: the protocol Anthropic most wants you to know.*

16. **MCP: discovery, resources, and building a server** — Domain 2
    *Skill gained:* connect MCP servers and read the flat tool list, distinguish tools vs read-only **resources** vs prompts (a key exam point), and build a small custom MCP server.

## Module 5 — Claude Code configuration and workflows *(Domain 3)*
*Objective: configure, secure, and automate Claude Code like an architect.*

17. **Settings scopes and precedence** — Domain 3
    *Skill gained:* place settings at the managed/user/project/local scopes with the right precedence, and navigate the full settings surface.
18. **Permission rules and modes** — Domain 3
    *Skill gained:* write allow/ask/deny rules (with deny→ask→allow precedence) and bash/path/webfetch/MCP patterns, and use permission modes (plan, acceptEdits, etc.).
19. **Sandboxing and dangerous permissions** — Domain 3
    *Skill gained:* enable sandboxing (bubblewrap/socat), understand its limits, and reason about `--dangerously-skip-permissions` — including how an agent can escape a sandbox to finish a task.
20. **Built-in tools, status, and debug** — Domain 3
    *Skill gained:* recall the built-in tool list (and which need permission), and use `status` and `debug` to diagnose auth and problems.
21. **Automating with Claude Code GitHub Actions** — Domain 3
    *Skill gained:* wire up `@claude` in CI to turn issues into PRs with a workflow file and an API-key secret.

## Module 6 — Context management and reliability *(Domain 5)*
*Objective: keep long-running agents correct, cheap, and trustworthy.*

22. **Sessions: resume, fork, and rewind** — Domain 5
    *Skill gained:* resume and non-destructively fork sessions (and know where Python's SDK needs a TypeScript detour), and rename/rewind/restore a session.
23. **Managing the context window** — Domain 5
    *Skill gained:* read the `context` breakdown and the auto-compact buffer, and use compact/clear deliberately.
24. **Reliability I — human review, confidence, and synthesis** — Domain 5
    *Skill gained:* add field-level confidence and stratified human review, and synthesize multiple sources while preserving provenance and flagging conflicts (with peer review to avoid self-bias).
25. **Reliability II — validation retries and large context** — Domain 5
    *Skill gained:* feed schema-validation errors back for capped retries, and handle large context with external memory (findings files), tool-output filtering, and a crash-recoverable explorer.
26. **Batch processing for scale and cost** — Domain 5
    *Skill gained:* submit and poll async batches with `custom_id`s to process many items at a large cost saving.

## Module 7 — Capstone: put it all together
*Objective: combine the whole course into one production-shaped agent.*

27. **Build a support agent with progressive escalation** — Domains 1 & 5
    *Skill gained:* assemble a support agent as a state machine that resolves what it can and escalates to a human with a structured handoff — the north-star "Atlas Support," complete.
