# Module 0 · Lesson 0: Set up your accounts & tools

> **Course:** The AI Agency Blueprint, a self-paced course
> **Module 0:** Pre-flight: get your tools ready so Lesson 1 is spent learning, not fighting setup
> **Speaker:** Self-guided (no talk — this is a hands-on setup on-ramp)
> **Source talk:** AI Agency Full Course (Owen Rensland) · [full transcript](../../transcripts/ai-agency-full-course.txt)
> **Estimated time:** 60 to 90 minutes (mostly clicking "Sign up")

---

## In one sentence

Before you learn how to run a marketing agency, you spend one focused session creating the eight or nine accounts the whole course runs on — a business name, a domain, DNS, email, a payment processor, a CRM, a Meta page, and an AI assistant — and log in to each one so it is real and waiting for you.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone: the "Setup complete" checklist**, where you confirm every account is created and you can log in to it. Everything before the Capstone tells you what each tool is *for* and what it *costs* so you are not signing up blind. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## A few plain-language basics first

This lesson uses some everyday tech terms. Here they are in plain words:

- **Domain:** the address of your website, like `yourbusiness.com`. You *rent* it (usually per year) from a company called a **registrar**.
- **Registrar:** the shop where you buy a domain (GoDaddy, Namecheap, Porkbun, Cloudflare).
- **DNS (Domain Name System):** the internet's phone book. It turns your domain name into the actual server your site lives on. You rarely touch it, but a couple of settings here make your site faster and safer.
- **CRM (Customer Relationship Management):** software that holds your leads, appointments, calendar, and follow-up messages in one place. In this course that tool is **GoHighLevel**.
- **Sub-account:** inside a CRM, a separate workspace. You get one for your own agency and one per client, so their data stays apart.
- **Payment processor:** the service that takes card payments and moves the money to your bank (Stripe, Square, PayPal).
- **Meta Business / Facebook page:** the business profile you need before you can run Facebook or Instagram ads.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Most business courses quietly assume you already have a domain, a business email, a payment link, and a CRM. You probably don't — and that is fine. As Owen puts it while walking through these exact steps: *"believe it or not, like starting your business is not hard. So, like that's why this part is so short."* — Owen. The goal here is simple: get the plumbing in place *once*, so that when Lesson 1 explains what this business actually is, you already have the tools open in front of you instead of scrambling.

## Learning objectives

By the end of this lesson you will be able to:

