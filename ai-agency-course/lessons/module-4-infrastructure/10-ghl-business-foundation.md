# Module 4 · Lesson 10: GoHighLevel & your business foundation

> **Course:** The AI Agency Blueprint, a self-paced course
> **Module 4:** Infrastructure: the systems your agency runs on
> **Speaker:** Owen Rensland, agency owner and course creator
> **Source talk:** [AI Agency Full Course (Owen Rensland)](https://www.youtube.com) · [full transcript](../../transcripts/ai-agency-full-course.txt)
> **Estimated time:** 50 to 60 minutes (read plus exercises)

---

## In one sentence

You turn "I want to start an agency" into a real, live business — a registered name, a domain protected on Cloudflare, a working email, an active Stripe account, and a CRM (GoHighLevel or an alternative) with your first client workspace created — all in your own legal name.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you stand up your entire business foundation: eight setup
> steps done, a CRM live, and one sub-account created. Everything before the
> Capstone teaches the pieces you will wire together. If you want to see the
> finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Tools like GoHighLevel come and go,
> but "a business needs an identity, a way to be found, a way to talk to
> customers, and a way to get paid" is timeless.
>
> - **[U.S. Small Business Administration — Launch your business](https://www.sba.gov/business-guide/launch-your-business)**
>   (government guide). The plainest first-principles checklist of what it
>   actually takes to legally exist as a business — name, structure,
>   registration, banking — independent of any software vendor.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **CRM (Customer Relationship Management):** software that stores your leads
  and customers and helps you talk to them — call, text, email, book them.
- **Domain:** your web address, like `youragency.com`. You rent it yearly.
- **DNS (Domain Name System):** the internet's phone book. It maps your domain
  to the servers that actually host your site and email.
- **Nameservers:** the specific DNS servers in charge of your domain. Point
  them at Cloudflare and Cloudflare becomes the traffic cop for your domain.
- **Snapshot:** a GoHighLevel template — pre-built funnels, automations, and
  pipelines you copy into a new workspace instead of building from scratch.
- **Sub-account:** one isolated workspace inside GoHighLevel. You make one per
  client (and one for your own agency).
- **Payment processor:** the service that charges cards and moves money to you.
  Stripe is the common one.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Running ads and generating leads is only half the job. As Owen puts it, *"just
ads isn't good enough… you just can't get a bunch of converted jobs and cash
from the ads without something else to convert the leads."* That "something
else" is your infrastructure: a CRM to catch and nurture leads, and a real
business identity so clients trust you and can pay you. This lesson is where you
stop being a person with an idea and become a business a client can hire.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain what an all-in-one CRM does and decide whether GoHighLevel or a
   cheaper stack fits you.
2. Import a snapshot and create your first sub-account, understanding the
   agency level vs sub-account level split.
3. Complete the eight business-foundation steps: name, domain, Cloudflare DNS,
   email, logo, company registration, banking, and Stripe.
4. Set every account up in your own legal name and know why the alternative is
   fraud.

## Prerequisites

- Lessons 1–3 (agency fundamentals and your chosen niche).
- Module 0 (accounts and tools) if you have not done it.
- A payment method for small recurring costs (domain ~$12/yr, email ~$12–20/mo,
  CRM varies). None are large; the domain and email are the main ones.

---

## Part 1: What GoHighLevel actually is

GoHighLevel (often "GHL") is an **all-in-one CRM** built for marketing agencies.
Instead of stitching together five separate tools, it bundles them:

| Feature | What it does for you |
|---|---|
| Funnels & websites | Host landing pages and a simple site |
| Calendar | Let leads book appointments with you |
| Pipelines | Track leads through stages (new → booked → closed) |
| Automations | Auto-text, email, and remind leads without you |
| SMS / email | Message leads from inside the CRM |
| AI booking | An agent that texts new leads to book them in |

Owen calls it *"the best sales and marketing platform that I've personally ever
seen"* and *"a hub for you and your clients."* He has used it for years. That
enthusiasm is real — but so is his financial interest, which is the next part.

> 🔑 **A CRM's one job is to convert leads into booked, paying customers. GHL is
> one product that does it; it is not the only one.**

## Part 2: GHL is one option — here are the others

> ⚠️ **Reality check.** In the source, Owen promotes GHL heavily through an
> **affiliate link** — he is paid a percentage when you sign up under it, and he
> offers bonuses (snapshots, calls, a course portal) as incentives. That is a
> legitimate business model, but it means the pitch is not neutral. Choose the
> tool that fits *your* budget and needs, not the one that pays the recommender.

GHL bundles everything into one monthly bill (Owen mentions a ~$97/mo plan
capped at three sub-accounts and a ~$297/mo plan for more — treat these as
illustrative; check current pricing). The bundle is convenient but not cheap,
and its funnel/site builder is weaker than dedicated tools.

> 💡 **Alternatives to GoHighLevel:**
> - **Other all-in-one CRMs:** HubSpot, Keap, Close, Vendasta.
> - **Build-your-own stack (cheaper, more flexible, you wire it together):**
>   Cal.com or Calendly (booking) + Zapier or Make (automation) + Brevo or
>   Mailchimp (email) + a form tool + Stripe (payments).
>
> The trade-off: **all-in-one** = one login, one bill, everything talks to
> itself, but you pay for the bundle and inherit its weaker parts. A **stack** =
> best tool for each job and often cheaper, but you connect the pieces and
> maintain them yourself.

The rest of this lesson uses GHL's terms because that is the source, but every
step (create a workspace, import a template, connect a calendar and domain) has
a direct equivalent in any alternative. If you pick a stack, do the same eight
foundation steps and skip only the GHL-specific clicks.

## Part 3: Agency level vs sub-account level, snapshots, and sub-accounts

Once inside GHL, there are **two levels** — this trips up every beginner:

```text
AGENCY LEVEL  (you, the agency owner)
  ├─ Sub-accounts list        ← every workspace you manage
  ├─ Snapshots (templates)
  ├─ Team & permissions       ← add yourself as "agency owner"
  └─ Company / profile settings
        │
        └── SUB-ACCOUNT LEVEL  (one per client, and one for you)
              ├─ Funnels / website
              ├─ Calendar
              ├─ Pipelines & contacts
              └─ Integrations (Google Calendar, domain, Stripe)
```

The **agency level** is your control room — it lists all sub-accounts and holds
templates and team settings. A **sub-account** is a single isolated workspace.
You make one per client so their leads never mix, plus one for your own agency.

**Importing a snapshot** copies a pre-built template (funnels, automations,
pipelines) into a new sub-account so you are not starting from a blank page. In
the source, Owen provides his own snapshot; if you do not have one, GHL has
starter templates, or you build the sub-account from scratch.

**Creating your first sub-account** (the exact clicks in GHL):

1. At the agency level, go to **Sub-Accounts → Create New → Create Sub-Account**.
2. Choose **use a snapshot** (if you have one) or start blank, then **Add
   Manually** and fill in your business details.
3. Go to **Settings → Team**, add yourself, and set your role to **Agency
   Owner** so you can access every sub-account.
4. Back on the sub-account, click **Manage Client → Switch to Sub-Account**.

> ✅ **What to do about it:** name your first sub-account after your own agency
> (e.g. "Acme Marketing"). This is your home base; client sub-accounts come later.

---

## Part 4: The eight business-foundation steps

Owen's promise: *"starting your business is not hard."* Here are the eight steps
he walks through. Numbers and vendors are examples — adapt them.

1. **Name the business.** Owen: *"Just do it in 10 minutes."* Ask an AI
   (Claude, ChatGPT, or Gemini) for names, keep it simple, and check the domain
   is free before you fall in love with it.
2. **Register the domain.** Owen uses GoDaddy (~$12/yr); Namecheap or Porkbun
   work too. One year is fine to start.
3. **Cloudflare for DNS.** Create a free Cloudflare account, **add your domain**,
   then in your registrar change the **nameservers** to the two Cloudflare gives
   you. This protects and speeds up your domain. *(Alternatives: your
   registrar's own DNS, Bunny.net, Fastly.)*
4. **Business email.** Set up Google Workspace on your domain
   (`you@youragency.com`). Owen notes you can start the ~$20/mo trial and later
   downgrade to the ~$12/mo plan. *(Alternative: Microsoft 365, or Zoho Mail
   which has a free tier.)*
5. **Logo.** Make one in Canva in five minutes. Owen is blunt: *"I don't really
   think this stuff matters to be honest"* — do not let it block you.
6. **Register the company.** Owen: *"I actually can't give you legal advice
   about this."* Neither can this course — see the Reality check below.
7. **Banking.** Owen uses Chase; Revolut is a solid online option. You need a
   **business** bank account (not your personal one) so money and taxes stay clean.
8. **Payment processing (Stripe).** Sign up and create a Stripe account. You can
   even build a **payment link** to send on sales calls. *(Alternatives: Square,
   PayPal, Braintree, Paddle.)*

> ⚠️ **Reality check — open every account in YOUR OWN legal name.** The source
> says of Stripe: *"you can always do this under someone else's name if you need
> to for now."* **Do not do this.** Opening a financial account in another
> person's name or identity is **fraud** — it can get the account frozen, the
> money seized, and expose you (and them) to criminal liability. If you are not
> old enough or not ready to register a business, wait until you are. There is no
> "for now" version of this that is safe.

> ⚠️ **Reality check — registration and tax are real steps, get them right.**
> Choosing a business structure (sole proprietor, LLC, Ltd, etc.), registering
> it, and handling sales/income tax are genuine legal and financial decisions
> that vary by country and state. Owen suggests a service like LegalZoom or
> asking an AI — an AI is fine for *understanding your options*, but for the
> actual filing, confirm with a local accountant or lawyer. **This lesson is not
> legal or tax advice.**

> 🔑 **Do the boring, correct version once: your real name, a real business
> entity, a real bank account. It is the foundation everything else sits on.**

---

## Key takeaways

1. **A CRM converts leads into paying customers.** GHL is one all-in-one option;
   HubSpot, Keap, Close, Vendasta, or a Cal.com + Zapier + Brevo + Stripe stack
   are real substitutes.
2. **The affiliate pitch is not neutral.** Owen earns a commission on GHL
   signups. Pick on fit and budget, not on who is recommending.
3. **Two levels in GHL:** agency level (control room) and sub-account level (one
   isolated workspace per client). Snapshots pre-fill a sub-account.
4. **Eight foundation steps** turn an idea into a business: name, domain,
   Cloudflare, email, logo, registration, banking, Stripe.
5. **Your own legal name, always.** Someone else's name is fraud, not a shortcut.

## Common pitfalls

- ❌ **Opening Stripe or a bank account under someone else's name.** That is
  fraud. Open everything in your own legal name.
- ❌ **Buying the $297/mo plan on day one because the pitch said so.** Start on
  the plan (or the free stack) that matches your actual client count.
- ❌ **Spending three days on a logo.** It "doesn't really matter that much" —
  ship a Canva logo in five minutes and move on.
- ❌ **Skipping Cloudflare's nameserver change.** If you do not update the
  nameservers at your registrar, Cloudflare never takes over and nothing works.
- ❌ **Treating AI as your lawyer/accountant.** Use it to understand options;
  confirm the actual company registration and tax setup with a local professional.

---

## 🛠️ Capstone Project: Your business foundation, live

> This is the main hands-on project for the lesson. When you finish, your agency
> legally and technically exists — you can be found, be trusted, and get paid.

### What you will build

A real, working business foundation: a registered name and business entity, a
domain protected on Cloudflare, a business email that sends and receives, an
active Stripe account, and a CRM (GHL or an alternative) with one sub-account
created for your own agency. Each piece maps to a lesson idea:

- CRM + sub-account → Parts 1–3
- The eight setup steps → Part 4
- Everything in your own legal name → the Reality checks

### Why this is the perfect practice

| Lesson idea | Where you use it |
|---|---|
| All-in-one vs stack | Choosing your CRM before you build |
| Agency vs sub-account level | Creating your first workspace |
| Snapshot import | Pre-filling that workspace |
| Eight foundation steps | The whole build |
| Own-legal-name rule | Stripe and banking, done correctly |

### Milestones (build them in order, each one works on its own)

1. **Choose your CRM.** Decide GHL vs an alternative and write down why in one
   sentence. If GHL, note which plan and why.
2. **Name it and grab the domain.** Use AI for names, confirm the domain is
   free, register it (~$12/yr).
3. **Protect the domain on Cloudflare.** Add the domain, change nameservers at
   your registrar, wait for the green check.
4. **Stand up business email.** Google Workspace (or alternative) on your
   domain; send yourself a test email and confirm it arrives.
5. **Register the company and open business banking.** File your entity (confirm
   specifics with a local professional) and open a business bank account in your
   own legal name.
6. **Activate Stripe.** Create the account in your own legal name and build one
   test payment link.
7. **Create your first sub-account.** In GHL, import a snapshot (or start
   blank), create the sub-account for your own agency, add yourself as agency
   owner, and connect your Google Calendar.
8. **Stretch goals.** Add a logo, connect your domain to the CRM so your site is
   live, and set your calendar's daily availability so bookings only land in
   working hours.

### How you will know you are done

- ✅ You can type your domain into a browser and it resolves (Cloudflare shows a
  green "active" check).
- ✅ You can send and receive email at `you@yourdomain.com`.
- ✅ Your Stripe account is active and a test payment link opens a real checkout.
- ✅ A business bank account and business entity exist **in your own legal name**.
- ✅ Your CRM has exactly one sub-account (your agency), and you can switch into
  it as agency owner.

> 💡 **Keep yourself honest:** if any account is in a name that is not legally
> yours, you are not done — you have a problem to undo. Redo it correctly.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice
> on one idea. Optional and independent; the Capstone already touches all of
> them, so feel free to skip straight to it.

### Exercise 1: Name sprint (foundational)
Ask an AI for 20 agency names in your niche. Check domain availability for your
top five. Pick one in under 15 minutes. Practices the "just do it" discipline.

### Exercise 2: Stack vs bundle costing (intermediate)
Price out a full year of GHL against a Cal.com + Zapier + Brevo + Stripe stack
for your situation. Write which you would choose and why. Practices Part 2.

### Exercise 3: DNS dry run (advanced)
Without changing anything live, open your registrar's DNS settings and
Cloudflare's dashboard side by side. Identify exactly where nameservers are
changed and where A records live. Practices Part 4, step 3 — the step most
beginners fumble.

---

## Cheat sheet

```text
WHAT GHL IS: all-in-one CRM = funnels + calendar + pipelines + automations
             + SMS/email + AI booking. One bill, convenient, not cheap.
ALTERNATIVES: HubSpot · Keap · Close · Vendasta
              OR stack: Cal.com/Calendly + Zapier/Make + Brevo + form + Stripe
AFFILIATE WARNING: Owen earns commission on GHL signups. Choose on fit, not pitch.

TWO LEVELS: Agency level = control room (sub-accounts, snapshots, team)
            Sub-account = one isolated workspace per client (+ one for you)
SUB-ACCOUNT: Sub-Accounts > Create New > use snapshot/blank > add as Agency Owner

THE 8 FOUNDATION STEPS:
  1 Name        - AI, 10 min, check domain first
  2 Domain      - GoDaddy/Namecheap/Porkbun, ~$12/yr
  3 Cloudflare  - add domain, CHANGE NAMESERVERS at registrar (free)
  4 Email       - Google Workspace on your domain (~$12-20/mo)
  5 Logo        - Canva, 5 min, don't overthink
  6 Register    - business entity; confirm with a real accountant/lawyer
  7 Banking     - business account (Chase/Revolut), YOUR legal name
  8 Stripe      - active account + payment link, YOUR legal name

HARD RULES:
  ✗ NEVER open Stripe/bank in someone else's name = FRAUD
  ✓ Every account in YOUR OWN legal name
  ✓ Registration + tax are real: not legal advice, confirm locally
```

## How this connects to the rest of the course

- **Earlier, Module 3 · Lessons 1–3:** you picked a niche and learned agency
  fundamentals — that is the business this lesson makes real.
- **Next, Lesson 11 "Configure your GHL command center":** you take the
  sub-account you just created and build out the funnel, calendar, pipelines,
  and automations inside it.
- **Later, Module 5 (Meta Ads) and beyond:** the leads your ads generate flow
  into this CRM, get booked on this calendar, and pay through this Stripe
  account. Everything downstream sits on the foundation you built today.

---

*Source: "AI Agency Full Course" by Owen Rensland. Prices, plans, vendors, and
click-paths are illustrative reconstructions of the patterns described in the
talk — verify current pricing and confirm company registration and tax steps
with a qualified local professional. This lesson is not legal or tax advice.*
