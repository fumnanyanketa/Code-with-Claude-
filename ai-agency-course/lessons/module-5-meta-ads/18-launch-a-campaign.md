# Module 5 · Lesson 18: Launch a campaign

> **Course:** The AI Agency Blueprint, a self-paced course
> **Module 5:** Meta Ads Mastery: run paid ads that actually book appointments
> **Speaker:** Owen Rensland, founder of a local-business ad agency
> **Source talk:** [AI Agency Full Course (Owen Rensland)](https://www.youtube.com) · [full transcript](../../transcripts/ai-agency-full-course.txt)
> **Estimated time:** 55 to 70 minutes (read plus exercises)

---

## In one sentence

You will sit down in Meta Ads Manager and build a complete campaign for a real client — objective, budget, 2026-style targeting, and a batch of creatives — then run a pre-launch checklist so that when you hit "schedule," nothing is broken.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you build and schedule a real, launch-ready campaign in Ads
> Manager for your niche — funnel connected, pixel firing, creatives loaded,
> checklist 100% ticked. Everything before the Capstone teaches the exact clicks.
> If you want to see the finish line first, jump to the **"Capstone Project"**
> section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Ad platforms change their buttons
> constantly, but the structure never does: an **account** holds **campaigns**
> (the objective), which hold **ad sets** (who + how much + where), which hold
> **ads** (the creative). For the timeless version:
>
> - **[Meta's "About campaign structure"](https://www.facebook.com/business/help)**
>   (official docs). It is the tool-agnostic map of the three-layer hierarchy you
>   will build in this lesson, no matter what the UI looks like next year.

## A few plain-language basics first

This lesson uses some everyday advertising terms. Here they are in plain words:

- **Campaign:** the top folder. It holds your **objective** — the one thing you
  are asking Meta to get you (in our case, leads).
- **Ad set:** the middle folder. It controls **budget**, **audience** (age,
  gender, location), **placement**, and the **optimization event**.
- **Ad:** the actual thing people see — one image or one video plus the text.
- **Pixel / dataset:** a snippet of tracking code on your funnel that tells Meta
  "someone became a lead here." It is how Meta learns who to show your ads to.
- **Optimization event:** the action you tell Meta to chase — a "Lead" or a
  "Schedule." Meta then hunts for people likely to do that.
- **Conversion location:** where the action happens — for us, your **website**
  (the funnel you built), not a Meta instant form.
- **CPM:** cost per 1,000 times your ad is shown. Lower CPM = cheaper reach.
- **Creative:** the image or video of the ad. A **hook** is its first 1–3 seconds.

You do not need to memorise these. Each is re-explained the first time it matters.

## Why this lesson matters

You have written offers, built a funnel, made creatives, and wired up your pixel
in Lessons 14–17. This is the lesson where all of it becomes a live machine.
Owen calls it out directly: *"one ad, literally just one winning ad, can
completely change your life. All it takes is one winning ad for your clients to
pay you 3K a month for two-plus years."* But a winning ad can only prove itself
if the campaign around it is built correctly and actually launches. This lesson
is the assembly — the difference between "I have creatives" and "I have a
campaign spending money and booking appointments."

## Learning objectives

By the end of this lesson you will be able to:

1. Build a Leads campaign in Ads Manager with the correct objective, budget location, and conversion setup.
2. Apply 2026 targeting: minimal manual targeting, correct age/gender, Facebook + Instagram placements only.
3. Build a batch of individual ads with the right toggles off and the funnel + pixel wired to each.
4. Run the full pre-launch checklist and catch problems before you spend a dollar.
5. Schedule a real campaign to launch cleanly.

## Prerequisites

- **Lesson 14–15** (ad fundamentals, offer and audience) — you know your niche and awareness level.
- **Lesson 16** (creatives) — you have a small batch of hooks/creatives ready.
- **Lesson 17** (funnel + pixel) — you have a mobile-first funnel with the pixel installed and events firing.

---

## Part 1: Targeting in 2026 — "targeting is the creative"

Start here, because it changes how much work the rest of the build is. Owen is
blunt: *"targeting in 2026 — targeting is an absolute joke. Targeting is solely
based on the creative nowadays. There is really no need to target anything
yourself on Meta. The creative will do the targeting."*

What this means in practice: Meta's AI now finds your buyers by watching who
responds to your creative. You do not need long lists of interests. You set a few
guardrails and let the machine do the rest.

The only manual settings Owen keeps:

| Setting | What to do | Why |
|---|---|---|
| **Age range** | Narrow it to your buyer. B2B contractors ≈ **29–64** | Stops spend on people who can't be your buyer |
| **Gender** | Match the buyer. Contractors skew **men** | Same reason — remove obvious waste |
| **Location** | The service area (a city/region, or general US for B2B) | Don't pay to reach the wrong geography |
| **Placements** | **Facebook + Instagram only** | *"Just to keep our CPMs lower."* Fewer, better placements = cheaper reach |
| **Detailed targeting** | *Optional.* A couple of interests (e.g. "general contractor," "roofing contractor," "Facebook page admins") | Only to help Meta warm up faster — you can skip it entirely |

> 🔑 **Set guardrails, then get out of the way.** Age, gender, location, and
> Facebook+Instagram placements. That is the whole targeting job in 2026 — the
> creative does the rest.

> 💡 **Retargeting has changed.** The old split of "one cold campaign + one
> retargeting campaign" doesn't work as well anymore. Owen is honest that he
> *"honestly has not done it much"* — it's beneficial but **not required** to
> get results. Don't let it block your launch. Ship the cold campaign first.

## Part 2: The campaign level — objective and budget

Open Ads Manager and click **Create**. Two decisions live at this top level.

**Objective: Leads.** You are asking Meta for leads, so choose the **Leads**
objective. Simple.

**Budget location: ad-set budget, not campaign budget.** Meta will offer to set
your budget at the campaign level (it spreads money across ad sets automatically).
Owen recommends the opposite: *"I would actually recommend doing ad-set budget"* —
so **you** control exactly what each ad set spends. For a beginner running one ad
set, this keeps you in the driver's seat.

Name it with a simple scheme so future-you can find it — for example
`CompanyName – Niche – Date` (e.g. `HamptonDecks – Decking – 617`). *(Illustrative;
use whatever scheme you like — it doesn't affect performance.)*

## Part 3: The ad set — budget, conversion, and how many creatives

This middle layer is where most of your decisions live.

**Conversion location: Website.** Send people to the funnel you built, not a Meta
instant form. Owen: *"a website… is the highest converting and it's honestly the
best."*

**Pixel + optimization event.** Choose the **dataset (pixel)** you set up in
Lesson 17 — the *same* pixel across all your clients, so it keeps learning.
Then pick the event to optimize for:

- **$50–$100/day budget → optimize for `Lead`.**
- **More than $100/day (and doing B2B client acquisition) → optimize for `Schedule`.**

For your first client campaign at a modest budget, **Lead** is the right call.

**Daily budget.** Owen's floor is firm: *"start off the ad campaign with no less
than $50 a day."* A healthy starting range is **$50–$100/day**. *(These numbers
are illustrative — set what the client's budget and your test plan support.)*

**How many creatives does that budget buy?** This is the "ad math" that tells you
how big your batch should be. Rule of thumb: **~$10–$20 per creative per day.**

```text
Daily budget  ÷  $10–$20 per creative  =  how many hooks/creatives to load

$50/day   →  ~3–4 creatives
$80/day   →  ~4 creatives
$100/day  →  ~5–6 creatives
```

**One ad set. Keep the signal.** Do not split into five ad sets. Owen:
*"We're going to go with one ad set for now… because we're only testing out one
targeting method and we want to keep the signal here."* One ad set pools all the
learning data instead of scattering it.

**Cost-per-result goal (optional).** You can set a target cost so Meta knows
where to bid — e.g. a $150 cost-per-schedule for a B2B campaign. *(Illustrative;
you'll learn your real number by running your niche.)* Skip it if you're unsure;
it's optional.

Then set your **age**, **gender**, **location**, and switch **placements to
Facebook + Instagram only** (Part 1). Ad set done.

> ✅ **What to do about it:** one ad set, $50–100/day, website conversion, `Lead`
> event, your shared pixel, FB+IG placements. Load the number of creatives your
> budget supports and no more.

## Part 4: Building the individual ads (the batch)

Now the ad level. You will build one ad, then duplicate it for the whole batch.

For **each** ad:

1. **Page selection.** Choose the **Facebook page** and **Instagram account** the ads run from. Use a page that's warmed up (has some posts/history) — brand-new empty pages get punished with higher CPMs.
2. **Multi-advertiser ads → OFF.** Owen turns this off *"just because you're going to be around so many competitors."*
3. **Destination.** Paste the **funnel link that has your pixel on it**. This is the single most important field — get it wrong and you track nothing.
4. **Browser add-ons → OFF.**
5. **Add creative.** Press **Image** for an image ad or **Video** for a video ad, and upload **one** creative. One creative per ad — keep it simple.
6. **Copy.** Paste your **primary text**, a **headline** that mirrors the top of your funnel, and set the **call to action** to **Learn More**. (Keep a copy/creative "ad vault" so you can paste these fast.)
7. **Turn the extras OFF.** Add music, image/video enhancements, and other "touch-ups" — Owen prefers *"to turn all these off."* They can distort your creative.
8. **Tracking.** Confirm **website events** is on and the **correct pixel** is selected.

Then **duplicate** that ad once per creative in your batch, and swap in a
different creative each time. Image and video ads can live in the same ad set —
with Meta's current delivery system it *"doesn't matter that much."*

> 🔑 **One creative per ad, one destination link with the pixel, competitor and
> "enhancement" toggles off.** Duplicate to fill the batch. That's the whole ad
> level.

> 💡 **Tool note (funnel + pixel stack).** This lesson assumes a **Lovable**
> funnel and a **GoHighLevel** back end from earlier lessons. Real substitutes
> exist: funnels — Framer, Webflow, Carrd, Unbounce, Leadpages; CRM/automation —
> HubSpot, Close, or a Cal.com + Zapier/Make + Brevo stack. The Ads Manager
> steps are identical whatever your funnel is built in.

## Part 5: The pre-launch checklist

Before you schedule, walk this list. This is what separates a clean launch from
burning $80 on a broken funnel. Tick every box.

```text
PRE-LAUNCH CHECKLIST
[ ] Pixel firing — Metapixel installed on the funnel and active
[ ] Events verified — go to Events Manager → Test Events, load the funnel,
    confirm your Lead / Schedule event registers
[ ] Copy & price match — the price in the ad copy = the price on the funnel
[ ] Headline mirrors the ad — funnel headline matches the ad promise (message congruency)
[ ] Mobile-first funnel — loads fast, CTA visible without scrolling, survey smooth
[ ] No off-ramps / dead ends — no stray links or buttons that let people wander off
[ ] Minimal friction — survey/application only as long as it needs to be
[ ] Speed-to-lead ready — automations set so a new lead is contacted fast
[ ] Offer & creative tight — final, on-brand, ready
[ ] Batch of hooks/creatives ready — one media per ad, "related media" off
[ ] Budget supports the creative count — ~$10–$20 per ad
[ ] Placements = Facebook + Instagram only; age/gender set
[ ] Billing verified — card set, bank verified, so the campaign can actually spend
[ ] Mindset — committed to leaving it alone for the first 5–7 days
[ ] Schedule to launch at midnight
```

A few of these deserve a word:

- **Events verified** is the one people skip and regret. In **Events Manager →
  Test Events**, open your funnel and submit a test lead. You should see `Lead`
  (and `Schedule` if you use it) fire *once*. *"That's all that matters."*
- **Price and headline match** matters more than it looks. If the ad says
  "decks from $9.5K" and the funnel says something else, trust breaks and your
  cost-per-lead climbs. Owen fixed exactly this live: *"we just want it to be
  aligned. That's the biggest thing."*
- **Speed-to-lead** can *"improve your ad results by five to ten times."* A lead
  contacted in seconds converts far better than one contacted tomorrow.

## Part 6: Schedule it — and the "midnight" folklore

Select your campaign and ad set, edit the schedule, set the **start date to
tonight at midnight** (23:59 / 00:00), and **publish**. Done — it's scheduled.

Why midnight? Owen says *"make sure to launch it at midnight. That helps."* The
idea is that the ad set starts with a fresh, full day of budget and learning
instead of a partial one.

> ⚠️ **Reality check.** "Launch at midnight" is low-stakes folklore. It probably
> doesn't hurt, and giving Meta a clean 24-hour learning day is a reasonable
> story — but there is no strong evidence it changes outcomes, and Owen himself
> only says it *"helps."* Don't treat it as sacred, and don't let "I couldn't
> schedule for exactly midnight" stop you from launching. The real levers are
> your creative and your funnel, not the launch minute.

> ❌ **The bigger trap: over-optimizing before you have data.** The temptation
> after launch is to refresh Ads Manager ten times a day and start "fixing"
> things. Don't. Owen's whole media-buying philosophy is to **let the ads
> breathe** and make decisions from data, not feelings. You committed to
> touching nothing for 5–7 days — honor that. Tuning a campaign that has spent
> $12 is just guessing with extra steps.

---

## Key takeaways

1. **Targeting is the creative.** In 2026 you set age, gender, location, and Facebook+Instagram placements — then let Meta's AI find buyers via the creative.
2. **Ad-set budget, one ad set.** You control the spend, and one ad set keeps the learning signal pooled.
3. **Website conversion, Lead event, shared pixel.** Send traffic to your funnel; optimize for `Lead` at $50–100/day; reuse the same pixel across clients so it keeps learning.
4. **Budget sets your batch size.** ~$10–20 per creative → a $100/day campaign runs ~5–6 creatives.
5. **The checklist is the launch.** Pixel firing, events verified, copy/price match, mobile-first funnel, speed-to-lead ready — tick all of it before you schedule.
6. **Don't worship folklore or over-tune early.** Midnight is harmless superstition; refreshing every hour is harmful. Launch clean, then leave it alone for a week.

## Common pitfalls

- ❌ **Splitting into many ad sets to "test more."** It scatters your data and starves each one. One ad set keeps the signal.
- ❌ **Forgetting to verify events.** A campaign that spends but doesn't fire `Lead` is money into a void. Test in Events Manager *before* launch.
- ❌ **Ad says one price, funnel says another.** Message mismatch tanks trust and cost-per-lead. Match copy, price, and headline.
- ❌ **Leaving "enhancements," music, and multi-advertiser ads on.** They distort your creative and dump you in with competitors. Toggle them off.
- ❌ **Managing the ads emotionally.** Killing a campaign after a few dollars because it "feels" bad. Let it breathe 5–7 days, then read the data.
- ❌ **Budget too thin for the batch.** Six creatives on $50/day means none get enough spend to prove themselves. Match creative count to ~$10–20 each.

---

## 🛠️ Capstone Project: build and schedule a real campaign

> This is the main hands-on project for the lesson. You will feel the difference
> between "I have assets" and "I have a live campaign" — because by the end, a
> real campaign is scheduled to spend money for your niche.

### What you will build

A complete, launch-ready Meta campaign for your chosen niche/client, assembled
from the funnel, pixel, and creatives you already made. You do **not** have to
spend big — you have to build it correctly and schedule it. Its pieces:

- A **Leads campaign** with ad-set budget (Part 2).
- **One ad set:** website conversion, your shared pixel, `Lead` event, $50–100/day, 2026 targeting, FB+IG placements (Parts 1 & 3).
- A **batch of ads** sized to your budget, each with the funnel link + pixel and the right toggles off (Part 4).
- A **fully ticked pre-launch checklist** (Part 5).
- A **scheduled launch** (Part 6).

### Why this is the perfect practice

| Lesson idea | Where you use it in the build |
|---|---|
| Targeting is the creative | Setting age/gender/location + FB+IG placements, minimal manual targeting |
| Ad-set budget, one ad set | Choosing budget location and keeping one ad set for signal |
| Website + Lead + shared pixel | Wiring the conversion setup at the ad-set level |
| Budget → batch size | Loading the right number of creatives (~$10–20 each) |
| Ad toggles off | Turning off multi-advertiser, music, enhancements on every ad |
| Pre-launch checklist | Verifying events, price match, mobile funnel, speed-to-lead |

### Milestones (build them in order, each one works on its own)

1. **Create the campaign.** Objective = Leads, budget at the **ad-set** level, named with your scheme. It exists now.
2. **Set up the ad set.** Website conversion location, your dataset/pixel, optimize for `Lead`, daily budget $50–100.
3. **Apply 2026 targeting.** Age range, gender, location for your niche; placements = Facebook + Instagram only; detailed targeting optional.
4. **Build ad #1.** Page selected, multi-advertiser + music + enhancements off, funnel-with-pixel as destination, one creative, copy + headline + Learn More, website events on.
5. **Duplicate into the batch.** Match your creative count to your budget (~$10–20 each); one different creative per ad.
6. **Run the pre-launch checklist.** Every box in Part 5 — especially **Test Events** showing your `Lead` event fire, and price/headline congruency.
7. **Schedule and publish.** Start date tonight at (or near) midnight. Confirm it reads "scheduled."
8. **Stretch goals.** Set a cost-per-result goal; add one video and one image creative to the same ad set; write your no-touch rule for the first 5–7 days into your PROGRESS.md.

### How you will know you are done

- ✅ The campaign is built: one campaign → one ad set → a batch of ads.
- ✅ In Events Manager Test Events, submitting your funnel fires the `Lead` event once.
- ✅ Every ad's destination is the funnel link that carries the pixel.
- ✅ The pre-launch checklist is **100% ticked** — copy/price/headline match, funnel is mobile-first, speed-to-lead automation is on, billing is verified.
- ✅ The campaign shows **scheduled** with a start time.

> 💡 **Keep yourself honest:** if any checklist box isn't a genuine "yes," it's a
> "no." A campaign that launches with a broken event or a mismatched price
> doesn't fail loudly — it just quietly wastes the client's money.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice
> on one idea. Optional and independent; the Capstone already touches all of
> them, so feel free to skip straight to it.

### Exercise 1: Ad math (foundational)
For three budgets — $50, $80, $100/day — calculate how many creatives each should
run at $10–20 per creative. Write the ranges down. This is the math that sizes
every batch you'll ever build.

### Exercise 2: Test Events dry run (intermediate)
Open Events Manager → Test Events, load your funnel, and submit a test lead.
Screenshot the `Lead` event firing. If nothing fires, you just found a bug before
it cost you money — fix it and repeat.

### Exercise 3: Congruency audit (advanced)
Put your ad copy and your funnel side by side. Check: does the price match? Does
the funnel headline mirror the ad promise? Is there any off-ramp link on the
funnel? Fix every mismatch until an outsider couldn't tell they weren't written
together.

---

## Cheat sheet

```text
LAUNCH A CAMPAIGN — THE BUILD (all numbers illustrative; Meta's UI changes often)

STRUCTURE:  Account → Campaign (objective) → Ad set (who/budget/where) → Ads (creative)

CAMPAIGN
  • Objective: Leads
  • Budget location: AD-SET budget (you control the spend)

AD SET  (keep ONE — pool the signal)
  • Conversion location: Website (your funnel)
  • Pixel: your ONE shared dataset (reuse across clients)
  • Optimize for: Lead ($50–100/day)  |  Schedule (>$100/day, B2B)
  • Daily budget: $50–100  (floor = $50)
  • Targeting (2026 = "targeting is the creative"):
       age range + gender + location only
       placements = Facebook + Instagram ONLY  (lower CPMs)
       detailed targeting = optional
  • Cost-per-result goal: optional

ADS  (build one, duplicate for the batch)
  • Batch size = budget ÷ $10–20 per creative  ($100/day → ~5–6)
  • Page selected (warmed up) · Multi-advertiser OFF
  • Destination = funnel link WITH the pixel
  • One creative per ad · music/enhancements OFF · CTA = Learn More
  • Website events ON, correct pixel

PRE-LAUNCH (tick ALL):
  pixel firing · events tested · copy+price match · headline mirrors ad ·
  mobile-first funnel · no off-ramps · minimal friction · speed-to-lead on ·
  batch ready · budget fits creative count · FB+IG + age/gender · billing verified ·
  committed to no-touch 5–7 days

SCHEDULE: start tonight ~midnight → publish → confirm "scheduled"

FOLKLORE WATCH: "launch at midnight" = harmless, not sacred.
DISCIPLINE:     don't over-optimize before you have data. Let it breathe.
```

## How this connects to the rest of the course

- **Earlier, Module 5 · Lesson 17:** you built the mobile-first funnel and installed the pixel — that funnel is the destination and that pixel is the tracking every ad in this campaign points to.
- **Earlier, Module 5 · Lesson 16:** the creative batch you made is exactly what you load into the ad set here.
- **Next, Module 5 · Lesson 19 ("Scale with data"):** now that it's live, you log the metrics daily (spend, CPM, CTR, leads, cost-per-lead) and use the *more/better/new* framework to scale what works — the payoff of launching clean and leaving it alone.

---

*Source: "AI Agency Full Course" by Owen Rensland. Prices, budgets, targeting
numbers, and settings are illustrative reconstructions of the patterns described
in the talk — Meta's Ads Manager UI changes frequently, so treat exact button
names as a guide and adapt them to the current interface.*