1. Name a business and register a matching domain.
2. Point that domain through Cloudflare (or your registrar's DNS) so it is protected and fast.
3. Create a business email on Google Workspace.
4. Open a payment processor (Stripe) and a business bank account **in your own legal name**.
5. Start a GoHighLevel trial and create one sub-account for your own agency.
6. Create a Meta Business account and a Facebook page for running ads.
7. Pick an AI assistant (Claude or ChatGPT) and copy the course's spreadsheet trackers.

## Prerequisites

- **None.** A computer, an internet connection, and an email address you can access.
- A payment card for the few paid steps (a domain is about $12/year; most other tools have free tiers or trials).

---

## Part 1: Name the business and grab the domain

Owen's advice is refreshingly blunt: don't agonise. *"Just do it in 10 minutes, okay? You can use AI to come up with a name or whatever."* — Owen.

1. Open your AI assistant (see Part 8) and ask for 20 short, simple business-name ideas for a local-marketing agency.
2. Pick one you can live with. Keep it simple and easy to spell.
3. Go to a registrar and check if the matching `.com` is free. Owen uses **GoDaddy**; the price he shows is about **$12 for one year**. Buy it for a single year to start — *"we can make sure we get it only for one year protection wise because it doesn't matter."*

> 💡 **Registrar alternatives.** GoDaddy works, but **Namecheap**, **Porkbun**, and **Cloudflare Registrar** are usually cheaper and have fewer upsells. Any of them is fine — you just need to own one domain.

> 🔑 **You are not marrying this name.** A domain is $12. If you rebrand later, you buy another one. Don't let "the perfect name" stall you for a week.

A logo is optional and, in Owen's words, *"doesn't really matter that much to be honest."* If you want one, make it in 5 minutes in Canva. Then move on.

## Part 2: Protect the domain with Cloudflare (DNS)

Next, route your domain through **Cloudflare**. Owen's reason: *"the reason why we do this is to protect the domain"* — and it also speeds your site up, which matters later for ads.

1. Go to `cloudflare.com`, create a free account.
2. Choose **Add a domain**, type the domain you just bought, and pick the **free plan**.
3. Cloudflare gives you two **name servers**. Copy them.
4. Back in your registrar (e.g. GoDaddy → your domain → **DNS / Name servers**), choose "I'll use my own" and paste Cloudflare's two name servers. Save.
5. Wait a few minutes and refresh. A green check means it's connected and *"protected and good to go."*

> 💡 **Cloudflare alternatives.** You don't strictly need Cloudflare on day one. Your registrar's own DNS (Namecheap, Porkbun) works, and **Bunny.net** or **Fastly** are other content-delivery / speed options. Cloudflare's free tier is just the easiest freebie.

> 💡 **Later gotcha (write it down):** when you connect this domain to GoHighLevel, it may complain about conflicting **"A records."** The fix is in Cloudflare → your domain → **DNS records** → delete the stray A records, then reconnect. You'll hit this in a later lesson; no action needed now.

## Part 3: Business email with Google Workspace

Now make a real business email like `you@yourbusiness.com` instead of a personal Gmail.

1. Search **Google Workspace**, click **Get started**.
2. Enter your business name, then choose **"use an existing domain"** and enter the domain you now control.
3. Set your email address (`you@yourbusiness.com`) and a password.
4. Verify the domain — because it's on Cloudflare, Google can often do this by having you **sign in to Cloudflare** and authorising it automatically.

Cost: Owen notes you can *"start a trial for the $20 a month plan and then also downgrade it to the $12 a month plan."* There's usually a **14-day free trial** to begin. This email also gives you a **Google Calendar**, which the CRM will use to avoid double-booking appointments.

> 💡 **Email alternatives.** Google Workspace is the smoothest, but **Zoho Mail** and **Microsoft 365** also give custom-domain email, and some registrars sell cheap mailboxes. Any professional address at your own domain is the goal.

## Part 4: Banking and payments — in YOUR name only

You need somewhere for money to land (a bank) and something to charge cards (a processor).

- **Bank:** Owen uses **Chase**; he mentions **Revolut** as a solid online option. Open a business or personal account you control.
- **Processor:** open a **Stripe** account. It's *"super simple."* You can create it without full legal business paperwork — you just *"won't be able to take the money out of Stripe without a business bank account."* Later you can register the business (via a service like LegalZoom, or just ask your AI to explain the steps for your country).

Once Stripe is live, make a test **payment link** (Stripe → **Payment links** → create a product, name it, set a price). This is the link you'll one day send a client on a call to get paid.

> ⚠️ **Reality check — open every account in your own legal name.** The source suggests you *"can always do this under someone else's name if you need to for now."* Do not. Opening a Stripe or bank account using another person's name or identity is **fraud**, it will get the account frozen, and it can expose you to criminal liability. Use **your** legal name and information, every time. This is the one non-negotiable rule of this whole lesson.

> 💡 **Processor alternatives.** Stripe is the default, but **Square**, **PayPal**, **Braintree**, **Paddle**, and **GoCardless** all process payments. Pick whichever is available and reputable in your country.

## Part 5: GoHighLevel trial + one sub-account

**GoHighLevel (GHL)** is the course's all-in-one hub: CRM, calendar, funnels, and automations in one place. Owen calls it *"the best sales and marketing platform that I've personally ever seen."* Note that he has a paid affiliate relationship with them — so weigh the recommendation with that in mind.

To set it up:

1. Start a GoHighLevel trial (Owen's affiliate link offers an extended 30-day trial; a standard trial works too).
2. Log in and, if you were given the course **snapshot** (a ready-made template of funnels and automations), import it.
3. Understand the two levels: the **agency level** (settings across everything) and the **sub-account** (one workspace). Go to **Sub-accounts → Create new** and make one sub-account for **your own agency**.
4. Under agency **Settings → Team**, add yourself and set your role to **Agency owner** so you can access every sub-account.

Pricing (as Owen describes it): the **$97/month** plan allows **3 sub-accounts** (your agency + 2 clients); the **$297/month** plan removes that limit. Start on the trial — you don't pay until you have paying clients.

> 💡 **GoHighLevel alternatives.** GHL bundles a lot, but you are not locked in. All-in-one substitutes: **HubSpot**, **Keap**, **Close**, **Vendasta**. Or assemble a cheaper, more flexible stack yourself: **Cal.com / Calendly** (booking) + **Zapier / Make** (automation) + **Brevo / Mailchimp** (email) + a form tool + **Stripe** (payments). The trade-off: a stack costs less and bends more, but you wire it together yourself.

## Part 6: Meta Business account + a Facebook page

To run Facebook or Instagram ads later, you need a **Facebook page** (a business profile, *not* your personal account).

1. From your personal Facebook account, go to `facebook.com/pages` and **create a new page**.
2. Name it. Owen sometimes uses his **own name** as the page (contractors *"trust a one-man band"* in his niche) and sometimes a brand name — pick what fits.
3. Add a logo and cover image. Then **stop** — don't rush to create an ad account or business portfolio the same minute, because *"they'll get restricted if you make things too quickly."*

That's all you need today: the page exists and is under your control.

> ❌ **Don't buy fake followers or "warm up" with cheap-geo likes.** The source suggests running a $5/day engagement campaign targeting places like Colombia or Pakistan to rack up page likes fast. Buying likes from unrelated regions is **vanity that violates Meta's terms**, pollutes your audience data, and can get the page flagged. Grow the page with real content and real local engagement instead.

## Part 7: An AI assistant

You'll use an AI assistant constantly — for naming, market research, ad analysis, and drafting copy. Owen leans on **Claude** throughout the course (*"you can ask Claude and figure it out"*).

1. Create a free account at **Claude** (`claude.ai`) or **ChatGPT** (`chat.openai.com`).
2. Send it one test prompt (e.g. "List 10 name ideas for a local home-improvement marketing agency"). If it answers, you're done.

> 💡 **AI alternatives.** Claude, ChatGPT, and **Gemini** are largely interchangeable for this course. Pick one; you can always try another. A free tier is enough to start.

## Part 8: Copy the course trackers

Finally, make your own copy of the course's **spreadsheet trackers** (the KPI, lead, and client trackers referenced throughout). Owen's whole philosophy is running the business on real numbers — *"buyers on your calendar and not leads in a spreadsheet"* is the goal, but you track everything in a spreadsheet to get there.

1. Open the shared trackers link from the course resources.
2. **File → Make a copy** (Google Sheets) into your own Drive, so you can edit freely.
3. Rename it with your business name.

> 💡 **Spreadsheet alternatives.** Google Sheets is easiest to copy and share; **Excel** or **Airtable** work just as well if you prefer them.

---

## Key takeaways

1. **Setup is short on purpose.** Nine accounts, one focused session. Don't let any single step stall you — most are free or a few dollars.
2. **Own everything in your own legal name.** Bank, Stripe, domain — no exceptions. Anything else is fraud and gets frozen.
3. **You're never locked in.** Every paid tool named here has real, cheaper substitutes. Pick what you can afford; swap later.
4. **"Created and logged in" is the bar.** You don't need to configure anything deeply today — just prove each account exists and opens.

## Common pitfalls

- ❌ **Agonising over the business name.** It's a $12 domain, not a tattoo. Use AI, pick in 10 minutes, move on.
- ❌ **Opening accounts under someone else's name** "just for now." That's fraud. Use your own identity everywhere.
- ❌ **Skipping the free tiers and paying for everything on day one.** GHL, Google Workspace, and your AI assistant all have trials or free plans. Spend the minimum until you have a client.
- ❌ **Rushing Meta setup** (page → ad account → portfolio in five minutes). Do it in steps over a few days or Meta restricts you.
- ❌ **Buying followers / cheap-geo page likes** to look established. Against Meta's terms and it teaches the algorithm the wrong audience.

---

## 🛠️ Capstone Project: the "Setup complete" checklist

> This is the main hands-on project for the lesson. It proves your tools are real — not "I'll do it later," but created, in your name, and openable right now.

### What you will build

Not a product — a *foundation*. By the end you have a folder of logins (use a password manager) where every account below opens on the first try. Each item maps directly to a Part above.

### Why this is the perfect practice

| Lesson idea | Where you prove it |
|---|---|
| Name + domain (Part 1) | Domain shows as owned in your registrar |
| DNS protection (Part 2) | Cloudflare shows a green "active" check |
| Business email (Part 3) | You can send a test email from `you@yourbusiness.com` |
| Payments in your name (Part 4) | Stripe dashboard loads; a test payment link exists |
| CRM + sub-account (Part 5) | You can switch into your agency sub-account |
| Meta page (Part 6) | Your Facebook page is live and you're admin |
| AI assistant (Part 7) | It answered one test prompt |
| Trackers (Part 8) | Your own editable copy sits in your Drive |

### Milestones (build them in order, each one works on its own)

1. **Name locked, domain bought.** You own one `.com` in your registrar account.
2. **DNS live.** Cloudflare (or your registrar's DNS) shows the domain active.
3. **Business email works.** You sent yourself one email from your new address.
4. **Bank + Stripe open, in your legal name.** Stripe dashboard loads and a test payment link is created.
5. **GoHighLevel sub-account created.** You can log in and switch into your own agency workspace.
6. **Facebook page live.** The page exists, with a logo, and you are its admin.
7. **AI assistant + trackers ready.** One test prompt answered; your own copy of the trackers is in your Drive.
8. **Stretch goals.** Add a logo in Canva; connect your Google Calendar to GoHighLevel; register your business legally (ask your AI to outline the steps for your country/state).

### How you will know you are done

- ✅ You can open **every** account in the table above and see its dashboard, right now, without a password reset.
- ✅ **Every** account was created with **your own** legal name and information.
- ✅ You sent one test email from your business address and it arrived.
- ✅ Your GoHighLevel account has **one sub-account** for your agency that you can enter.

> 💡 **Keep yourself honest:** "created" means *logged in and dashboard loaded* — not "I made the tab and closed it." If you can't open it cold, it isn't done.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks for extra practice. Optional — the Capstone already covers the essentials.

### Exercise 1: Name sprint (foundational)
Ask your AI for 20 agency names, shortlist 3, and check `.com` availability for each. Notice how fast "the perfect name" stops mattering once you see the options.

### Exercise 2: Payment link (intermediate)
In Stripe, create a payment link for a fake $1,500 service named after your business. Open it in a private window to see what a client would see. Then archive it.

### Exercise 3: Calendar connect (advanced)
Connect your new Google Calendar to your GoHighLevel sub-account as both a **linked** and a **conflict** calendar, then block out non-working hours so the CRM only offers real availability.

---

## Cheat sheet

```text
THE PRE-FLIGHT STACK (create each, log in, done)
1. Name + domain ...... AI for name → registrar (GoDaddy/Namecheap/Porkbun) ~$12/yr
2. DNS ................ Cloudflare free plan → paste name servers into registrar
3. Email ............. Google Workspace (~$12-20/mo, 14-day trial) you@yourbiz.com
4. Bank .............. Chase / Revolut — YOUR LEGAL NAME
5. Payments ......... Stripe (alt: Square/PayPal/Paddle) — YOUR LEGAL NAME
6. CRM .............. GoHighLevel trial → 1 sub-account (alt: HubSpot/Close/stack)
                      $97/mo = 3 sub-accts · $297/mo = unlimited
7. Meta ............. facebook.com/pages → business page (don't rush ad acct)
8. AI ............... Claude / ChatGPT / Gemini — one test prompt
9. Trackers ......... File → Make a copy of the course sheets into your Drive

THREE RULES
- Own everything in YOUR OWN legal name. Someone else's name = fraud.
- Use free tiers/trials until you have a paying client.
- "Done" = you can open the dashboard cold. No fake followers, ever.
```

## How this connects to the rest of the course

- **Next, Module 0 → Module 1 · Lesson 1: "What this business actually is."** Now that the tools exist, that lesson explains the business model they serve — a local-business marketing agency.
- **Later, Module 4 (Infrastructure):** you'll go deep on GoHighLevel — funnels, automations, and connecting this domain and calendar into a working booking system.
- **Later, Module 5 (Meta Ads Mastery):** the Facebook page you made today becomes the launchpad for real ad campaigns.

---

*Source: "AI Agency Full Course" by Owen Rensland. Prices, plan names, and steps are illustrative of what he describes and change often — verify current pricing yourself. Adapt tool choices to your country and budget.*
