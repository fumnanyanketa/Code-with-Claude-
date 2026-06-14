# Code with Claude 2026 — London — Table of Contents

*A chronological walkthrough of every talk across both days, with what each one
actually covers. Order follows the conference agenda: **Day 1** (Opening Keynote →
closing) then **Day 2**. Two Day-2 talks (#14, #15) were removed from YouTube and
are not recoverable.*

Source markers: 🎙️ = transcribed from audio (Whisper, minor name garbling possible) ·
the rest are from YouTube captions.

---

## DAY 1

### 1. Opening Keynote
**Anthropic — Boris Cherny & team (Lisa, Angela, Caitlyn, "Cat")**
The state of Claude and a sweep of launches across the model layer, the Claude
platform, and Claude Code.
- Customer proof points: Spotify merging 1,000+ migration PRs/month, a 27-year-old vuln found in OpenBSD, API volume up ~17x, avg developer running Claude 20+ hrs/week.
- Model layer: 8 frontier models in 12 months (Opus 3 → Opus 4.7 → "Mythos" preview); scaffolding vs. primitives; task horizon; Claude Design.
- Platform: the "advisor strategy" (cheap executor + Opus advisor), Claude Managed Agents, multi-agent orchestration, "dreaming" self-improvement.
- New features announced: self-hosted sandboxes (Daytona, Cloudflare, Vercel, Modal) and MCP tunnels (reach internal MCP servers behind a firewall).
- Claude Code: desktop app, new agents view ("multi-clauding"), code review, mobile remote control, autofix, routines, Claude Security.

### 2. Beyond the basics with Claude Code 🎙️
**Anthropic — Daisy Holman (Claude Code team)**
Customizing the agentic harness for large-scale engineering, centered on context-window economics.
- What Claude needs to do your job: access (Slack, CI/CD, docs), knowledge (in-context vs. fine-tuning), tooling (LSP, linters, post-tool-use hooks).
- KV-cache economics: context isn't growing; put stable content first, volatile content last (changing early tokens costs ~10x).
- Which plugin primitives scale to 100,000+: MCP doesn't (use tool search), skills "kind of," hooks are zero-overhead, subagents pay a description tax.
- Async/parallel work: git worktrees, named persistent agents, Claude-to-Claude messaging, `/loop`, auto permission mode, phone remote control.

### 3. Running an AI-native engineering org
**Anthropic — Fiona Fung (Head of Eng & Product, Claude Code & Cowork)**
Leadership lessons for when coding is no longer the bottleneck.
- The bottleneck moved to verification, review, and maintenance.
- New norms: fewer design docs (discussion moves to PRs/prototypes), enjoyable TDD, "code wins" debates, Claude co-authored commits.
- Where humans stay in the loop: legal, risk/trust-boundary, product taste.
- Org design: hire creative builders + deep system experts, keep flat, dogfood relentlessly; top-down forcing functions + bottoms-up freedom.

### 4. Getting more out of the Claude Platform 🎙️
**Anthropic — Puneet Shah (Platform PM)**
Turning agent demos into cost-efficient production systems (demoed via "HeroCorp").
- Prompt caching: 90% discount on cached tokens, effective rate-limit boost, new console analytics for *why* a cache broke.
- Context engineering: tool search (lazy-load schemas), programmatic tool calling, compaction.
- Advisor strategy: Sonnet/Haiku executor + Opus 4.7 advisor for Pareto-optimal cost/intelligence.
- Demo drives cost down ~10x by stacking these techniques; Claude platform now on AWS.

### 5. The Prompting Playbook
**Anthropic — Margo van Laar (Applied AI Engineer)**
Hands-on prompt engineering for two scenarios: fixing a production prompt and building an agent from scratch.
- Debugging a telco support bot against an eval suite, fixing failure modes one at a time.
- Prompt hygiene: XML tags, removing cruft, output contracts, stop sequences.
- Core lessons: "instructions don't add capability," avoid overfitted ban-lists, state both sides of trade-offs, give the model tools instead of mental math.
- Building a scheduling agent: Sonnet vs. Opus, adaptive thinking, and a generate-evaluate-repair agentic loop.

### 6. The Capability Curve 🎙️
**Anthropic — Jeremy (Research PM, coding)**
How Claude's coding ability leapt over 12 months and how to ride the curve.
- SWE-bench Verified ~60% → 87% (Opus 4.7), roughly 3x more issues solved.
- 12-months-apart demo rebuilding Claude.ai one-shot (broken UI → working app).
- Three gains: planning before acting, error recovery (end of "doom looping"), sustained attention past 1M tokens (Bun's JS-engine→Rust rewrite).
- Practices: build trustworthy evals, shrink Frankenstein scaffolding, give the model room (adaptive thinking, high effort, auto mode).

### 7. Designing with Claude: From prompt to production 🎙️
**Anthropic — Dan Carey (PM, Anthropic Labs)**
How a 3-person team built and shipped Claude Design in ~10 weeks.
- Anthropic Labs as a "bet factory" (previously shipped Claude Code, MCP, Skills).
- Prototypes over docs: no PRD/OKRs; weekend prototype → Slack → ship; "pitch-offs."
- Tiny teams where roles dissolve; optimize every loop step with Claude (feedback clustering, dogfooding Claude Design to design itself).
- A failure (over-advanced power-user controls ripped out in a week); 62 improvements between Friday launch and Monday.

### 8. Building with Claude on Google Cloud 🎙️
**Google Cloud — Iman Nardini (Developer Advocate)**
Five-persona live demo building/securing/deploying a feedback app with Claude on Vertex.
- Claude Code against Claude models on Google Cloud via Application Default Credentials; pay-per-token, provisioned throughput, data residency.
- Five personas (PM, UI/UX, engineer, security, data) each with a CLAUDE.md role file.
- Google Cloud Skills + Developer Knowledge API (MCP server with fresh docs).
- Architecture: Cloud Run + Firestore + BigQuery + Looker, built with parallel sub-agents; security review plugin; CI/CD via Cloud Build + Cloud Deploy.

### 9. Building signals that trade themselves
**Man Group — Tashara Fernando (Head of Data & AI)**
Putting AI at the center of systematic trading research via governed skills.
- Production trading signals where AI generates the idea, fetches data, back-tests, and productionizes (humans review all output).
- The "iceberg": the signal is easy; the shared workflows beneath (data cleaning, back-testing) are the hard, must-be-consistent part.
- Skills governance: an internal marketplace where every skill is tagged, eval-tested, owned, and versioned (cautionary tale of a hardcoded expense-report skill).
- Demo: build a credit-card-data signal, back-test, scale across retail companies on distributed compute; ~750 of ~1,800 staff on Claude Code.

### 10. Picking the right model
**Anthropic — Lucas (Applied AI)**
Use a small private eval to pick the model that's cheapest per successful outcome.
- Three pillars (quality, latency, cost); a small good eval beats public benchmarks.
- Building evals: atomic tasks, LLM-as-judge + deterministic graders, reading transcripts (e.g., Claude cheating from git history).
- Thinking vs. effort dials; Haiku no-thinking 92% vs. Sonnet/Opus 100%.
- Shifting the frontier: prompt caching, markdown over JSON (66% token cut), dedup (77% fewer tokens, +9% accuracy); hands-on Tau-bench workshop.

### 11. Memory and dreaming for self-learning agents
**Anthropic — Ravi (API Knowledge team)**
New memory and "dreaming" features that let agents learn across tasks, sessions, and agents.
- File-system-based memory for managed agents (Rakuten 97% fewer first-pass errors).
- Multi-agent memory: read-only org stores + read-write granular stores, optimistic concurrency, version control/audit, standalone memory API.
- "Dreaming" (research preview): out-of-band batch process that analyzes transcripts and proposes better-organized memory (Harvey saw 6x completion-rate increase).
- Live SRE on-call demo: triage with org knowledge store + per-task stores; a dream discovers a recurring alert pattern.

### 12. What legal agents inherit from coding agents: Lessons from Legora 🎙️
**Legora — Jacob Emmerling (Staff Software Engineer)**
Building legal agents by borrowing from coding agents across three buckets.
- Parallels between coding and legal work (prior work, conventions, review culture).
- Reuse / Translate / Invent framework.
- Reuse: planning mode, dangerous-action approval. Translate: document editing as a coding-agent read/edit/verify loop over .docx XML; "linting for legal documents."
- Invent: due diligence via "Tabular Review"; demo runs redlined edits + a 100-doc due-diligence pass.

### 13. How to get to production faster with Claude Managed Agents
**Anthropic — Michael & Harrison + partner panel (Cloudflare, Daytona, Modal, Vercel)**
Overview of Claude Managed Agents plus a panel on self-hosted sandbox infrastructure.
- Model capability is no longer the bottleneck — infrastructure is.
- Core primitives: agent definition, sandboxed environments, sessions, event stream.
- Demo "Pascal" analytics agent; getting-started tooling (Claude API skill, CLI, cookbooks).
- Advanced: multi-agent orchestration, outcomes, memory, dreaming; announced self-hosted sandboxes + MCP tunnels.

### 14. Build a production-ready agent with Claude Managed Agents
**Anthropic — (Member of Technical Staff)**
Hands-on workshop building a multi-agent "Deal Desk" M&A app from a starter repo.
- The four primitives recapped (agents, environments, sessions, events).
- Live coding with Bun + Anthropic SDK; sessions API; delegating streaming to Claude Code.
- Multi-agent orchestration (coordinator spawns four analyst sub-agents), outcomes/rubrics, credential vaults, memory stores.
- Console tour: versioning, live session monitoring, observability for slow tool calls.

### 15. The thinking lever
**Anthropic — Alexander Briken (Applied AI Research)**
How Claude uses test-time compute and how to tune "effort."
- Performance scales with both model size and thinking tokens (Deep Search QA, OSWorld, HLE).
- Demo at low/high/max effort on Opus 4.7 (traffic simulation improves with effort).
- Three forms of test-time compute (thinking, tool calling, text); evolution to adaptive thinking ("not a model router").
- Effort guidance: extra-high default for Claude Code/claude.ai; low for latency-sensitive classification; prefer a bigger model at low effort over a small one at high effort.

### 16. How Lovable vibecodes production software at scale 🎙️
**Lovable**
Detecting when users are "stuck" and self-healing.
- Scale: 50M projects, 200K new apps/day, 600M monthly visits.
- The `is_stuck` metric (asking "fix it" 3x, complaining, abandoning) via a small classifier.
- Lovable Overflow: a Stack-Overflow-style corpus retrieved into the main agent.
- The `vent` tool: agent posts friction to Slack, another agent dedupes and opens PRs; ~10 fixes merged/day, stuck rate down ~5%.

### 17. Building AI-native at enterprise scale: monday.com, Doctolib, Delivery Hero 🎙️
**Panel — moderated by Anthropic (Rebecca); Ruslan (monday.com), Alex (Doctolib), Ulrich Schäfer (Delivery Hero)**
Retrofitting Claude into decade-old codebases.
- Delivery Hero "HeroGen": Jira ticket → production PR; ~173 merged PRs/day, 85% success via a "council of agents."
- Doctolib: ~100% adoption, internal skills marketplace, "Build with AI" Slack channel.
- monday.com "Monday Vibe": prompt → PRD → working app; Opus orchestrator + deterministic sub-workflows.
- Model-migration pain (4.5→4.6 broke prompts); API-first design; integrate into existing tools, not new chat UIs.

### 18. From one person to 80: Scaling a hypergrowth engineering org with Claude Code 🎙️
**Base44 — Yoav & Gabriel**
Keeping velocity while scaling from a solo founder to 80 engineers (acquired by Wix).
- Onboarding via two prompts (map ownership from commits; generate live Mermaid charts).
- Amplifying the founder's PR reviews into Claude review instructions.
- Production-traffic evals: a cheap model classifies user frustration to A/B test agent versions.
- User-simulator evals (Stagehand in CI), QA automation via Claude + browser wrapped in skills; theme: "keep it simple," encode team taste.

### 19. Build a proactive agent workflow with Claude Code
**Anthropic — Maya (Applied AI)**
Introducing "routines" — scheduled/event-triggered remote Claude Code sessions.
- The pain of running Claude Code on cron today (where it runs, hosting, triggers, visibility).
- Routines = prompt + repos + connectors + trigger, on Claude Code's managed infrastructure (`/schedule`).
- Schedule-based and event-based triggers (GitHub events, custom webhooks).
- Internal use: auto docs-update PRs; agent-on-agent review; deploy verifier, on-call investigator, PM triage.

### 20. Build AI agents using Claude in Microsoft Foundry
**Microsoft — Marlene Mungai (Sr. Developer Advocate) + Liam Hampton, Chris Snoring**
Hands-on workshop deploying Claude in Foundry and building a cupcake-shop agent.
- Foundry as a unified platform (models incl. Claude, Agent Service, tools, fine-tuning).
- 1,400+ connectors/MCP tools; enterprise security/governance via Defender, Purview, Entra ID.
- Lab: deploy Claude Sonnet 4.6, test in the playground, wire up via `.env`.
- Build with the Microsoft Agent Framework; connect to a cupcake-store MCP server; end-to-end ordering demo.

### 21. Coding is no longer the constraint: Scaling devex at Spotify 🎙️
**Spotify — Nicklaus**
Scaling developer experience for ~3,000 engineers when coding isn't the bottleneck.
- Scale: ~4,500 deploys/day, 40M-line monorepo; >99% weekly AI-tool use, PRs up 76%.
- FleetShift: 2.5M automated maintenance PRs merged (mostly auto-merged).
- "Honk" LLM migration tool on the Agent SDK (Java migration: months → 3 days); Honk V2 adds interactivity + multiplayer.
- Codebase standardization (technology radar, Backstage Soundcheck), Backstage exposed to agents as MCP/CLI; the new constraint is human decisions + review.

### 22. AI with Claude on AWS: From code to orchestration
**AWS — Antonio Rodriguez**
The AWS-Anthropic partnership and three ways to run Claude on AWS.
- Partnership: multi-billion investment, Project Rainier, 3rd-gen Trainium chips.
- Bedrock ecosystem: evaluation, prompt optimization, fine-tuning/distillation, knowledge bases, Guardrails, AgentCore.
- Three ways: Claude models via Bedrock, the new GA "Claude platform on AWS," and Claude Desktop/Code via Marketplace.
- Workshop: "Claude Code on AWS" using the Excalidraw repo (basics → context/Playwright/git → subagents/plugins/skills/hooks).

### 23. Stop babysitting your agents 🎙️
**Anthropic — Siddh Bhundasarya (Founding engineer, Claude Code)**
A "Claude Code 301" talk: three stacked techniques for unsupervised agents.
- Table stakes: a good CLAUDE.md, connected tools, a remote environment.
- Verification: teach Claude the human build/run/check/test playbook; the autonomous hill-climbing "loop."
- Front-end loop recipe: dev server + browser (Chrome MCP/Playwright) + before/after screenshots; package verification as a self-improving skill (MonkeyType demo).
- Multi-clauding (desktop app, agents view, web, phone remote control) and background loops (`/loop`, routines).

### 24. What's new in Claude Code 🎙️
**Anthropic — Ralf (Technical Staff)**
A rapid roundup of recent releases across developer experience and autonomy.
- Remote control (start on desktop, continue on mobile/web with notifications).
- Flicker-free full-screen TUI; desktop UI refresh (sessions grouped by repo, plan/diff commenting).
- Auto mode (classifier checks destructiveness + prompt injection), native git worktrees, auto memory (memory.md).
- Multi-agent code review (`/ultra-review`), routines (research preview), Agent View (`claude agents`), better Windows + GCP/AWS deployment.

---

## DAY 2

### 25. Ship your first Managed Agent
**Anthropic — Isabella He (Member of Technical Staff, Applied AI)**
Hands-on workshop building an incident-response agent on Claude Managed Agents (CMA).
- Evolution: Messages API → Agent SDK → CMA (Anthropic handles scaling, sandboxing, observability).
- The harness manages compaction, caching, and "context anxiety."
- Primitives: agents (Opus 4.7), environments ("the hands"), sessions (speak in events).
- Decoupling the agent loop from tool execution → >90% reduction in P95 time-to-first-token; new: bring-your-own-compute, MCP tunnels, memory + dreaming, vaults, webhooks.

### 26. Tool, skill, or subagent? Decomposing an agent that outgrew its prompt
**Anthropic — Will (Applied AI)**
Refactoring an overgrown inventory agent ("Stock Pilot") while hill-climbing on evals.
- Starting state: 400-line system prompt, 12 tools, evals at 83% (62% on the old version).
- Specific eval failures diagnosed (inefficient paths, orchestrator/subagent breakdown, forecasting hallucination).
- Replace prompt bulk with skills (progressive disclosure, 400 → ~15-50 lines); replace custom tools with human-like primitives (bash/read/write).
- When to use subagents (parallelization or a fresh mind); tool strategy (primitives → custom → MCP); score climbs to ~92%.

### 27. Agent Battle: Mine the most diamonds in 45 minutes
**Anthropic — Ben & Jeff (Applied AI)**
Competitive workshop configuring managed agents to mine diamonds in a Minecraft clone.
- Goals: build/deploy a managed agent; understand config impact (system prompt, model, skills, MCPs); hill-climb on evals.
- Setup: Minecraft clone + Mineflayer bot via MCP tools; same seed for all.
- Rules: 35-min build, 5-min mining run, live leaderboard, ties broken by token efficiency.
- Result: winner mined 19 diamonds; token-efficiency scoring quirks.

### 28. Evals for taste: Hill-climbing a slide-generation agent
**Anthropic**
Building eval intuition by improving a PowerPoint slide-generation agent.
- Why build your own evals vs. generic benchmarks (SWE-bench, Tau-bench, OSWorld, ARC-AGI 2).
- Four grader types: code-based, model-based (LLM-as-judge), pairwise, human.
- Concrete graders (emoji count, clutter, slide count, fonts) + judge rubrics; tighten the prompt to "avoid AI tells"; add an adversarial QA loop.
- Calibration pitfalls (inflated judge scores, saturation); ask for reasons BEFORE the score; Sonnet → Opus 4.7 markedly improves output.

### 29. Agents that remember
**Anthropic — Kevin (Engineer)**
CMA's new memory stores and "dreaming" for cross-session persistence and self-improvement.
- The base problem: sessions are isolated.
- Memory store: file-system-like, read/write via bash/grep, per user/workspace/org, versioned and human-editable.
- Dreaming: async multi-agent batch (orchestrator + a subagent per session) that fact-checks, enriches, dedupes, consolidates — non-destructively.
- Three composable layers (session → memory store → dreaming); ~95% cache-hit rate.

### 30. How we Claude Code
**Anthropic — Arno (Architect, Applied AI; based on Tariq's SF talk)**
How Anthropic uses Claude Code today.
- Sutton's "bitter lesson": don't over-constrain; let Claude interview you for the spec (ask-user-question tool).
- HTML files instead of Markdown specs ("unreasonable effectiveness of HTML"); generate multiple design directions.
- Agent-native verification (Storybook fixtures, data-attributes, schemas, invariants, probes).
- Three verification surfaces: human dashboard, browser DOM contract, headless `bun verify` in CI; record runs as video clips.

### 31. Making agentic workflows trustworthy and verifiable with a custom DSL
**Elicit — James Brady**
Why Elicit built a custom DSL ("AshPL") so its research agent's process is legible and verifiable.
- Thesis: identical outputs aren't equally trustworthy — the mechanism matters; choose rigor over speed.
- Three desiderata: legible process, fidelity across iteration, faithful execution.
- AshPL: Turing-incomplete, functional, typed subset of Python with domain primitives (papers, clinical trials).
- Architecture: event sourcing, message broker, sandbox + "curator"; content-addressed store for memoization (~95% cached); biology research-landscape demo.

### 32. Fighting financial crime with Claude Cowork 🎙️
**Qonto — Stefano Amorelli (Senior Staff Software Engineer)**
A security- and compliance-first agentic system assisting anti-financial-crime investigators.
- Opus 4.7 for long-context cross-document reasoning; Cowork as the UI for non-technical investigators.
- MCP gateway (on "Context Forge") handling OAuth/SSO, RBAC (in Terraform), append-only audit trail; downstream MCP servers on Kubernetes.
- Security: PASETO tokens, OTEL instrumentation, ClickHouse + Grafana.
- Plugin engineering by sitting with investigators; meta-skill verification; evals for tool selection/grounding/reasoning; human-in/on/out-of-the-loop progression.

### 33. Where code meets court: AI at the legal-technical frontier 🎙️
**Solve Intelligence — Olly Cobb (Founding AI Engineer)**
Patent work suits a "collaboration" model with AI, not "delegation."
- Patent background (claims, prosecution, litigation); why delegation breaks (outputs validated years later, highly entangled decisions, non-textual data).
- Collaboration model: surface judgment calls at the right time, then execute.
- Three principles: citations as first-class, translate dedicated-interface workflows into agent instructions, parallelize alignment + sequence execution.
- Demo: prior-art comparison with clickable citations, claim drafting, parallel application review.

### 34. How AirOps chases friction to build AI products with Claude 🎙️
**AirOps — Dylan (Product)**
Moving from a node-based workflow builder to agent products on the Claude Agent SDK.
- Node builder hit a "complexity ceiling"; Opus 4.5 made tool-calling reliable enough to invest in agents.
- "AirOps Next": "Quill" (content-marketer agent) + "Playbooks" (accessible skills) with connectors, triggers, Monitor.
- Friction 1: intentionality (document-based IDE, transparency, enforced human review via Inbox/Grid).
- Friction 2: consistency via harness engineering (specialized deterministic tools, brand-kit sub-agent); Parallel case study (+130% citations, live in 1 week).

### 35. How Metaview built self-improving prompts for application review 🎙️
**Metaview — Nick Mayhew (Product Engineer)**
A self-improving "ideal candidate profile" prompt that learns from recruiter decisions.
- LLMs caused an application explosion (one client: 2,740 applications in 24h); requirements constantly shift.
- Design: PII redaction → match against a self-improving ICP; "human in the center" as master, system as apprentice.
- ICP agent: user messages, a "query files" tool for unstructured resumes, an ICP-manager agent.
- Haiku for high-volume eval, Sonnet for pattern-finding; ICP as markdown prose (not weights/rules); guardrails in the architecture.

### 36. Teaching agents to learn from your team
**Warp — Petra (Head of Developer Experience)**
"Buzz," Warp's social-media response agent, taught to self-improve.
- The "80% there" gap; Buzz triages mentions (reply/like/skip), ~15 skills, near-zero code.
- Rules → principles (flexible principles cut the skill file to ~1/5 and improved output).
- Teaching the agent to learn: compare its output to ideal human output and generalize the lesson.
- Daily team feedback loop via Slack emoji reactions → Buzz opens a GitHub PR adjusting its own instructions; design the feedback loop, not the initial prompt.

### 37. Building the best agentic analytics harness: Powered by Claude, built with Claude Code 🎙️
**Omni — (CTO)**
Building "Blobby," Omni's data-analytics agent, on a semantic layer.
- Claude Code (Opus) was the adoption turning point; the team "skilled up" over the holidays.
- The semantic layer: curates data, localizes context next to field definitions (like CLAUDE.md), enforces permissions, refines via feedback.
- Metadata evolution (AI context, sample queries, field values); error recovery was the biggest early quality win; Haiku → Sonnet for longer conversations.
- "Blubotomies": fixing a "split brain" between outer agent and inner query sub-agent; pivot to writing real SQL (with CTEs) instead of a JSON query form.

---

*Removed from YouTube (no transcript possible): Day 2 #14 and #15.*
